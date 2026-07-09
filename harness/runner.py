"""Eval runner. Spec: TESTING-METHODOLOGY.md section 5.

Runs every case through `claude -p` under two conditions — arm A (no
instructions) and arm B (instruction files present) — N times each, grades
each response with the Layer-1 deterministic checkers, and writes pass
fractions to results/<run-id>.json. Judge checks are skipped for now.

Isolation: CLAUDE_CONFIG_DIR points at an empty sandbox so the operator's
global ~/.claude/CLAUDE.md (which contains these same instructions) cannot
contaminate arm A. Only PATH and API credentials pass through.
"""
import argparse
import json
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv

from checks import CHECKS, run_check
from scoring import append_history, baseline, evaluate_gate, load_history, summarize

INSTRUCTION_FILES = ["CLAUDE.md", "PLAN_BUILD_MATRIX_RESPONSE_TEMPLATES.md"]
ENV_FILE = Path(__file__).resolve().parent / ".env"
PASSTHROUGH_ENV = ["PATH", "ANTHROPIC_API_KEY"]
TIMEOUT_SECONDS = 300
MODEL_IDS = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-5"}
MAX_TOKENS = 4096
RATE_LIMIT_RETRIES = 5
RATE_LIMIT_WAIT = 60


def load_env(path=ENV_FILE):
    # shell/CI env always wins over the file (override=False is the default)
    load_dotenv(path)


def load_cases(cases_dir):
    cases = [json.loads(p.read_text()) for p in Path(cases_dir).glob("*.json")]
    return sorted(cases, key=lambda c: c["id"])


def make_workdir(arm, repo_root, sandbox):
    d = Path(sandbox) / f"arm-{arm}-{uuid.uuid4().hex[:8]}"
    d.mkdir(parents=True)
    if arm == "B":
        for name in INSTRUCTION_FILES:
            shutil.copy(Path(repo_root) / name, d / name)
    return d


def isolated_env(config_dir):
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    return env


def call_claude(prompt, workdir, env, model, session=None, run=subprocess.run):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--setting-sources", "project"]
    if session:
        cmd += ["--resume", session]
    proc = run(cmd, cwd=workdir, env=env, capture_output=True, text=True,
               timeout=TIMEOUT_SECONDS)
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude exited {proc.returncode}\n"
            f"stderr: {proc.stderr.strip()}\nstdout: {proc.stdout.strip()[:2000]}")
    data = json.loads(proc.stdout)
    return data["result"], data.get("session_id")


def run_sample(case, workdir, env, model, run=subprocess.run):
    result, session = None, None
    for turn in case["turns"]:
        result, session = call_claude(turn, workdir, env, model,
                                      session=session, run=run)
    return result


def instruction_system_prompt(repo_root):
    return "\n\n".join((Path(repo_root) / f).read_text() for f in INSTRUCTION_FILES)


def call_api(messages, system, model, client, sleep=time.sleep):
    kwargs = {"model": MODEL_IDS.get(model, model), "max_tokens": MAX_TOKENS,
              "messages": messages}
    if system:
        kwargs["system"] = system
    for attempt in range(RATE_LIMIT_RETRIES):
        try:
            resp = client.messages.create(**kwargs)
            return "".join(b.text for b in resp.content if b.type == "text")
        except Exception as e:
            if getattr(e, "status_code", None) == 429 and attempt < RATE_LIMIT_RETRIES - 1:
                sleep(RATE_LIMIT_WAIT)
                continue
            raise


def run_sample_api(case, system, model, client, sleep=time.sleep):
    messages, text = [], None
    for turn in case["turns"]:
        messages.append({"role": "user", "content": turn})
        text = call_api(list(messages), system, model, client, sleep=sleep)
        messages.append({"role": "assistant", "content": text})
    return text


def grade_sample(case, response):
    return {c: run_check(c, response) for c in case["checks"] if c in CHECKS}


def pass_fractions(samples):
    checks = samples[0].keys()
    return {c: sum(s[c] for s in samples) / len(samples) for c in checks}


def run_suite(cases, n, model, repo_root, sandbox, run=subprocess.run,
              runtime="cli", client=None):
    config_dir = Path(sandbox) / "claude-config"
    config_dir.mkdir(parents=True, exist_ok=True)
    env = isolated_env(config_dir)
    system_b = instruction_system_prompt(repo_root) if runtime == "api" else None

    arms = {}
    for arm in ["A", "B"]:
        arms[arm] = {}
        for case in cases:
            samples = []
            for _ in range(n):
                if runtime == "api":
                    system = system_b if arm == "B" else None
                    response = run_sample_api(case, system, model, client)
                else:
                    workdir = make_workdir(arm, repo_root, sandbox)
                    response = run_sample(case, workdir, env, model, run=run)
                samples.append(grade_sample(case, response))
            fractions = pass_fractions(samples)
            arms[arm][case["id"]] = {
                "checks": fractions,
                "score": sum(fractions.values()) / len(fractions) if fractions else None,
                "status": case.get("status"),
            }
    return {"arms": arms, "n": n, "model": model, "runtime": runtime}


def write_results(results, out_dir, run_id):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{run_id}.json"
    path.write_text(json.dumps(results, indent=2) + "\n")
    return path


def _git_sha(repo_root):
    proc = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                          cwd=repo_root, capture_output=True, text=True)
    return proc.stdout.strip() or "unknown"


def main():
    load_env()
    repo_root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Run the instruction eval suite.")
    ap.add_argument("--n", type=int, default=5, help="samples per case per arm")
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--runtime", choices=["api", "cli"], default="cli",
                    help="api: raw messages API (cheap, no Claude Code harness); "
                         "cli: claude -p (real-world conditions)")
    ap.add_argument("--cases", default=repo_root / "tests" / "cases")
    ap.add_argument("--out", default=repo_root / "results")
    ap.add_argument("--sandbox", default=None, help="scratch dir (default: temp)")
    args = ap.parse_args()

    import tempfile
    sandbox = args.sandbox or tempfile.mkdtemp(prefix="pbm-eval-")

    client = None
    if args.runtime == "api":
        import anthropic
        client = anthropic.Anthropic()

    cases = load_cases(args.cases)
    results = run_suite(cases, n=args.n, model=args.model,
                        repo_root=repo_root, sandbox=sandbox,
                        runtime=args.runtime, client=client)
    results["instructions_sha"] = _git_sha(repo_root)
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    summary = summarize(results)
    history_path = Path(args.out) / "history.jsonl"
    base = baseline(load_history(history_path), runtime=args.runtime)
    gate_ok, reasons = evaluate_gate(summary, base)
    results["summary"] = summary
    results["gate"] = {"ok": gate_ok, "reasons": reasons, "baseline": base}

    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{results['instructions_sha']}"
    path = write_results(results, out_dir=args.out, run_id=run_id)
    append_history(history_path, {
        "run_id": run_id,
        "runtime": args.runtime,
        "sha": results["instructions_sha"],
        "timestamp": results["timestamp"],
        "suite": summary["suite"],
        "dimensions": summary["dimensions"],
        "lift": summary["lift"],
        "gate": gate_ok,
    })

    print(f"wrote {path}")
    print(f"suite {summary['suite']}, lift {summary['lift']}, gate {'PASS' if gate_ok else 'FAIL'}")
    for reason in reasons:
        print(f"  {reason}")
    raise SystemExit(0 if gate_ok else 1)


if __name__ == "__main__":
    main()

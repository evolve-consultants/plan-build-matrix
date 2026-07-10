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
import copy
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


class PacedClient:
    """Wraps an anthropic client, enforcing a minimum interval between calls
    so runs respect the org's requests-per-minute limit proactively instead
    of discovering it one 429 at a time."""

    def __init__(self, client, interval, clock=time.monotonic, sleep=time.sleep):
        self._client = client
        self._interval = interval
        self._clock = clock
        self._sleep = sleep
        self._last = None
        self.messages = self

    def create(self, **kwargs):
        now = self._clock()
        if self._last is not None:
            wait = self._last + self._interval - now
            if wait > 0:
                self._sleep(wait)
                now += wait
        self._last = now
        return self._client.messages.create(**kwargs)


def call_api(messages, system, model, client, sleep=time.sleep, out=print):
    kwargs = {"model": MODEL_IDS.get(model, model), "max_tokens": MAX_TOKENS,
              "messages": messages}
    if system:
        # constant across calls: cacheable, so repeats are cache reads
        # (excluded from ITPM and 10x cheaper)
        kwargs["system"] = [{"type": "text", "text": system,
                             "cache_control": {"type": "ephemeral"}}]
    for attempt in range(RATE_LIMIT_RETRIES):
        try:
            resp = client.messages.create(**kwargs)
            return "".join(b.text for b in resp.content if b.type == "text")
        except Exception as e:
            if getattr(e, "status_code", None) == 429 and attempt < RATE_LIMIT_RETRIES - 1:
                out(f"  rate limited (429): waiting {RATE_LIMIT_WAIT}s "
                    f"(attempt {attempt + 1}/{RATE_LIMIT_RETRIES})")
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


def grade_sample(case, response, judge=None):
    verdicts = {}
    for c in case["checks"]:
        if c in CHECKS:
            verdicts[c] = run_check(c, response)
        elif judge is not None:
            verdicts[c] = judge(c, case, response)
    return verdicts


def pass_fractions(samples):
    checks = samples[0].keys()
    return {c: sum(s[c] for s in samples) / len(samples) for c in checks}


def run_suite(cases, n, model, repo_root, sandbox, run=subprocess.run,
              runtime="cli", client=None, judge=None, log=None, checkpoint=None):
    log = log or (lambda _msg: None)
    config_dir = Path(sandbox) / "claude-config"
    config_dir.mkdir(parents=True, exist_ok=True)
    env = isolated_env(config_dir)
    system_b = instruction_system_prompt(repo_root) if runtime == "api" else None

    results = {"arms": {}, "n": n, "model": model, "runtime": runtime}
    arms = results["arms"]
    for arm in ["A", "B"]:
        arms[arm] = {}
        for idx, case in enumerate(cases, 1):
            verdicts, responses = [], []
            for _ in range(n):
                if runtime == "api":
                    system = system_b if arm == "B" else None
                    response = run_sample_api(case, system, model, client)
                else:
                    workdir = make_workdir(arm, repo_root, sandbox)
                    response = run_sample(case, workdir, env, model, run=run)
                responses.append(response)
                verdicts.append(grade_sample(case, response, judge=judge))
            fractions = pass_fractions(verdicts)
            score = sum(fractions.values()) / len(fractions) if fractions else None
            arms[arm][case["id"]] = {
                "checks": fractions,
                "score": score,
                "status": case.get("status"),
                "samples": responses,
                "sample_verdicts": verdicts,
            }
            log(f"[arm {arm} {idx}/{len(cases)}] {case['id']} "
                f"score={score if score is None else round(score, 2)}")
            if checkpoint:
                checkpoint(results)
    return results


def write_transcripts(results, transcripts_root, run_id):
    run_dir = Path(transcripts_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    for arm, cases in results["arms"].items():
        for case_id, case_result in cases.items():
            paths = []
            for i, text in enumerate(case_result.pop("samples", [])):
                name = f"{arm}-{case_id}-{i}.md"
                (run_dir / name).write_text(text or "")
                paths.append(f"{run_id}/{name}")
            case_result["transcripts"] = paths


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
    ap.add_argument("--pace", type=float, default=1.5,
                    help="min seconds between API calls; match your org's "
                         "requests/min limit (free tier 5 rpm -> 12)")
    ap.add_argument("--judge", action="store_true",
                    help="enable LLM-judge checks (calibrates against "
                         "tests/golden/ first; aborts below 90% agreement)")
    ap.add_argument("--runtime", choices=["api", "cli"], default="api",
                    help="api: raw messages API, instructions as system prompt "
                         "(canonical, reproducible); cli: claude -p inside the "
                         "Claude Code harness (manual/exploratory only)")
    ap.add_argument("--cases", default=repo_root / "tests" / "cases")
    ap.add_argument("--out", default=repo_root / "results")
    ap.add_argument("--transcripts", default=repo_root / "transcripts")
    ap.add_argument("--sandbox", default=None, help="scratch dir (default: temp)")
    args = ap.parse_args()

    import tempfile
    sandbox = args.sandbox or tempfile.mkdtemp(prefix="pbm-eval-")

    client = None
    if args.runtime == "api" or args.judge:
        import anthropic
        client = PacedClient(anthropic.Anthropic(), interval=args.pace)

    cases = load_cases(args.cases)

    judge_fn, calibration = None, None
    if args.judge:
        from judge import calibrate, load_golden, make_judge
        golden = load_golden(repo_root / "tests" / "golden")
        cases_by_id = {c["id"]: c for c in cases}
        calibration = calibrate(golden, cases_by_id, client)
        print(f"judge calibration: {calibration:.0%} ({len(golden)} golden items)")
        if calibration < 0.90:
            raise SystemExit("judge below 90% agreement with golden set - "
                             "run aborted as untrustworthy")
        judge_fn = make_judge(client)

    sha = _git_sha(repo_root)
    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{sha}"

    def save_progress(partial):
        # a crash loses nothing: transcripts + partial results land per case
        snapshot = copy.deepcopy(partial)
        write_transcripts(snapshot, transcripts_root=args.transcripts, run_id=run_id)
        write_results(snapshot, out_dir=args.out, run_id=run_id)

    results = run_suite(cases, n=args.n, model=args.model,
                        repo_root=repo_root, sandbox=sandbox,
                        runtime=args.runtime, client=client, judge=judge_fn,
                        log=print, checkpoint=save_progress)
    results["judge_calibration"] = calibration
    results["instructions_sha"] = sha
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    summary = summarize(results)
    history_path = Path(args.out) / "history.jsonl"
    base = baseline(load_history(history_path), runtime=args.runtime)
    gate_ok, reasons = evaluate_gate(summary, base)
    results["summary"] = summary
    results["gate"] = {"ok": gate_ok, "reasons": reasons, "baseline": base}

    write_transcripts(results, transcripts_root=args.transcripts, run_id=run_id)
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

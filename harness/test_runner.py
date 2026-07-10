"""Runner tests. Spec: TESTING-METHODOLOGY.md section 5.

subprocess calls are faked — no API spend, no claude binary needed.
"""
import json
import os
from pathlib import Path

import pytest
from types import SimpleNamespace

from runner import (
    INSTRUCTION_FILES,
    call_api,
    call_claude,
    grade_sample,
    instruction_system_prompt,
    isolated_env,
    load_cases,
    load_env,
    make_workdir,
    pass_fractions,
    run_sample,
    run_sample_api,
    run_suite,
    write_results,
    write_transcripts,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class FakeRun:
    """Captures commands; replays canned claude JSON responses."""

    def __init__(self, results):
        self.results = list(results)
        self.commands = []

    def __call__(self, cmd, **kwargs):
        self.commands.append((cmd, kwargs))
        body = self.results.pop(0)

        class Proc:
            returncode = body.get("returncode", 0)
            stdout = json.dumps(body) if "result" in body else body.get("stdout", "")
            stderr = body.get("stderr", "")

        return Proc()


def fake(result="hello", session_id="sess-1", **extra):
    return {"result": result, "session_id": session_id, **extra}


# --- load_cases --------------------------------------------------------------

def test_load_cases_reads_sorted_json(tmp_path):
    (tmp_path / "b.json").write_text(json.dumps({"id": "b", "turns": ["x"], "checks": []}))
    (tmp_path / "a.json").write_text(json.dumps({"id": "a", "turns": ["y"], "checks": []}))
    cases = load_cases(tmp_path)
    assert [c["id"] for c in cases] == ["a", "b"]


def test_load_cases_on_real_dataset():
    cases = load_cases(REPO_ROOT / "tests" / "cases")
    assert {c["id"] for c in cases} >= {"ul-messy-brief-01", "br-final-form-01", "triv-lookup-01"}


# --- make_workdir ------------------------------------------------------------

def test_workdir_arm_a_is_empty(tmp_path):
    d = make_workdir("A", REPO_ROOT, tmp_path)
    assert list(d.iterdir()) == []


def test_workdir_arm_b_has_instruction_files(tmp_path):
    d = make_workdir("B", REPO_ROOT, tmp_path)
    names = {p.name for p in d.iterdir()}
    assert names == set(INSTRUCTION_FILES)


# --- isolated_env ------------------------------------------------------------

def test_isolated_env_points_config_at_sandbox(tmp_path):
    env = isolated_env(tmp_path)
    assert env["CLAUDE_CONFIG_DIR"] == str(tmp_path)


def test_isolated_env_passes_api_key_and_path(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    env = isolated_env(tmp_path)
    assert env["ANTHROPIC_API_KEY"] == "sk-test"
    assert env["PATH"] == os.environ["PATH"]


# --- load_env ----------------------------------------------------------------

def test_load_env_reads_api_key_from_file(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    envfile = tmp_path / ".env"
    envfile.write_text("ANTHROPIC_API_KEY=sk-from-file\n")
    load_env(envfile)
    assert os.environ["ANTHROPIC_API_KEY"] == "sk-from-file"


def test_load_env_does_not_override_existing_env(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-from-shell")
    envfile = tmp_path / ".env"
    envfile.write_text("ANTHROPIC_API_KEY=sk-from-file\n")
    load_env(envfile)
    assert os.environ["ANTHROPIC_API_KEY"] == "sk-from-shell"


def test_load_env_tolerates_missing_file(tmp_path):
    load_env(tmp_path / "nope.env")   # must not raise


# --- call_claude -------------------------------------------------------------

def test_call_claude_builds_print_command(tmp_path):
    run = FakeRun([fake()])
    call_claude("hi", tmp_path, {}, "haiku", run=run)
    cmd, kwargs = run.commands[0]
    assert cmd[:3] == ["claude", "-p", "hi"]
    assert cmd[cmd.index("--model") + 1] == "haiku"
    assert cmd[cmd.index("--output-format") + 1] == "json"
    assert "--resume" not in cmd
    assert kwargs["cwd"] == tmp_path


def test_call_claude_resumes_session(tmp_path):
    run = FakeRun([fake()])
    call_claude("again", tmp_path, {}, "haiku", session="sess-9", run=run)
    cmd, _ = run.commands[0]
    assert cmd[cmd.index("--resume") + 1] == "sess-9"


def test_call_claude_returns_result_and_session(tmp_path):
    run = FakeRun([fake(result="the answer", session_id="s42")])
    result, session = call_claude("q", tmp_path, {}, "haiku", run=run)
    assert (result, session) == ("the answer", "s42")


def test_call_claude_raises_on_failure(tmp_path):
    run = FakeRun([{"returncode": 1, "stderr": "boom"}])
    with pytest.raises(RuntimeError, match="boom"):
        call_claude("q", tmp_path, {}, "haiku", run=run)


def test_call_claude_failure_includes_stdout(tmp_path):
    # with --output-format json, claude reports errors on stdout
    run = FakeRun([{"returncode": 1, "stderr": "", "stdout": "Invalid API key"}])
    with pytest.raises(RuntimeError, match="Invalid API key"):
        call_claude("q", tmp_path, {}, "haiku", run=run)


# --- run_sample --------------------------------------------------------------

def test_run_sample_multi_turn_resumes(tmp_path):
    case = {"id": "x", "turns": ["one", "two"], "checks": []}
    run = FakeRun([fake(result="r1", session_id="s1"), fake(result="r2", session_id="s1")])
    result = run_sample(case, tmp_path, {}, "haiku", run=run)
    assert result == "r2"
    first_cmd, _ = run.commands[0]
    second_cmd, _ = run.commands[1]
    assert "--resume" not in first_cmd
    assert second_cmd[second_cmd.index("--resume") + 1] == "s1"


# --- grading + aggregation ----------------------------------------------------

def test_grade_sample_runs_only_deterministic_checks():
    case = {"id": "x", "turns": ["q"], "checks": ["position-stated", "position-correct", "assumptions-present"]}
    verdicts = grade_sample(case, "**Operating from: Upper-Left**")
    assert set(verdicts) == {"position-stated", "assumptions-present"}   # position-correct is a judge check: skipped without a judge
    assert verdicts["position-stated"] is True
    assert verdicts["assumptions-present"] is False


def test_grade_sample_includes_judge_checks_when_judge_provided():
    case = {"id": "x", "turns": ["q"], "checks": ["position-stated", "position-correct"]}
    judged = []
    def judge(check_id, c, response):
        judged.append(check_id)
        return True
    verdicts = grade_sample(case, "**Operating from: Upper-Left**", judge=judge)
    assert verdicts == {"position-stated": True, "position-correct": True}
    assert judged == ["position-correct"]


def test_run_suite_threads_judge_through(tmp_path):
    case = {"id": "c1", "turns": ["q"], "checks": ["position-correct"], "status": "gating"}
    run = FakeRun([fake() for _ in range(2)])
    results = run_suite([case], n=1, model="haiku", repo_root=REPO_ROOT,
                        sandbox=tmp_path, run=run,
                        judge=lambda cid, c, r: True)
    assert results["arms"]["B"]["c1"]["checks"]["position-correct"] == 1.0


def test_pass_fractions():
    samples = [{"position-stated": True, "assumptions-present": True}, {"position-stated": True, "assumptions-present": False}, {"position-stated": False, "assumptions-present": False}]
    assert pass_fractions(samples) == {"position-stated": pytest.approx(2 / 3), "assumptions-present": pytest.approx(1 / 3)}


# --- api runtime ---------------------------------------------------------------

class FakeAPI:
    """Stands in for anthropic.Anthropic(); records create() kwargs."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []
        self.messages = self   # client.messages.create(...)

    def create(self, **kwargs):
        self.calls.append(kwargs)
        out = self.outputs.pop(0)
        if isinstance(out, Exception):
            raise out
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=out)])


def test_instruction_system_prompt_concatenates_files():
    system = instruction_system_prompt(REPO_ROOT)
    assert "Plan-Build Matrix" in system
    assert "Response Templates" in system


def test_call_api_maps_model_alias_and_passes_system():
    client = FakeAPI(["hi"])
    call_api([{"role": "user", "content": "q"}], "SYS", "haiku", client)
    kwargs = client.calls[0]
    assert kwargs["model"] == "claude-haiku-4-5-20251001"
    assert kwargs["system"] == "SYS"


def test_call_api_omits_system_when_none():
    client = FakeAPI(["hi"])
    call_api([{"role": "user", "content": "q"}], None, "haiku", client)
    assert "system" not in client.calls[0]


def test_call_api_retries_on_429_then_succeeds():
    err = Exception("rate limited")
    err.status_code = 429
    client = FakeAPI([err, "recovered"])
    naps = []
    text = call_api([{"role": "user", "content": "q"}], None, "haiku", client,
                    sleep=naps.append)
    assert text == "recovered"
    assert len(naps) == 1


def test_call_api_raises_non_rate_limit_errors():
    err = Exception("bad request")
    err.status_code = 400
    client = FakeAPI([err])
    with pytest.raises(Exception, match="bad request"):
        call_api([{"role": "user", "content": "q"}], None, "haiku", client)


def test_run_sample_api_multi_turn_accumulates_messages():
    case = {"id": "x", "turns": ["one", "two"], "checks": []}
    client = FakeAPI(["r1", "r2"])
    result = run_sample_api(case, None, "haiku", client)
    assert result == "r2"
    second = client.calls[1]["messages"]
    assert [m["role"] for m in second] == ["user", "assistant", "user"]
    assert second[1]["content"] == "r1"


def test_run_suite_api_arm_a_has_no_system_arm_b_has_instructions(tmp_path):
    case = {"id": "c1", "turns": ["q"], "checks": ["position-stated"], "status": "gating"}
    client = FakeAPI(["r"] * 4)
    results = run_suite([case], n=2, model="haiku", repo_root=REPO_ROOT,
                        sandbox=tmp_path, runtime="api", client=client)
    arm_a_calls, arm_b_calls = client.calls[:2], client.calls[2:]
    assert all("system" not in c for c in arm_a_calls)
    assert all("Plan-Build Matrix" in c["system"] for c in arm_b_calls)
    assert results["runtime"] == "api"


def test_run_suite_cli_results_note_runtime(tmp_path):
    case = {"id": "c1", "turns": ["q"], "checks": ["position-stated"], "status": "gating"}
    run = FakeRun([fake() for _ in range(2)])
    results = run_suite([case], n=1, model="haiku", repo_root=REPO_ROOT,
                        sandbox=tmp_path, run=run)
    assert results["runtime"] == "cli"


# --- run_suite + write_results -------------------------------------------------

def test_run_suite_runs_both_arms(tmp_path):
    case = {"id": "c1", "turns": ["q"], "checks": ["position-stated"], "status": "gating"}
    run = FakeRun([fake() for _ in range(4)])   # 2 arms x n=2
    results = run_suite([case], n=2, model="haiku", repo_root=REPO_ROOT,
                        sandbox=tmp_path, run=run)
    assert set(results["arms"]) == {"A", "B"}
    assert results["arms"]["A"]["c1"]["checks"]["position-stated"] == 0.0   # "hello" has no scaffold
    assert results["n"] == 2
    assert len(run.commands) == 4


def test_run_suite_keeps_raw_samples(tmp_path):
    case = {"id": "c1", "turns": ["q"], "checks": ["position-stated"], "status": "gating"}
    run = FakeRun([fake(result="resp-arm-a"), fake(result="resp-arm-b")])
    results = run_suite([case], n=1, model="haiku", repo_root=REPO_ROOT,
                        sandbox=tmp_path, run=run)
    assert results["arms"]["A"]["c1"]["samples"] == ["resp-arm-a"]
    assert results["arms"]["B"]["c1"]["samples"] == ["resp-arm-b"]


def test_write_transcripts_writes_files_and_rewrites_references(tmp_path):
    results = {"arms": {"A": {"c1": {"samples": ["hello world", "second try"],
                                     "checks": {"position-stated": 0.0}}}}}
    write_transcripts(results, transcripts_root=tmp_path, run_id="r1")
    assert (tmp_path / "r1" / "A-c1-0.md").read_text() == "hello world"
    assert (tmp_path / "r1" / "A-c1-1.md").read_text() == "second try"
    case = results["arms"]["A"]["c1"]
    assert case["transcripts"] == ["r1/A-c1-0.md", "r1/A-c1-1.md"]
    assert "samples" not in case   # raw text must not bloat results.json


def test_write_results_creates_run_file(tmp_path):
    results = {"arms": {}, "n": 1, "model": "haiku"}
    path = write_results(results, out_dir=tmp_path, run_id="r1")
    assert path == tmp_path / "r1.json"
    assert json.loads(path.read_text())["model"] == "haiku"

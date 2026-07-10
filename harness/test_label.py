"""Labeler tests: candidate generation from a run + the y/n/s/q loop."""
import json
from pathlib import Path

from label import candidates, label_loop, latest_run

CASES = {"c1": {"id": "c1", "quadrant": "upper-left", "turns": ["my prompt"]}}


def make_run_fixture(tmp_path):
    """A minimal results dict + transcript files on disk."""
    tdir = tmp_path / "transcripts" / "r1"
    tdir.mkdir(parents=True)
    (tdir / "B-c1-0.md").write_text("full response zero")
    (tdir / "B-c1-1.md").write_text("full response one")
    (tdir / "A-c1-0.md").write_text("bare baseline answer")
    results = {"arms": {
        "B": {"c1": {
            "checks": {"position-stated": 1.0, "position-correct": 0.5},
            "transcripts": ["r1/B-c1-0.md", "r1/B-c1-1.md"],
            "sample_verdicts": [
                {"position-stated": True, "position-correct": True},
                {"position-stated": True, "position-correct": False},
            ],
        }},
        "A": {"c1": {
            "checks": {"position-stated": 0.0, "position-correct": 0.0},
            "transcripts": ["r1/A-c1-0.md"],
            "sample_verdicts": [
                {"position-stated": False, "position-correct": False},
            ],
        }},
    }}
    return results, tmp_path / "transcripts"


# --- latest_run ----------------------------------------------------------------

def test_latest_run_picks_newest_by_name(tmp_path):
    (tmp_path / "20260709-120000-aaa.json").write_text(json.dumps({"run": 1}))
    (tmp_path / "20260710-090000-bbb.json").write_text(json.dumps({"run": 2}))
    (tmp_path / "history.jsonl").write_text("")   # must be ignored
    assert latest_run(tmp_path)["run"] == 2


# --- candidate generation --------------------------------------------------------

def test_candidates_judge_checks_only_with_proposed_labels(tmp_path):
    results, troot = make_run_fixture(tmp_path)
    cands = candidates(results, troot, golden=[])
    # position-stated is deterministic: never a candidate
    assert all(c["check"] == "position-correct" for c in cands)
    assert len(cands) == 3
    by_response = {c["response"]: c["proposed_label"] for c in cands}
    assert by_response["full response zero"] == "pass"
    assert by_response["full response one"] == "fail"


def test_candidates_carry_their_arm(tmp_path):
    results, troot = make_run_fixture(tmp_path)
    arms = {c["response"]: c["arm"] for c in candidates(results, troot, golden=[])}
    assert arms["bare baseline answer"] == "A"
    assert arms["full response zero"] == "B"


def test_candidates_arm_filter(tmp_path):
    results, troot = make_run_fixture(tmp_path)
    cands = candidates(results, troot, golden=[], arm="B")
    assert len(cands) == 2
    assert all(c["arm"] == "B" for c in cands)


def test_candidates_skip_items_already_in_golden(tmp_path):
    results, troot = make_run_fixture(tmp_path)
    golden = [{"case_id": "c1", "check": "position-correct",
               "response": "full response zero", "label": "pass"}]
    cands = candidates(results, troot, golden=golden)
    assert {c["response"] for c in cands} == {"full response one", "bare baseline answer"}


def test_candidates_put_disagreements_first(tmp_path):
    # judge failed position-correct while deterministic sibling passed -> most
    # informative to label, so it must sort before the agreeing sample
    results, troot = make_run_fixture(tmp_path)
    cands = candidates(results, troot, golden=[])
    assert cands[0]["proposed_label"] == "fail"


# --- label loop -------------------------------------------------------------------

def run_loop(tmp_path, cands, answers):
    golden_path = tmp_path / "golden.json"
    golden_path.write_text("[]")
    answers = iter(answers)
    shown = []
    added = label_loop(cands, golden_path, CASES,
                       ask=lambda _prompt: next(answers), out=shown.append)
    return added, json.loads(golden_path.read_text()), shown


def cand(response="resp", label="pass"):
    return {"case_id": "c1", "check": "position-correct",
            "response": response, "proposed_label": label, "run_id": "r1"}


def test_label_loop_y_certifies_proposed_label(tmp_path):
    added, golden, _ = run_loop(tmp_path, [cand(label="pass")], ["y"])
    assert added == 1
    assert golden[0]["label"] == "pass"
    assert golden[0]["labeled_by"] == "operator"
    assert golden[0]["response_source"] == "transcript"


def test_label_loop_n_flips_label(tmp_path):
    added, golden, _ = run_loop(tmp_path, [cand(label="pass")], ["n"])
    assert golden[0]["label"] == "fail"
    assert golden[0]["labeled_by"] == "operator"


def test_label_loop_s_skips_and_q_quits(tmp_path):
    cands = [cand("r1"), cand("r2"), cand("r3")]
    added, golden, _ = run_loop(tmp_path, cands, ["s", "q"])
    assert added == 0
    assert golden == []


def test_label_loop_shows_expected_and_received_evidence(tmp_path):
    response = "Some intro.\n**Operating from: Bottom-Right (Build + Quality)**\nMore text." * 3
    _, _, shown = run_loop(tmp_path, [cand(response)], ["y"])
    joined = "\n".join(shown)
    assert "my prompt" in joined
    assert "EXPECTED" in joined and "upper-left" in joined
    assert "RECEIVED" in joined and "Operating from: Bottom-Right" in joined
    assert "CRITERION" in joined


def test_label_loop_reports_missing_evidence(tmp_path):
    _, _, shown = run_loop(tmp_path, [cand("no position anywhere here")], ["y"])
    assert any("no matching evidence" in s for s in shown)


def test_label_loop_v_shows_full_response_then_asks_again(tmp_path):
    added, golden, shown = run_loop(tmp_path, [cand("SECRET FULL BODY text")], ["v", "y"])
    assert added == 1
    assert any("SECRET FULL BODY" in s for s in shown)


def test_label_loop_saves_after_every_decision(tmp_path):
    golden_path = tmp_path / "golden.json"
    golden_path.write_text("[]")
    answers = iter(["y"])
    def ask(_prompt):
        try:
            return next(answers)
        except StopIteration:
            raise KeyboardInterrupt   # simulates Ctrl-C mid-session
    import pytest as _pytest
    with _pytest.raises(KeyboardInterrupt):
        label_loop([cand("r1"), cand("r2")], golden_path, CASES,
                   ask=ask, out=lambda _: None)
    saved = json.loads(golden_path.read_text())
    assert len(saved) == 1   # the decision before the crash survived


def test_label_loop_assigns_unique_sequential_ids(tmp_path):
    golden_path = tmp_path / "golden.json"
    golden_path.write_text(json.dumps([{"id": "g007", "case_id": "x", "check": "c",
                                        "response": "r", "label": "pass"}]))
    label_loop([cand("r1"), cand("r2")], golden_path, CASES,
               ask=lambda _: "y", out=lambda _: None)
    golden = json.loads(golden_path.read_text())
    ids = [g["id"] for g in golden]
    assert ids == ["g007", "g008", "g009"]
    assert len(set(ids)) == len(ids)

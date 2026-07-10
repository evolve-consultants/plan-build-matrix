"""Judge layer tests. Spec: TESTING-METHODOLOGY.md section 3, Layer 2.

The rubric file (tests/judge-rubric.md) is the single source of truth:
the judge module parses it rather than duplicating criteria in code.
"""
import pytest
from judge import build_prompt, calibrate, judge_check, load_golden, make_judge, parse_rubric
from test_runner import REPO_ROOT, FakeAPI

JUDGE_CHECK_IDS = {"position-correct", "assumptions-specific", "single-artifact", "minimal-commentary", "movement-on-challenge", "assumptions-on-demand", "uncertainty-separated", "commits-to-quality", "trivial-reason"}

CASE = {
    "id": "ul-messy-brief-01",
    "quadrant": "upper-left",
    "turns": ["My app is slow, maybe caching? What should I do?"],
}


def verdict(v):
    return f'{{"verdict": "{v}", "reason": "because"}}'


# --- rubric parsing ------------------------------------------------------------

def test_parse_rubric_extracts_frame_and_all_criteria():
    rubric = parse_rubric()
    assert "strict JSON" in rubric["frame"]
    assert set(rubric["criteria"]) == JUDGE_CHECK_IDS
    assert "PASS" in rubric["criteria"]["assumptions-specific"]


def test_build_prompt_fills_every_placeholder():
    rubric = parse_rubric()
    prompt = build_prompt(rubric, "position-correct", CASE, "**Operating from: Upper-Left**")
    assert "My app is slow" in prompt
    assert "upper-left" in prompt
    assert "Operating from: Upper-Left" in prompt
    assert "Criterion position-correct" in prompt
    for leftover in ["{user_turns}", "{expected_quadrant}", "{response}",
                     "{criterion_id}", "{criterion}"]:
        assert leftover not in prompt


# --- judging ---------------------------------------------------------------------

def test_judge_check_pass_verdict():
    client = FakeAPI([verdict("pass")])
    assert judge_check(parse_rubric(), "position-correct", CASE, "resp", client) is True


def test_judge_check_fail_verdict():
    client = FakeAPI([verdict("fail")])
    assert judge_check(parse_rubric(), "position-correct", CASE, "resp", client) is False


def test_judge_check_extracts_json_from_surrounding_text():
    client = FakeAPI(['Here is my verdict:\n```json\n{"verdict": "pass", "reason": "r"}\n```'])
    assert judge_check(parse_rubric(), "position-correct", CASE, "resp", client) is True


def test_judge_check_unparseable_output_is_fail():
    client = FakeAPI(["I think it is probably fine?"])
    assert judge_check(parse_rubric(), "position-correct", CASE, "resp", client) is False


def test_make_judge_binds_client():
    client = FakeAPI([verdict("pass")])
    judge = make_judge(client)
    assert judge("position-correct", CASE, "resp") is True


# --- golden set + calibration -----------------------------------------------------

def test_load_golden_skips_items_not_operator_labeled(tmp_path):
    import json
    items = [
        {"case_id": "c1", "check": "position-correct", "response": "r1",
         "label": "pass", "labeled_by": "operator"},
        {"case_id": "c1", "check": "position-correct", "response": "r2",
         "label": "fail", "labeled_by": None},          # proposed, unapproved
        {"case_id": "c1", "check": "assumptions-specific", "response": "r3",
         "label": "pass"},                               # field missing entirely
    ]
    (tmp_path / "golden.json").write_text(json.dumps(items))
    golden = load_golden(tmp_path)
    assert len(golden) == 1   # only the operator-labeled item counts
    assert golden[0]["response"] == "r1"


def test_calibrate_agreement_fraction():
    golden = [
        {"case_id": "c1", "check": "position-correct", "response": "r1", "label": "pass"},
        {"case_id": "c1", "check": "position-correct", "response": "r2", "label": "fail"},
        {"case_id": "c1", "check": "assumptions-specific", "response": "r3", "label": "pass"},
        {"case_id": "c1", "check": "assumptions-specific", "response": "r4", "label": "fail"},
    ]
    cases = {"c1": CASE}
    # judge agrees on first three, disagrees on the fourth
    client = FakeAPI([verdict("pass"), verdict("fail"), verdict("pass"), verdict("pass")])
    assert calibrate(golden, cases, client) == pytest.approx(0.75)


def test_calibrate_with_no_labeled_items_is_zero():
    assert calibrate([], {}, FakeAPI([])) == 0.0


def test_real_golden_file_has_unique_ids():
    import json
    items = json.loads((REPO_ROOT / "tests" / "golden" / "golden.json").read_text())
    ids = [g["id"] for g in items]
    assert all(ids), "every golden item needs an id"
    assert len(set(ids)) == len(ids), "golden ids must be unique"

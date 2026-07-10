"""Judge layer tests. Spec: TESTING-METHODOLOGY.md section 3, Layer 2.

The rubric file (tests/judge-rubric.md) is the single source of truth:
the judge module parses it rather than duplicating criteria in code.
"""
import pytest
from judge import build_prompt, calibrate, judge_check, load_golden, make_judge, parse_rubric
from test_runner import REPO_ROOT, FakeAPI

JUDGE_CHECK_IDS = {"1b", "2b", "4a", "4b", "5a", "6a", "7b", "8b", "9c"}

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
    assert "PASS" in rubric["criteria"]["2b"]


def test_build_prompt_fills_every_placeholder():
    rubric = parse_rubric()
    prompt = build_prompt(rubric, "1b", CASE, "**Operating from: Upper-Left**")
    assert "My app is slow" in prompt
    assert "upper-left" in prompt
    assert "Operating from: Upper-Left" in prompt
    assert "Criterion 1b" in prompt
    for leftover in ["{user_turns}", "{expected_quadrant}", "{response}",
                     "{criterion_id}", "{criterion}"]:
        assert leftover not in prompt


# --- judging ---------------------------------------------------------------------

def test_judge_check_pass_verdict():
    client = FakeAPI([verdict("pass")])
    assert judge_check(parse_rubric(), "1b", CASE, "resp", client) is True


def test_judge_check_fail_verdict():
    client = FakeAPI([verdict("fail")])
    assert judge_check(parse_rubric(), "1b", CASE, "resp", client) is False


def test_judge_check_extracts_json_from_surrounding_text():
    client = FakeAPI(['Here is my verdict:\n```json\n{"verdict": "pass", "reason": "r"}\n```'])
    assert judge_check(parse_rubric(), "1b", CASE, "resp", client) is True


def test_judge_check_unparseable_output_is_fail():
    client = FakeAPI(["I think it is probably fine?"])
    assert judge_check(parse_rubric(), "1b", CASE, "resp", client) is False


def test_make_judge_binds_client():
    client = FakeAPI([verdict("pass")])
    judge = make_judge(client)
    assert judge("1b", CASE, "resp") is True


# --- golden set + calibration -----------------------------------------------------

def test_load_golden_reads_seed():
    golden = load_golden(REPO_ROOT / "tests" / "golden")
    assert len(golden) >= 4
    assert all({"case_id", "check", "response_excerpt", "label"} <= set(g) for g in golden)


def test_calibrate_agreement_fraction():
    golden = [
        {"case_id": "c1", "check": "1b", "response_excerpt": "r1", "label": "pass"},
        {"case_id": "c1", "check": "1b", "response_excerpt": "r2", "label": "fail"},
        {"case_id": "c1", "check": "2b", "response_excerpt": "r3", "label": "pass"},
        {"case_id": "c1", "check": "2b", "response_excerpt": "r4", "label": "fail"},
    ]
    cases = {"c1": CASE}
    # judge agrees on first three, disagrees on the fourth
    client = FakeAPI([verdict("pass"), verdict("fail"), verdict("pass"), verdict("pass")])
    assert calibrate(golden, cases, client) == pytest.approx(0.75)

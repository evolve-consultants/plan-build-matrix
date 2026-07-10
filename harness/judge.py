"""LLM-as-judge layer. Spec: TESTING-METHODOLOGY.md section 3, Layer 2.

The rubric file is the single source of truth: frame and criteria are parsed
from tests/judge-rubric.md at runtime, so editing the rubric never requires
touching code (but does require golden-set recalibration, enforced in the
runner). One judge call per (check, sample); binary verdict; anything that
is not a clean "pass" — including unparseable output — is a fail.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_FILE = REPO_ROOT / "tests" / "judge-rubric.md"
JUDGE_MODEL = "claude-haiku-4-5-20251001"
JUDGE_MAX_TOKENS = 200

_FRAME = re.compile(r"```\n(.*?)```", re.S)
_CRITERION = re.compile(r"^### ([\w-]+) — .*?\n(.*?)(?=^### |\Z)", re.M | re.S)


def parse_rubric(path=RUBRIC_FILE):
    text = Path(path).read_text()
    return {
        "frame": _FRAME.search(text).group(1),
        "criteria": {cid: body.strip() for cid, body in _CRITERION.findall(text)},
    }


def build_prompt(rubric, check_id, case, response):
    prompt = rubric["frame"]
    substitutions = {
        "{user_turns}": "\n---\n".join(case["turns"]),
        "{expected_quadrant}": case.get("quadrant", ""),
        "{response}": response,
        "{criterion_id}": check_id,
        "{criterion}": rubric["criteria"][check_id],
    }
    for placeholder, value in substitutions.items():
        prompt = prompt.replace(placeholder, value)
    return prompt


def judge_check(rubric, check_id, case, response, client):
    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=JUDGE_MAX_TOKENS,
        messages=[{"role": "user",
                   "content": build_prompt(rubric, check_id, case, response)}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return False
    try:
        return json.loads(m.group(0)).get("verdict") == "pass"
    except json.JSONDecodeError:
        return False


def make_judge(client, rubric=None):
    rubric = rubric or parse_rubric()
    return lambda check_id, case, response: judge_check(
        rubric, check_id, case, response, client)


def load_golden(golden_dir):
    # only items whose label a human has certified may calibrate the judge
    golden = []
    for path in sorted(Path(golden_dir).glob("*.json")):
        golden.extend(g for g in json.loads(path.read_text())
                      if g.get("labeled_by") == "operator")
    return golden


def calibrate(golden, cases_by_id, client, rubric=None):
    if not golden:
        return 0.0   # no certified items -> judge is untrusted by definition
    rubric = rubric or parse_rubric()
    agreed = 0
    for g in golden:
        case = cases_by_id[g["case_id"]]
        got = judge_check(rubric, g["check"], case, g["response"], client)
        agreed += got == (g["label"] == "pass")
    return agreed / len(golden)

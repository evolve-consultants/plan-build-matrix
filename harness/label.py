"""Golden-set labeler: certify judge verdicts on real transcripts.

Candidates are (case, transcript response, judge check, judge's verdict)
tuples from the latest run. For each one the operator answers:
  y = agree with the judge's verdict (it becomes the golden label)
  n = the judge is wrong (the flipped verdict becomes the golden label)
  s = skip   q = quit (already-certified items are kept)

Accepted items are appended to tests/golden/golden.json with
labeled_by="operator" and response_source="transcript". Disagreement
candidates — judge failed a check whose deterministic sibling passed —
sort first, because they are the most informative to label.
"""
import argparse
import json
import re
from pathlib import Path

from checks import CHECKS
from judge import parse_rubric

REPO_ROOT = Path(__file__).resolve().parent.parent

# deterministic sibling whose pass makes a judge fail "interesting"
SIBLINGS = {
    "position-correct": "position-stated",
    "assumptions-specific": "assumptions-present",
    "trivial-reason": "trivial-marker",
}

# per-check evidence extractors: pull only the part of the response the
# criterion actually judges, so the operator sees EXPECTED vs RECEIVED
# instead of hunting through the full text (v shows it on demand)
_EVIDENCE = {
    "position-correct": re.compile(
        r"^.*(operating from|position on the (matrix|continuum)).*$", re.I | re.M),
    "assumptions-specific": re.compile(
        r"<assumptions>.*?</assumptions>|^#{1,6}\s[^\n]*assumption[^\n]*\n(?:[-*][^\n]*\n?)*",
        re.I | re.S | re.M),
    "trivial-reason": re.compile(
        r"^.*trivial\s*[—–-]\s*matrix not applied.*(?:\n(?!\n).*)*", re.I | re.M),
    "verify-sections-present": re.compile(
        r"^#{1,6}\s[^\n]*(confident about|double.check)[^\n]*\n(?:[-*][^\n]*\n?)*",
        re.I | re.M),
}


def evidence(check, response):
    pattern = _EVIDENCE.get(check)
    if pattern is None:
        return response   # no extractor: the whole response is the evidence
    m = pattern.search(response)
    return m.group(0).strip() if m else "(no matching evidence found in the response)"


def expectation(check, case):
    if check == "position-correct":
        return f"a stated position matching quadrant: {case.get('quadrant', '?')}"
    return f"quadrant {case.get('quadrant', '?')}; see criterion above"


def latest_run(results_dir):
    runs = sorted(Path(results_dir).glob("*.json"))
    if not runs:
        raise SystemExit(f"no run files in {results_dir} - run the eval first")
    return json.loads(runs[-1].read_text())


def _disagreement(check, verdict):
    sibling = SIBLINGS.get(check)
    return (not verdict[check]) and sibling in verdict and verdict[sibling]


def candidates(results, transcripts_root, golden):
    seen = {(g["case_id"], g["check"], g["response"]) for g in golden}
    out = []
    for cases in results["arms"].values():
        for case_id, r in cases.items():
            for i, verdict in enumerate(r.get("sample_verdicts", [])):
                response = (Path(transcripts_root) / r["transcripts"][i]).read_text()
                for check, passed in verdict.items():
                    if check in CHECKS:   # deterministic checks need no golden labels
                        continue
                    if (case_id, check, response) in seen:
                        continue
                    out.append({
                        "case_id": case_id,
                        "check": check,
                        "response": response,
                        "proposed_label": "pass" if passed else "fail",
                        "disagreement": _disagreement(check, verdict),
                    })
    return sorted(out, key=lambda c: not c["disagreement"])


def _next_id(golden):
    taken = [int(g["id"][1:]) for g in golden if g.get("id", "").startswith("g")]
    return max(taken, default=0) + 1


def label_loop(cands, golden_path, cases_by_id, ask=input, out=print):
    golden = json.loads(golden_path.read_text()) if golden_path.exists() else []
    rubric = parse_rubric()
    counter = _next_id(golden)
    added = 0
    for k, c in enumerate(cands):
        out(f"\n[{k + 1}/{len(cands)}] {c['case_id']} · {c['check']}"
            f" · judge says: {c['proposed_label']}"
            + ("  (disagrees with deterministic sibling)" if c.get("disagreement") else ""))
        out("PROMPT: " + " // ".join(cases_by_id[c["case_id"]]["turns"]))
        out("CRITERION: " + rubric["criteria"].get(c["check"], "(unknown check)"))
        out("EXPECTED: " + expectation(c["check"], cases_by_id[c["case_id"]]))
        out("RECEIVED: " + evidence(c["check"], c["response"]))
        while True:
            answer = ask("[y]=judge is right  [n]=judge is wrong  [s]=skip  "
                         "[v]=view full response  [q]=quit > ").strip().lower()
            if answer == "v":
                out("FULL RESPONSE:\n" + c["response"])
                continue
            break
        if answer == "q":
            break
        if answer not in ("y", "n"):
            continue
        label = c["proposed_label"] if answer == "y" else (
            "fail" if c["proposed_label"] == "pass" else "pass")
        golden.append({
            "id": f"g{counter + added:03d}",
            "case_id": c["case_id"],
            "check": c["check"],
            "response": c["response"],
            "label": label,
            "why": "operator-certified via labeler"
                   + ("; operator overruled judge" if answer == "n" else ""),
            "response_source": "transcript",
            "labeled_by": "operator",
        })
        added += 1
        # save immediately: a Ctrl-C or crash never loses a decision
        golden_path.write_text(json.dumps(golden, indent=2, ensure_ascii=False) + "\n")
    golden_path.write_text(json.dumps(golden, indent=2, ensure_ascii=False) + "\n")
    return added


def main():
    ap = argparse.ArgumentParser(description="Certify judge verdicts into the golden set.")
    ap.add_argument("--results", default=REPO_ROOT / "results")
    ap.add_argument("--transcripts", default=REPO_ROOT / "transcripts")
    ap.add_argument("--cases", default=REPO_ROOT / "tests" / "cases")
    ap.add_argument("--golden", default=REPO_ROOT / "tests" / "golden" / "golden.json")
    args = ap.parse_args()

    from runner import load_cases
    cases_by_id = {c["id"]: c for c in load_cases(args.cases)}
    golden_path = Path(args.golden)
    golden = json.loads(golden_path.read_text()) if golden_path.exists() else []

    cands = candidates(latest_run(args.results), args.transcripts, golden)
    if not cands:
        print("no unlabeled candidates in the latest run")
        return
    added = label_loop(cands, golden_path, cases_by_id)
    print(f"\nadded {added} operator-labeled items to {golden_path}")


if __name__ == "__main__":
    main()

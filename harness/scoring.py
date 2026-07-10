"""Score rollups, run history, rolling baseline, soft gate.
Spec: TESTING-METHODOLOGY.md section 4.

Rollup hierarchy: check pass-fraction -> case score -> dimension score ->
suite score. Suite and gate use the gating set only; lift uses all cases.
"""
import json
from pathlib import Path

from checks import DIMENSIONS

GATE_EPS_SUITE = 0.05
GATE_EPS_DIMENSION = 0.10
BASELINE_RUNS = 3


def _gating(arm_results):
    return {cid: r for cid, r in arm_results.items() if r.get("status") == "gating"}


def dimension_scores(arm_results, gating_only=True):
    cases = _gating(arm_results) if gating_only else arm_results
    by_dim = {}
    for result in cases.values():
        for check_id, fraction in result["checks"].items():
            by_dim.setdefault(DIMENSIONS[check_id], []).append(fraction)
    return {dim: sum(f) / len(f) for dim, f in sorted(by_dim.items())}


def suite_score(arm_results):
    scores = [r["score"] for r in _gating(arm_results).values()]
    return sum(scores) / len(scores) if scores else None


def lift(results):
    def mean_all(arm):
        scores = [r["score"] for r in results["arms"][arm].values()]
        return sum(scores) / len(scores)
    return mean_all("B") - mean_all("A")


def summarize(results):
    arm_b = results["arms"]["B"]
    return {
        "suite": suite_score(arm_b),
        "dimensions": dimension_scores(arm_b, gating_only=True),
        "dimensions_all": dimension_scores(arm_b, gating_only=False),
        "lift": lift(results),
    }


def load_history(path):
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def append_history(path, entry):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def baseline(history, last=BASELINE_RUNS, runtime=None):
    # scores from different runtimes (api vs cli) are never comparable
    if runtime is not None:
        history = [h for h in history if h.get("runtime") == runtime]
    if not history:
        return None
    window = history[-last:]
    dims = {}
    for run in window:
        for dim, score in run.get("dimensions", {}).items():
            dims.setdefault(dim, []).append(score)
    return {
        "suite": sum(r["suite"] for r in window) / len(window),
        "dimensions": {d: sum(s) / len(s) for d, s in dims.items()},
    }


def evaluate_gate(summary, base):
    if base is None:
        return True, []
    reasons = []
    if summary["suite"] < base["suite"] - GATE_EPS_SUITE:
        reasons.append(
            f"suite score {summary['suite']:.2f} fell more than "
            f"{GATE_EPS_SUITE} below baseline {base['suite']:.2f}")
    for dim, score in summary["dimensions"].items():
        if dim not in base["dimensions"]:
            continue   # new dimension: no baseline yet, cannot regress
        if score < base["dimensions"][dim] - GATE_EPS_DIMENSION:
            reasons.append(
                f"dimension {dim} score {score:.2f} fell more than "
                f"{GATE_EPS_DIMENSION} below baseline {base['dimensions'][dim]:.2f}")
    return not reasons, reasons

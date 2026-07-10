"""Report renderer tests: results.json + history -> self-contained static HTML.

Design contract comes from samples/report.html (operator-approved): plain
language, no trial jargon, click-to-expand deltas, no backend processing.
"""
from report import render_report

RESULTS = {
    "arms": {
        "A": {"c1": {"checks": {"position-stated": 0.0}, "score": 0.0, "status": "gating"},
              "c2": {"checks": {"trivial-marker": 1.0}, "score": 1.0, "status": "xfail"}},
        "B": {"c1": {"checks": {"position-stated": 1.0}, "score": 1.0, "status": "gating"},
              "c2": {"checks": {"trivial-marker": 0.5}, "score": 0.5, "status": "xfail"}},
    },
    "n": 1, "model": "haiku", "runtime": "api",
    "judge_calibration": 0.97,
    "instructions_sha": "abc1234",
    "timestamp": "2026-07-10T22:21:11Z",
    "summary": {"suite": 1.0,
                "dimensions": {"positioning": 1.0},
                "dimensions_all": {"positioning": 1.0, "trivial": 0.5},
                "lift": 0.75},
    "gate": {"ok": True, "reasons": [], "baseline": {"suite": 0.9, "dimensions": {"positioning": 0.9}}},
}

HISTORY = [
    {"run_id": "r1", "sha": "old1111", "timestamp": "2026-07-09", "suite": 0.6,
     "dimensions": {"positioning": 0.9}, "lift": 0.4, "gate": True},
    {"run_id": "r2", "sha": "abc1234", "timestamp": "2026-07-10", "suite": 1.0,
     "dimensions": {"positioning": 1.0}, "lift": 0.75, "gate": True},
]

PREV_RESULTS = {
    "arms": {"B": {"c1": {"checks": {"position-stated": 0.0}, "score": 0.0, "status": "gating"}}},
}


def html():
    return render_report(RESULTS, HISTORY, prev_results=PREV_RESULTS,
                         compare_url="https://example.com/compare/old1111..abc1234")


def test_report_contains_no_trial_jargon():
    page = html()
    assert "Arm A" not in page and "Arm B" not in page
    assert "xfail" not in page
    assert "in development" in page          # the plain-language replacement
    assert "Without instructions" in page and "With instructions" in page


def test_report_shows_gate_and_headline_numbers():
    page = html()
    assert "No regressions" in page
    assert "0.75" in page                    # improvement (lift)
    assert "abc1234" in page                 # instructions version


def test_report_delta_details_show_moved_checks_and_compare_link():
    page = html()
    assert "<details" in page
    assert "position-stated" in page         # the check that moved 0.0 -> 1.0
    assert "https://example.com/compare/old1111..abc1234" in page


def test_report_history_table_lists_runs():
    page = html()
    assert "old1111" in page
    assert page.count("<tr>") >= 4           # headers + dimension/case/history rows


def test_report_survives_first_run_without_prev():
    first = dict(RESULTS, gate={"ok": True, "reasons": [], "baseline": None})
    page = render_report(first, HISTORY[:1], prev_results=None, compare_url=None)
    assert "No regressions" in page or "first run" in page.lower()

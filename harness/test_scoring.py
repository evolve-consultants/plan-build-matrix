"""Scoring, history, baseline, gate tests. Spec: TESTING-METHODOLOGY.md section 4."""
import json

import pytest
from scoring import (
    append_history,
    baseline,
    dimension_scores,
    evaluate_gate,
    lift,
    load_history,
    suite_score,
    summarize,
)

# arm result shape produced by runner.run_suite: case id -> {checks, score, status}
ARM_B = {
    "c1": {"checks": {"1a": 1.0, "2a": 0.8}, "score": 0.9, "status": "gating"},
    "c2": {"checks": {"1a": 0.6, "3a": 1.0}, "score": 0.8, "status": "gating"},
    "c3": {"checks": {"9a": 0.4, "9b": 0.4}, "score": 0.4, "status": "xfail"},
}
ARM_A = {
    "c1": {"checks": {"1a": 0.0, "2a": 0.0}, "score": 0.0, "status": "gating"},
    "c2": {"checks": {"1a": 0.2, "3a": 0.0}, "score": 0.1, "status": "gating"},
    "c3": {"checks": {"9a": 0.0, "9b": 1.0}, "score": 0.5, "status": "xfail"},
}
RESULTS = {"arms": {"A": ARM_A, "B": ARM_B}, "n": 5, "model": "haiku"}


# --- rollups -----------------------------------------------------------------

def test_dimension_scores_gating_only():
    dims = dimension_scores(ARM_B, gating_only=True)
    assert dims == {"1": pytest.approx(0.8), "2": pytest.approx(0.8), "3": pytest.approx(1.0)}


def test_dimension_scores_including_xfail():
    dims = dimension_scores(ARM_B, gating_only=False)
    assert dims["9"] == pytest.approx(0.4)


def test_suite_score_is_mean_of_gating_case_scores():
    assert suite_score(ARM_B) == pytest.approx((0.9 + 0.8) / 2)


def test_lift_is_b_minus_a_over_all_cases():
    b_all = (0.9 + 0.8 + 0.4) / 3
    a_all = (0.0 + 0.1 + 0.5) / 3
    assert lift(RESULTS) == pytest.approx(b_all - a_all)


def test_summarize_bundles_suite_dimensions_lift():
    s = summarize(RESULTS)
    assert s["suite"] == pytest.approx(0.85)
    assert s["dimensions"]["3"] == pytest.approx(1.0)
    assert s["lift"] == pytest.approx(0.5)


# --- history + baseline --------------------------------------------------------

def test_history_round_trip(tmp_path):
    path = tmp_path / "history.jsonl"
    append_history(path, {"suite": 0.8, "dimensions": {"1": 0.9}})
    append_history(path, {"suite": 0.9, "dimensions": {"1": 1.0}})
    assert [h["suite"] for h in load_history(path)] == [0.8, 0.9]


def test_load_history_missing_file_is_empty(tmp_path):
    assert load_history(tmp_path / "nope.jsonl") == []


def test_baseline_means_last_k_runs():
    history = [
        {"suite": 0.70, "dimensions": {"1": 0.7}},
        {"suite": 0.80, "dimensions": {"1": 0.8}},
        {"suite": 0.85, "dimensions": {"1": 0.9}},
        {"suite": 0.90, "dimensions": {"1": 1.0}},
    ]
    base = baseline(history, last=3)
    assert base["suite"] == pytest.approx((0.80 + 0.85 + 0.90) / 3)
    assert base["dimensions"]["1"] == pytest.approx(0.9)


def test_baseline_empty_history_is_none():
    assert baseline([]) is None


# --- gate ----------------------------------------------------------------------

def test_gate_passes_without_baseline():
    ok, reasons = evaluate_gate({"suite": 0.5, "dimensions": {}}, None)
    assert ok is True


def test_gate_passes_within_thresholds():
    summary = {"suite": 0.82, "dimensions": {"1": 0.85}}
    base = {"suite": 0.85, "dimensions": {"1": 0.90}}
    ok, reasons = evaluate_gate(summary, base)   # drops of 0.03 / 0.05: within eps
    assert ok is True
    assert reasons == []

def test_gate_fails_on_suite_regression():
    summary = {"suite": 0.79, "dimensions": {}}
    base = {"suite": 0.85, "dimensions": {}}
    ok, reasons = evaluate_gate(summary, base)
    assert ok is False
    assert "suite" in reasons[0]


def test_gate_fails_on_dimension_regression():
    summary = {"suite": 0.85, "dimensions": {"2": 0.70}}
    base = {"suite": 0.85, "dimensions": {"2": 0.85}}
    ok, reasons = evaluate_gate(summary, base)
    assert ok is False
    assert "dimension 2" in reasons[0]


def test_gate_ignores_dimension_new_in_this_run():
    summary = {"suite": 0.85, "dimensions": {"7": 0.10}}
    base = {"suite": 0.85, "dimensions": {}}   # dimension 7 has no baseline yet
    ok, _ = evaluate_gate(summary, base)
    assert ok is True

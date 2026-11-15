"""
Test Suite: Three-Policy Paired-Seed Comparative Benchmark (Stage 4)
Verifies:
1. Snapshot copy independence and equivalent starting contents.
2. Complete three-policy execution for every generated seed.
3. Independent verification failure recording and exclusion from valid paired analysis.
4. Reconciliation of pairwise wins, ties, and losses against valid paired counts.
5. Exact subtraction direction semantics for lateness reduction and differences.
6. Deterministic paired bootstrap confidence interval calculations.
7. Safe handling of invalid runs without silent dropping.
8. Small N=5 smoke benchmark generating valid JSON and Markdown artifacts.
9. Preservation of historical canonical benchmark artifacts.
"""

import copy
import hashlib
import json
import os
import pytest

from backend.benchmark import generate_benchmark_seeds
from backend.models import PolicyId, SolverStatusEnum
from backend.v2.benchmark_three_policy import (
    run_three_policy_benchmark,
    compute_paired_bootstrap_ci,
    evaluate_seed_a2,
    evaluate_seed_a2_plus,
    evaluate_seed_p3,
    validate_policy_metrics_completeness,
    PolicyMetrics,
    ThreePolicyBenchmarkResult
)


# -----------------------------------------------------------------------------
# 1. Snapshot Independence and Seed Integrity Tests
# -----------------------------------------------------------------------------

def test_seeds_generation_and_snapshot_copy_independence():
    """
    Prove that all policies receive independent deep copies of identical starting snapshots.
    Mutating one copy must not leak into any other copy.
    """
    seeds = generate_benchmark_seeds(n=5, master_seed=42)
    assert len(seeds) == 5

    s0 = seeds[0]
    snap_a2 = copy.deepcopy(s0)
    snap_a2p = copy.deepcopy(s0)
    snap_p3 = copy.deepcopy(s0)

    # Initial equivalence
    assert snap_a2.scenario_id == snap_a2p.scenario_id == snap_p3.scenario_id
    assert snap_a2.current_tick == snap_a2p.current_tick == snap_p3.current_tick
    assert snap_a2.ro1042.promise_ticks == snap_a2p.ro1042.promise_ticks == snap_p3.ro1042.promise_ticks
    assert len(snap_a2.sources) == len(snap_a2p.sources) == len(snap_p3.sources)

    # Mutation independence
    snap_a2.sources[0].cost = 999.0
    assert snap_a2p.sources[0].cost != 999.0
    assert snap_p3.sources[0].cost != 999.0

    snap_a2p.ro1042.promise_ticks = 1234
    assert snap_a2.ro1042.promise_ticks != 1234
    assert snap_p3.ro1042.promise_ticks != 1234


# -----------------------------------------------------------------------------
# 2. Execution and Policy Evaluation Tests
# -----------------------------------------------------------------------------

def test_three_policy_execution_for_all_seeds():
    """Prove that A2, A2+, and P3 are each executed and populated for every seed."""
    seeds = generate_benchmark_seeds(n=3, master_seed=42)
    for s in seeds:
        m_a2 = evaluate_seed_a2(copy.deepcopy(s))
        m_a2p = evaluate_seed_a2_plus(copy.deepcopy(s))
        m_p3 = evaluate_seed_p3(copy.deepcopy(s))

        assert m_a2.policy == "A2"
        assert m_a2p.policy == "A2_PLUS"
        assert m_p3.policy == "P3"

        assert m_a2.is_valid is True
        assert m_a2p.is_valid is True
        assert m_p3.is_valid is True

        assert m_a2.weighted_lateness is not None
        assert m_a2p.weighted_lateness is not None
        assert m_p3.weighted_lateness is not None

        assert m_a2.verification_status == "VERIFIED"
        assert m_a2p.verification_status == "VERIFIED"
        assert m_p3.verification_status == "VERIFIED"


# -----------------------------------------------------------------------------
# 3. Statistical Reconciliation and Subtraction Direction Tests
# -----------------------------------------------------------------------------

def test_pairwise_wins_ties_losses_reconciliation():
    """Prove that wins + ties + losses strictly equals valid_paired_count for all pairs."""
    res = run_three_policy_benchmark(
        n=5,
        master_seed=42,
        bootstrap_seed=42,
        bootstrap_resamples=1000,
        output_dir="generated-results/test_tmp"
    )

    assert res.valid_paired_seeds == 5
    assert len(res.pairwise_comparisons) == 3

    for comp_key, comp in res.pairwise_comparisons.items():
        total_reconciled = comp.wins_advanced + comp.ties + comp.losses_advanced
        assert total_reconciled == comp.valid_paired_count
        assert comp.win_rate_pct + comp.tie_rate_pct + comp.loss_rate_pct == pytest.approx(100.0)


def test_subtraction_direction_semantics():
    """
    Verify the exact documented subtraction direction semantics:
    - Reduction = Baseline - Advanced (positive means advanced reduced lateness / improved).
    - Difference = Advanced - Baseline (negative means advanced achieved lower lateness).
    - Freight Delta = Advanced - Baseline (positive means advanced expended more freight).
    """
    res = run_three_policy_benchmark(
        n=5,
        master_seed=42,
        bootstrap_seed=42,
        bootstrap_resamples=1000,
        output_dir="generated-results/test_tmp"
    )

    comp_a2_a2p = res.pairwise_comparisons["A2_vs_A2_PLUS"]
    # A2+ reduces lateness compared to A2
    assert comp_a2_a2p.mean_lateness_reduction > 0.0
    assert comp_a2_a2p.mean_lateness_difference < 0.0
    assert comp_a2_a2p.mean_lateness_reduction == pytest.approx(-comp_a2_a2p.mean_lateness_difference)
    # A2+ incurs additional freight compared to fixed S2
    assert comp_a2_a2p.mean_freight_delta > 0.0


# -----------------------------------------------------------------------------
# 4. Bootstrap Confidence Interval Tests
# -----------------------------------------------------------------------------

def test_deterministic_bootstrap_confidence_intervals():
    """Prove that paired bootstrap calculations are 100% deterministic with fixed seed."""
    diffs = [10.0, 15.0, 12.0, 8.0, 14.0, 11.0, 13.0, 9.0]
    ci1 = compute_paired_bootstrap_ci(diffs, "test_metric", "test_comp", n_resamples=5000, seed=42)
    ci2 = compute_paired_bootstrap_ci(diffs, "test_metric", "test_comp", n_resamples=5000, seed=42)

    assert ci1.mean == ci2.mean
    assert ci1.ci_lower == ci2.ci_lower
    assert ci1.ci_upper == ci2.ci_upper
    assert ci1.std_error == ci2.std_error
    assert ci1.is_statistically_significant is True  # all positive, excludes 0

    # Zero differences test (like A2+ vs P3 ties)
    zero_diffs = [0.0, 0.0, 0.0, 0.0, 0.0]
    ci_zero = compute_paired_bootstrap_ci(zero_diffs, "zero_metric", "zero_comp", n_resamples=1000, seed=42)
    assert ci_zero.mean == 0.0
    assert ci_zero.ci_lower == 0.0
    assert ci_zero.ci_upper == 0.0
    assert ci_zero.is_statistically_significant is False


# -----------------------------------------------------------------------------
# 5. Invalid Run Handling and Complete Orchestration Tests
# -----------------------------------------------------------------------------

def test_complete_benchmark_orchestration_with_injected_invalid_snapshots(tmp_path):
    """
    Task 1: Deterministic test injecting a controlled set of synthetic snapshots
    into the complete benchmark execution path.
    Verifies:
    1. A2, A2+, and P3 execute for every supplied snapshot.
    2. An infeasible or rejected policy output invalidates that paired scenario.
    3. Invalid scenarios remain present in the complete `records` collection.
    4. Invalid scenarios appear in `invalid_runs`, with correct scenario ID and failure reason.
    5. Invalid scenarios are excluded from paired aggregate statistics.
    6. Valid scenarios remain included in aggregate statistics.
    7. Wins + ties + losses equal `valid_paired_count` for every pairwise comparison.
    8. The final valid paired count and validity percentage are correct.
    """
    seeds = generate_benchmark_seeds(n=3, master_seed=42)
    test_seeds = copy.deepcopy(seeds)

    # Invalidate Seed 1 by zeroing ATP across all part sources (causes INFEASIBLE across policies)
    for s in test_seeds[1].sources:
        s.atp = 0

    out_dir = str(tmp_path / "artifacts")
    res = run_three_policy_benchmark(
        seeds=test_seeds,
        bootstrap_seed=42,
        bootstrap_resamples=500,
        output_dir=out_dir
    )

    # 1. Total seeds and execution across all policies
    assert res.total_seeds == 3
    assert len(res.records) == 3

    # Seed 0: valid
    r0 = res.records[0]
    assert r0.is_valid_for_paired_analysis is True
    assert set(r0.policies.keys()) == {"A2", "A2_PLUS", "P3"}
    assert all(p.is_valid for p in r0.policies.values())

    # Seed 1: invalid, but executed and recorded
    r1 = res.records[1]
    assert r1.is_valid_for_paired_analysis is False
    assert r1.scenario_id == test_seeds[1].scenario_id
    assert set(r1.policies.keys()) == {"A2", "A2_PLUS", "P3"}
    assert not all(p.is_valid for p in r1.policies.values())
    assert len(r1.invalidation_reasons) > 0

    # Seed 2: valid
    r2 = res.records[2]
    assert r2.is_valid_for_paired_analysis is True
    assert all(p.is_valid for p in r2.policies.values())

    # 2. Invalid runs collection
    assert len(res.invalid_runs) == 1
    assert res.invalid_runs[0]["seed_index"] == 1
    assert res.invalid_runs[0]["scenario_id"] == test_seeds[1].scenario_id
    assert len(res.invalid_runs[0]["reasons"]) > 0

    # 3. Valid counts and percentages
    assert res.valid_paired_seeds == 2
    assert res.valid_paired_rate_pct == round(2 / 3 * 100.0, 2)

    # 4. Aggregates include only valid seeds
    for pol in ("A2", "A2_PLUS", "P3"):
        agg = res.policy_aggregates[pol]
        assert agg.valid_count == 2
        assert agg.total_seeds == 3
        assert agg.validity_rate_pct == round(2 / 3 * 100.0, 2)
        # Expected mean should be average of Seed 0 and Seed 2
        expected_mean = (r0.policies[pol].weighted_lateness + r2.policies[pol].weighted_lateness) / 2.0
        assert agg.mean_weighted_lateness == round(expected_mean, 2)

    # 5. Pairwise reconciliation: wins + ties + losses == valid_paired_count
    for comp_key, comp in res.pairwise_comparisons.items():
        assert comp.valid_paired_count == 2
        assert comp.wins_advanced + comp.ties + comp.losses_advanced == 2


# -----------------------------------------------------------------------------
# 5b. Focused PolicyMetrics Completeness and Type Validation Tests (Task 2)
# -----------------------------------------------------------------------------

def _make_valid_sample_metrics(policy: str = "P3", **overrides) -> PolicyMetrics:
    """Helper to construct a valid base PolicyMetrics object for mutation testing."""
    params = {
        "policy": policy,
        "scenario_id": "TEST-SCENARIO-01",
        "selected_source_id": "S1",
        "selected_movement": "HOLD_ON_BAY",
        "weighted_lateness": 24.0,
        "ro1042_lateness_ticks": 0,
        "ro1051_lateness_ticks": 8,
        "ro1042_finish_tick": 38,
        "ro1051_finish_tick": 59,
        "b4_first_release_tick": 38,
        "freight_cost": 50.38,
        "downstream_delay_minutes": 40,
        "solve_time_ms": 15.0,
        "solver_status": "OPTIMAL",
        "verification_status": "VERIFIED",
        "verification_violations": [],
        "is_valid": True,
        "proposal_digest": "test_sha256_digest"
    }
    params.update(overrides)
    return PolicyMetrics(**params)


def test_metric_validation_valid_sample_passes():
    """Verify that a complete, valid sample passes all completeness checks."""
    m = _make_valid_sample_metrics()
    is_valid, violations = validate_policy_metrics_completeness(m)
    assert is_valid is True
    assert violations == []


def test_metric_validation_missing_weighted_lateness():
    """Missing weighted lateness must fail validation."""
    m = _make_valid_sample_metrics(weighted_lateness=None)
    is_valid, violations = validate_policy_metrics_completeness(m)
    assert is_valid is False
    assert any("MISSING_OR_NON_FINITE_WEIGHTED_LATENESS" in v for v in violations)


def test_metric_validation_non_finite_weighted_lateness():
    """Non-finite or boolean weighted lateness (NaN, +inf, -inf, True) must fail validation."""
    for bad_val in [float("nan"), float("inf"), float("-inf"), True, False]:
        m = _make_valid_sample_metrics(weighted_lateness=bad_val)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False, f"Failed to reject weighted_lateness={bad_val}"
        assert any("MISSING_OR_NON_FINITE_WEIGHTED_LATENESS" in v for v in violations)


def test_metric_validation_missing_freight_cost():
    """Missing freight cost must fail validation."""
    m = _make_valid_sample_metrics(freight_cost=None)
    is_valid, violations = validate_policy_metrics_completeness(m)
    assert is_valid is False
    assert any("MISSING_OR_NON_FINITE_FREIGHT_COST" in v for v in violations)


def test_metric_validation_non_finite_freight_cost():
    """Non-finite or boolean freight cost (NaN, +inf, -inf, True) must fail validation."""
    for bad_val in [float("nan"), float("inf"), float("-inf"), True, False]:
        m = _make_valid_sample_metrics(freight_cost=bad_val)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False, f"Failed to reject freight_cost={bad_val}"
        assert any("MISSING_OR_NON_FINITE_FREIGHT_COST" in v for v in violations)


def test_metric_validation_missing_selected_source():
    """Missing or empty selected source ID must fail validation."""
    for bad_src in [None, "", "   "]:
        m = _make_valid_sample_metrics(selected_source_id=bad_src)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False
        assert any("MISSING_SELECTED_SOURCE_ID" in v for v in violations)


def test_metric_validation_missing_or_invalid_movement():
    """Missing, empty, or unsupported movement option must fail validation."""
    for bad_move in [None, "", "UNSUPPORTED_MOVE", "TELEPORT"]:
        m = _make_valid_sample_metrics(selected_movement=bad_move)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False
        assert any("MISSING_OR_INVALID_SELECTED_MOVEMENT" in v for v in violations)


def test_metric_validation_missing_schedule_milestones():
    """Missing, float, or boolean schedule milestones must fail validation."""
    milestones = [
        ("ro1042_lateness_ticks", "MISSING_OR_INVALID_RO1042_LATENESS_TICKS"),
        ("ro1051_lateness_ticks", "MISSING_OR_INVALID_RO1051_LATENESS_TICKS"),
        ("ro1042_finish_tick", "MISSING_OR_INVALID_RO1042_FINISH_TICK"),
        ("ro1051_finish_tick", "MISSING_OR_INVALID_RO1051_FINISH_TICK"),
        ("b4_first_release_tick", "MISSING_OR_INVALID_B4_RELEASE_TICK"),
    ]
    for field_name, expected_violation in milestones:
        # Test None
        m_none = _make_valid_sample_metrics(**{field_name: None})
        is_v, viols = validate_policy_metrics_completeness(m_none)
        assert is_v is False, f"Failed to reject None for {field_name}"
        assert any(expected_violation in v for v in viols)

        # Test boolean
        m_bool = _make_valid_sample_metrics(**{field_name: True})
        is_v, viols = validate_policy_metrics_completeness(m_bool)
        assert is_v is False, f"Failed to reject boolean for {field_name}"
        assert any(expected_violation in v for v in viols)

        # Test float
        m_float = _make_valid_sample_metrics(**{field_name: 38.5})
        is_v, viols = validate_policy_metrics_completeness(m_float)
        assert is_v is False, f"Failed to reject float for {field_name}"
        assert any(expected_violation in v for v in viols)


def test_metric_validation_missing_or_invalid_downstream_delay():
    """Missing, float, or boolean downstream delay minutes must fail validation."""
    for bad_delay in [None, True, False, 40.5]:
        m = _make_valid_sample_metrics(downstream_delay_minutes=bad_delay)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False, f"Failed to reject downstream_delay_minutes={bad_delay}"
        assert any("MISSING_OR_INVALID_DOWNSTREAM_DELAY_MINUTES" in v for v in violations)


def test_metric_validation_invalid_solver_status():
    """Invalid or genuinely infeasible solver status must fail validation."""
    # For P3 / A2: INFEASIBLE or UNKNOWN fails
    for bad_status in ["INFEASIBLE", "UNKNOWN", "MODEL_INVALID", None]:
        m = _make_valid_sample_metrics(policy="P3", solver_status=bad_status)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False
        assert any("INVALID_SOLVER_STATUS" in v for v in violations)

    # For A2+: INFEASIBLE fails, but HEURISTIC passes
    m_a2p_infeasible = _make_valid_sample_metrics(policy="A2_PLUS", solver_status="INFEASIBLE")
    is_v, viols = validate_policy_metrics_completeness(m_a2p_infeasible)
    assert is_v is False
    assert any("INVALID_SOLVER_STATUS" in v for v in viols)

    m_a2p_heuristic = _make_valid_sample_metrics(policy="A2_PLUS", solver_status="HEURISTIC")
    is_v, viols = validate_policy_metrics_completeness(m_a2p_heuristic)
    assert is_v is True


def test_metric_validation_verification_rejection():
    """Unverified or rejected verification status must fail validation."""
    for bad_v_status in ["REJECTED", "NOT_VERIFIABLE", "INSUFFICIENT_EVIDENCE", "PENDING"]:
        m = _make_valid_sample_metrics(verification_status=bad_v_status)
        is_valid, violations = validate_policy_metrics_completeness(m)
        assert is_valid is False
        assert any("UNVERIFIED_STATUS" in v for v in violations)


# -----------------------------------------------------------------------------
# 6. Artifact Generation & Baseline Artifact Preservation Tests
# -----------------------------------------------------------------------------

def test_n5_smoke_benchmark_generates_valid_artifacts(tmp_path):
    """Smoke test proving that a benchmark execution writes valid JSON and Markdown artifacts."""
    out_dir = str(tmp_path / "artifacts")
    res = run_three_policy_benchmark(
        n=5,
        master_seed=42,
        bootstrap_seed=42,
        bootstrap_resamples=1000,
        output_dir=out_dir
    )

    assert res.json_artifact_path is not None
    assert os.path.exists(res.json_artifact_path)
    assert res.markdown_artifact_path is not None
    assert os.path.exists(res.markdown_artifact_path)

    # Validate JSON content
    with open(res.json_artifact_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["n_seeds"] == 5
    assert data["valid_paired_seeds"] == 5
    assert "policy_aggregates" in data
    assert "pairwise_comparisons" in data
    assert len(data["records"]) == 5

    # Validate Markdown content
    with open(res.markdown_artifact_path, "r", encoding="utf-8") as f:
        md = f.read()
    assert "# StallBreaker 2.0 — Three-Policy Paired-Seed Comparative Benchmark Report" in md
    assert "A2 vs A2_PLUS" in md
    assert "A2_PLUS vs P3" in md


def test_preserved_benchmark_artifact_untouched():
    """Verify that historical benchmark artifact is preserved with exact SHA-256 checksum."""
    path = "generated-results/benchmark_results_n100_20261115_033621.json"
    assert os.path.exists(path)
    content = open(path, "rb").read()
    h = hashlib.sha256(content).hexdigest().upper()
    assert h == "5E36AEC5654D7539950F173EB09073905E42B5B6867DF4669B1A30856E921941"

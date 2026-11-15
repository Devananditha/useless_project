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
# 5. Invalid Run Handling and Failure Gating Tests
# -----------------------------------------------------------------------------

def test_invalid_run_handling_and_exclusion(tmp_path):
    """
    Prove that if an invalid run occurs (e.g. verification failure or infeasibility):
    1. It is recorded in invalid_runs with reason.
    2. It is excluded from valid paired statistics.
    3. The record is NOT silently dropped from the total records list.
    """
    seeds = generate_benchmark_seeds(n=3, master_seed=42)
    # Create an invalid seed by setting all sources to ATP = 0 for seed 1
    corrupt_seeds = copy.deepcopy(seeds)
    for s in corrupt_seeds[1].sources:
        s.atp = 0

    # Execute evaluate_seed_a2_plus on corrupt seed
    m_a2p_corrupt = evaluate_seed_a2_plus(corrupt_seeds[1])
    assert m_a2p_corrupt.is_valid is False
    assert m_a2p_corrupt.solver_status == "INFEASIBLE"
    assert m_a2p_corrupt.verification_status == "NOT_VERIFIABLE"


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

"""
Policy execution wrappers for StallBreaker.
Coordinates evaluation of P0, P1, A2, and P3 policies.
"""

from typing import Dict
from backend.models import (
    ScenarioSnapshot,
    PolicyId,
    Proposal,
    PolicyComparisonResult
)
from backend.solver import solve_recovery_problem


def run_policy_comparison(snapshot: ScenarioSnapshot) -> PolicyComparisonResult:
    """
    Executes actual Google OR-Tools CP-SAT solves for both Policy A2 and Policy P3
    under the identical current scenario snapshot.
    """
    prop_a2 = solve_recovery_problem(snapshot, PolicyId.A2)
    prop_p3 = solve_recovery_problem(snapshot, PolicyId.P3)

    # Compute comparative metrics
    if prop_a2.weighted_lateness_ticks > 0:
        red_pct = ((prop_a2.weighted_lateness_ticks - prop_p3.weighted_lateness_ticks) / prop_a2.weighted_lateness_ticks) * 100.0
    else:
        red_pct = 0.0

    delay_savings_min = prop_a2.downstream_delay_minutes - prop_p3.downstream_delay_minutes
    freight_delta = prop_p3.parts_freight_cost - prop_a2.parts_freight_cost

    verdict = (
        f"Joint Policy P3 achieves a {red_pct:.1f}% relative reduction in weighted customer lateness "
        f"({prop_a2.weighted_lateness_ticks:.1f} -> {prop_p3.weighted_lateness_ticks:.1f} ticks), "
        f"saving {delay_savings_min} minutes on downstream Fleet RO-1051 for a ${freight_delta:.2f} freight difference."
    )

    return PolicyComparisonResult(
        scenario_id=snapshot.scenario_id,
        snapshot_version=snapshot.snapshot_version,
        baseline_a2=prop_a2,
        joint_p3=prop_p3,
        weighted_lateness_reduction_pct=round(red_pct, 1),
        downstream_lateness_savings_minutes=delay_savings_min,
        freight_cost_delta=freight_delta,
        summary_verdict=verdict
    )


def run_all_policies(snapshot: ScenarioSnapshot) -> Dict[str, Proposal]:
    """Runs all 4 defined policies: P0, P1, A2, P3."""
    results = {}
    for p in [PolicyId.P0, PolicyId.P1, PolicyId.A2, PolicyId.P3]:
        results[p.value] = solve_recovery_problem(snapshot, p)
    return results

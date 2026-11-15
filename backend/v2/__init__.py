"""
StallBreaker 2.0 V2 Module.
Houses advanced research algorithms, baselines, and multi-tier recovery engines.
"""

from backend.v2.baseline_a2_plus import (
    solve_a2_plus_policy,
    evaluate_deterministic_schedule,
    check_a2_plus_relocation_gating,
    a2_plus_to_proposal_adapter,
    A2PlusCandidatePlan,
    A2PlusDecision
)

__all__ = [
    "solve_a2_plus_policy",
    "evaluate_deterministic_schedule",
    "check_a2_plus_relocation_gating",
    "a2_plus_to_proposal_adapter",
    "A2PlusCandidatePlan",
    "A2PlusDecision"
]

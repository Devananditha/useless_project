"""
Test Suite: A2+ Deterministic Lookahead Baseline (Stage 3)
Verifies:
1. Mandatory acceptance tests A2P-01, A2P-02, and A2P-03.
2. Adversarial source eligibility and budgeting edge cases.
3. Physical safety gating independence.
4. Schedule evaluation accuracy and chronology.
5. Verifier compatibility via adapter.
6. Deterministic idempotency.
"""

import copy
import pytest

from backend.models import (
    VehicleState,
    PartSource,
    RejectedOption
)
from backend.fixtures import (
    get_canonical_s_math_01_fixture,
    get_rollable_s_math_01_fixture,
    get_s_math_02_fixture,
    get_s_math_03_fixture
)
from backend.verifier import (
    verify_proposal,
    compute_proposal_digest,
    VerificationStatus
)
from backend.v2.baseline_a2_plus import (
    solve_a2_plus_policy,
    evaluate_deterministic_schedule,
    check_a2_plus_relocation_gating,
    a2_plus_to_verifier_view,
    a2_plus_to_proposal_adapter,
    A2PlusDecision,
    A2PlusVerifierView
)


# -----------------------------------------------------------------------------
# 1. Mandatory Acceptance Tests (Section 6)
# -----------------------------------------------------------------------------

def test_a2p_01_canonical_s_math_01_lookahead_upgrade():
    """
    Test A2P-01: Lookahead Upgrade on Canonical S-MATH-01 under Hoist Lock.
    - Movement must be HOLD_ON_BAY.
    - Cheapest source S2 ($18.00) results in RO-1051 finish at t=87 (P=54), lateness L=33, Z1=99.0 ticks.
    - Alternative S1 ($55.00) freight delta is $37.00 <= $50.00.
    - S1 finishes RO-1051 at t=65 (P=54), reducing L to 11 ticks, Z1=33.0 ticks.
    - A2+ upgrades to S1, yielding weighted lateness 33.0 ticks.
    - The generated schedule is verified by the independent verifier.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    # 1. Overall decision status
    assert decision.is_feasible is True
    assert decision.status == "HEURISTIC"
    assert decision.selected_movement == "HOLD_ON_BAY"
    assert decision.selected_source_id == "S1"
    assert decision.weighted_lateness == 33.0
    assert decision.freight_cost == 55.0

    # 2. Candidate evaluations ledger check
    assert len(decision.candidate_evaluations) == 2
    eval_s2 = [e for e in decision.candidate_evaluations if e.source_id == "S2"][0]
    eval_s1 = [e for e in decision.candidate_evaluations if e.source_id == "S1"][0]

    assert eval_s2.source_cost == 18.0
    assert eval_s2.weighted_lateness == 99.0
    assert eval_s2.ro1051_finish_tick == 87
    assert eval_s2.ro1051_lateness_ticks == 33

    assert eval_s1.source_cost == 55.0
    assert eval_s1.freight_delta_from_cheapest == 37.0
    assert eval_s1.weighted_lateness == 33.0
    assert eval_s1.ro1051_finish_tick == 65
    assert eval_s1.ro1051_lateness_ticks == 11
    assert eval_s1.qualifies_for_upgrade is True

    # 3. Milestone times
    assert decision.b4_release_tick == 41  # 27 + 12 + 2
    assert decision.ro1042_finish_tick == 41
    assert decision.ro1051_finish_tick == 65

    # 4. Independent Verifier Certification
    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert len(v_res.violations) == 0


def test_a2p_02_s_math_02_null_benefit_restraint():
    """
    Test A2P-02: Null-Control Restraint on S-MATH-02.
    - Technician K2 is occupied until tick 60.
    - S2 ($18.00) completes RO-1051 at tick 86 <= promise 90 -> Z1 = 0.0 ticks.
    - S1 ($55.00) completes RO-1051 at tick 84 <= promise 90 -> Z1 = 0.0 ticks.
    - S1 offers zero lateness improvement over S2 (equal lateness does not qualify).
    - A2+ strictly retains S2 ($18.00), saving $37.00.
    """
    snap = get_s_math_02_fixture(version=14)
    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.is_feasible is True
    assert decision.selected_movement == "HOLD_ON_BAY"
    assert decision.selected_source_id == "S2"
    assert decision.weighted_lateness == 0.0
    assert decision.freight_cost == 18.0

    eval_s2 = [e for e in decision.candidate_evaluations if e.source_id == "S2"][0]
    eval_s1 = [e for e in decision.candidate_evaluations if e.source_id == "S1"][0]

    assert eval_s2.weighted_lateness == 0.0
    assert eval_s1.weighted_lateness == 0.0
    assert eval_s1.qualifies_for_upgrade is False
    assert "does not strictly improve" in (eval_s1.disqualification_reason or "")

    # Independent verifier accepts S2 baseline plan
    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert len(v_res.violations) == 0


def test_a2p_03_s_math_03_physical_safety_gating():
    """
    Test A2P-03: Physical Invariant Gating on S-MATH-03.
    - Holding location H2 has 2 open stalls (capacity 2, available 2).
    - However, RO-1042 has current_vehicle_state=PARTIALLY_DISMANTLED, is_rollable=False,
      and technician_signoff_recorded=False.
    - A2+ must reject RELOCATE_TO_H2 and enforce HOLD_ON_BAY.
    - S2 ($18.00) yields Z1 = 111.0 ticks.
    - S1 ($55.00) yields Z1 = 45.0 ticks.
    - S1 qualifies (delta = $37 <= $50) and is selected.
    """
    snap = get_s_math_03_fixture(version=14)
    assert snap.h2_available_stalls == 2

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.is_feasible is True
    # Crucial: H2 availability does not override physical safety gating
    assert decision.selected_movement == "HOLD_ON_BAY"
    assert decision.selected_source_id == "S1"
    assert decision.weighted_lateness == 45.0
    assert decision.freight_cost == 55.0

    eval_s2 = [e for e in decision.candidate_evaluations if e.source_id == "S2"][0]
    eval_s1 = [e for e in decision.candidate_evaluations if e.source_id == "S1"][0]
    assert eval_s2.weighted_lateness == 111.0
    assert eval_s1.weighted_lateness == 45.0
    assert eval_s1.qualifies_for_upgrade is True

    # Independent verifier certification
    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert len(v_res.violations) == 0


# -----------------------------------------------------------------------------
# 2. Source Eligibility & Infeasibility Tests (Section 7)
# -----------------------------------------------------------------------------

def test_a2_plus_no_eligible_sources_returns_infeasible():
    """Prove that empty source list returns an un-fabricated INFEASIBLE decision."""
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.sources = []

    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is False
    assert decision.status == "INFEASIBLE"
    assert decision.selected_source_id is None
    assert decision.selected_source_name is None
    assert decision.ro1042_finish_tick is None
    assert decision.ro1051_finish_tick is None
    assert decision.weighted_lateness is None
    assert decision.freight_cost is None
    assert decision.scheduled_intervals == []


def test_a2_plus_zero_atp_source_rejected():
    """Prove that sources with ATP < 1 are pruned from eligible candidates."""
    snap = get_canonical_s_math_01_fixture(version=14)
    # Mark S1 and S2 with ATP = 0
    for s in snap.sources:
        s.atp = 0

    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is False
    assert decision.status == "INFEASIBLE"
    atp_rejections = [r for r in decision.rejected_options if r.reason_code == "INSUFFICIENT_ATP"]
    assert len(atp_rejections) == 2


def test_a2_plus_invalid_fitment_source_rejected():
    """Prove that sources failing fitment verification are excluded."""
    snap = get_canonical_s_math_01_fixture(version=14)
    for s in snap.sources:
        s.fitment_verified = False

    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is False
    assert decision.status == "INFEASIBLE"
    fit_rejections = [r for r in decision.rejected_options if r.reason_code == "FITMENT_MISMATCH"]
    assert len(fit_rejections) == 2


def test_a2_plus_expired_quote_source_rejected():
    """Prove that sources with expired quotations are excluded."""
    snap = get_canonical_s_math_01_fixture(version=14)
    for s in snap.sources:
        s.quote_valid = False

    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is False
    assert decision.status == "INFEASIBLE"
    quote_rejections = [r for r in decision.rejected_options if r.reason_code == "EXPIRED_QUOTE"]
    assert len(quote_rejections) == 2


# -----------------------------------------------------------------------------
# 3. Budgeting & Lookahead Surcharge Boundaries (Section 7)
# -----------------------------------------------------------------------------

def test_a2_plus_alternative_exceeds_budget_disqualified():
    """
    Alternative with strictly better lateness is DISQUALIFIED when cost delta > budget.
    S2 costs $18.00 (Z1 = 99.0).
    S1 costs $70.00 (delta = $52.00 > $50.00, Z1 = 33.0).
    S1 must be disqualified, and S2 must be retained.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    s1 = [s for s in snap.sources if s.source_id == "S1"][0]
    s1.cost = 70.00  # $70 - $18 = $52 > $50 budget

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.selected_source_id == "S2"
    assert decision.weighted_lateness == 99.0
    assert decision.freight_cost == 18.0

    eval_s1 = [e for e in decision.candidate_evaluations if e.source_id == "S1"][0]
    assert eval_s1.qualifies_for_upgrade is False
    assert "exceeds permitted budget" in (eval_s1.disqualification_reason or "")


def test_a2_plus_alternative_exact_budget_boundary_qualifies():
    """
    Alternative costing EXACTLY $50.00 more qualifies on the boundary (delta <= 50.0).
    S2 costs $18.00 (Z1 = 99.0).
    S1 costs $68.00 (delta = $50.00 exactly, Z1 = 33.0).
    S1 must qualify and be selected.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    s1 = [s for s in snap.sources if s.source_id == "S1"][0]
    s1.cost = 68.00  # $68 - $18 = $50.00 exactly

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.selected_source_id == "S1"
    assert decision.weighted_lateness == 33.0
    assert decision.freight_cost == 68.0

    eval_s1 = [e for e in decision.candidate_evaluations if e.source_id == "S1"][0]
    assert eval_s1.freight_delta_from_cheapest == 50.0
    assert eval_s1.qualifies_for_upgrade is True


def test_a2_plus_alternative_equal_lateness_does_not_qualify():
    """Prove that an alternative with equal lateness does NOT qualify for upgrade."""
    snap = get_canonical_s_math_01_fixture(version=14)
    # Set S1 usable time equal to S2 usable time, so lateness is identical
    s1 = [s for s in snap.sources if s.source_id == "S1"][0]
    s2 = [s for s in snap.sources if s.source_id == "S2"][0]
    s1.usable_time_ticks = s2.usable_time_ticks

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.selected_source_id == "S2"
    assert decision.freight_cost == 18.0
    eval_s1 = [e for e in decision.candidate_evaluations if e.source_id == "S1"][0]
    assert eval_s1.qualifies_for_upgrade is False


def test_a2_plus_multiple_qualifying_alternatives_deterministic_tie_breaking():
    """
    When multiple alternatives qualify:
    1. Lowest weighted lateness wins.
    2. Ties in lateness broken by lowest cost.
    3. Ties in cost broken by earliest usable tick.
    4. Ties in usable tick broken by source ID.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    # Add S3, S4, S5
    s_cheap = PartSource(source_id="S0", name="Slow Ground", usable_time_ticks=60, cost=10.0, atp=1, fitment_verified=True, quote_valid=True)
    # S3 and S4 achieve the same lateness, but S3 is cheaper
    s3 = PartSource(source_id="S3", name="Expedited Air A", usable_time_ticks=27, cost=30.0, atp=1, fitment_verified=True, quote_valid=True)
    s4 = PartSource(source_id="S4", name="Expedited Air B", usable_time_ticks=27, cost=35.0, atp=1, fitment_verified=True, quote_valid=True)
    # S5 achieves even better lateness
    s5 = PartSource(source_id="S5", name="Ultra Courier", usable_time_ticks=24, cost=45.0, atp=1, fitment_verified=True, quote_valid=True)
    
    snap.sources = [s_cheap, s3, s4, s5]
    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    # S5 should win because it achieves lowest weighted lateness
    assert decision.selected_source_id == "S5"

    # Now remove S5, test tie-breaker between S3 and S4 (both have same lateness, S3 is $30 vs S4 $35)
    snap.sources = [s_cheap, s3, s4]
    decision_tie = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)
    assert decision_tie.selected_source_id == "S3"
    assert decision_tie.freight_cost == 30.0


def test_a2_plus_single_eligible_source_retained():
    """When only one source is eligible, it is retained unconditionally with zero alternatives."""
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.sources = [snap.sources[0]]  # Only S1

    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is True
    assert decision.selected_source_id == "S1"
    assert len(decision.candidate_evaluations) == 1
    assert decision.candidate_evaluations[0].freight_delta_from_cheapest == 0.0


# -----------------------------------------------------------------------------
# 4. Technician Availability Semantics (Stage 2.2.2 Alignment)
# -----------------------------------------------------------------------------

def test_a2_plus_explicit_technician_zero_tick():
    """
    Prove that an explicit 0 in technician_k2_available_tick is treated as a valid tick
    and is NOT replaced by fallback ro1051.technician_available_tick = 60.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.technician_k2_available_tick = 0
    snap.ro1051.technician_available_tick = 60

    decision = solve_a2_plus_policy(snap)
    # RO-1051 should start at tick 41 (b4 release), NOT delayed until tick 60
    assert decision.selected_source_id == "S1"
    assert decision.ro1051_finish_tick == 65  # 41 + 24 = 65

    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert len([v for v in v_res.violations if v.violation_code == "TECHNICIAN_OVERLAP"]) == 0


def test_a2_plus_technician_fallback_when_primary_none():
    """
    Prove that when technician_k2_available_tick is None, it falls back to
    ro1051.technician_available_tick = 60.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.technician_k2_available_tick = None
    snap.ro1051.technician_available_tick = 60

    decision = solve_a2_plus_policy(snap)
    # RO-1051 start = max(41, 60) = 60 -> finish = 60 + 24 = 84
    assert decision.ro1051_finish_tick == 84

    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED


# -----------------------------------------------------------------------------
# 5. Physical Relocation Gating Precondition Independence
# -----------------------------------------------------------------------------

def test_a2_plus_relocation_blocked_by_each_precondition_independently():
    """
    Prove that each physical safety condition blocks relocation independently.
    Base: rollable fixture with all 4 conditions satisfied.
    """
    base_snap = get_rollable_s_math_01_fixture(version=14)
    can_reloc, rejs = check_a2_plus_relocation_gating(base_snap)
    assert can_reloc is True
    assert len(rejs) == 0

    # Case 1: is_rollable == False
    snap_not_rollable = base_snap.model_copy(deep=True)
    snap_not_rollable.ro1042.is_rollable = False
    can, r = check_a2_plus_relocation_gating(snap_not_rollable)
    assert can is False
    assert any(x.reason_code == "VEHICLE_NOT_ROLLABLE" for x in r)

    # Case 2: current_vehicle_state == PARTIALLY_DISMANTLED
    snap_dismantled = base_snap.model_copy(deep=True)
    snap_dismantled.ro1042.current_vehicle_state = VehicleState.PARTIALLY_DISMANTLED
    can, r = check_a2_plus_relocation_gating(snap_dismantled)
    assert can is False
    assert any(x.reason_code == "VEHICLE_PARTIALLY_DISMANTLED" for x in r)

    # Case 3: technician_signoff_recorded == False
    snap_no_signoff = base_snap.model_copy(deep=True)
    snap_no_signoff.ro1042.technician_signoff_recorded = False
    can, r = check_a2_plus_relocation_gating(snap_no_signoff)
    assert can is False
    assert any(x.reason_code == "MISSING_TECHNICIAN_SIGNOFF" for x in r)

    # Case 4: h2_available_stalls == 0
    snap_no_h2 = base_snap.model_copy(deep=True)
    snap_no_h2.h2_available_stalls = 0
    can, r = check_a2_plus_relocation_gating(snap_no_h2)
    assert can is False
    assert any(x.reason_code == "HOLDING_CAPACITY_EXCEEDED" for x in r)


def test_a2_plus_relocation_mode_certified_by_verifier():
    """
    Test A2+ in RELOCATE_TO_H2 mode on S-MATH-01-ROLLABLE.
    Assert that the schedule generated under relocation passes the independent verifier.
    """
    snap = get_rollable_s_math_01_fixture(version=14)
    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.is_feasible is True
    assert decision.selected_movement == "RELOCATE_TO_H2"
    # S2 ($18.00, ready t=49):
    # RO-1051 starts at 24, finishes at 48. Clearance ends at 50.
    # RO-1042 returns at max(50, 49) = 50. Finishes at 50 + 3 + 12 + 2 = 67.
    # RO-1042 lateness = max(0, 67 - 66) = 1 tick. RO-1051 lateness = 0. Z1 = 1.0 tick.
    # S1 ($55.00, ready t=27):
    # Same finish ticks! Z1 = 1.0 tick. Equal lateness does not qualify.
    # Therefore, cheapest S2 ($18.00) is retained!
    assert decision.selected_source_id == "S2"
    assert decision.weighted_lateness == 1.0
    assert decision.freight_cost == 18.0

    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert len(v_res.violations) == 0


def test_a2_plus_relocation_with_technician_later_than_b4_release():
    """
    Stage 2.2.3 Alignment:
    In RELOCATE_TO_H2, RO-1051 start on B4 is constrained by max(b4_free_reloc, tech_avail).
    When tech_avail = 60, RO-1051 must not start until tick 60.
    """
    snap = get_rollable_s_math_01_fixture(version=14)
    snap.technician_k2_available_tick = 60

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    assert decision.selected_movement == "RELOCATE_TO_H2"
    # RO-1051 start tick must be >= 60
    ro1051_iv = [i for i in decision.scheduled_intervals if i.entity_id == "RO-1051"][0]
    assert ro1051_iv.start_tick >= 60
    assert ro1051_iv.start_tick == 60
    assert decision.ro1051_finish_tick == 84

    prop = a2_plus_to_proposal_adapter(decision)
    v_res = verify_proposal(prop, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert len([v for v in v_res.violations if v.violation_code == "TECHNICIAN_OVERLAP"]) == 0


def test_a2_plus_idempotent_identical_decisions():
    """Prove that repeated evaluations on identical snapshots yield identical decisions."""
    snap = get_canonical_s_math_01_fixture(version=14)

    d1 = solve_a2_plus_policy(snap)
    d2 = solve_a2_plus_policy(snap)

    assert d1.decision_id == d2.decision_id
    assert d1.selected_source_id == d2.selected_source_id
    assert d1.selected_movement == d2.selected_movement
    assert d1.weighted_lateness == d2.weighted_lateness
    assert d1.freight_cost == d2.freight_cost
    assert len(d1.scheduled_intervals) == len(d2.scheduled_intervals)
    for i1, i2 in zip(d1.scheduled_intervals, d2.scheduled_intervals):
        assert i1.start_tick == i2.start_tick
        assert i1.end_tick == i2.end_tick
        assert i1.entity_id == i2.entity_id
        assert i1.operation == i2.operation


# -----------------------------------------------------------------------------
# 6. Stage 3.1 Verifier Identity & Tie-Break Audit Tests
# -----------------------------------------------------------------------------

def test_a2_plus_verifier_view_preserves_identity_in_digest():
    """
    Stage 3.1 Task 1: Prove that A2PlusVerifierView preserves policy_id='A2_PLUS'
    in the computed decision digest without modifying PolicyId enum or Proposal.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is True

    view = a2_plus_to_verifier_view(decision)
    assert isinstance(view, A2PlusVerifierView)
    assert view.policy_id == "A2_PLUS"

    digest_a2_plus = compute_proposal_digest(view)
    
    # Mutate view copy to legacy A2 and verify the digest changes strictly
    view_a2 = view.model_copy()
    view_a2.policy_id = "A2"
    digest_a2 = compute_proposal_digest(view_a2)
    assert digest_a2_plus != digest_a2

    # Verify that verify_proposal validates the view and records A2_PLUS digest
    v_res = verify_proposal(view, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    assert v_res.proposal_digest == digest_a2_plus


def test_a2_plus_infeasible_adapter_conversion_rejected():
    """
    Stage 3.1 Task 2: Prove that infeasible A2PlusDecision cannot be converted into
    a populated verifier view/proposal, rejecting fabrication of 0/999 milestones.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.sources = []  # Force infeasibility

    decision = solve_a2_plus_policy(snap)
    assert decision.is_feasible is False
    assert decision.status == "INFEASIBLE"
    assert decision.b4_release_tick is None
    assert decision.ro1051_finish_tick is None
    assert decision.ro1042_finish_tick is None
    assert decision.weighted_lateness is None
    assert decision.freight_cost is None

    # Conversion must raise ValueError and reject fabrication
    with pytest.raises(ValueError) as excinfo:
        a2_plus_to_verifier_view(decision)
    assert "Cannot project infeasible A2PlusDecision" in str(excinfo.value)

    # Prove backwards-compatibility alias also raises ValueError
    with pytest.raises(ValueError):
        a2_plus_to_proposal_adapter(decision)


def test_a2_plus_tie_break_earlier_usable_tick_wins():
    """
    Stage 3.1 Task 3A: When two qualifying alternatives have equal weighted lateness
    and equal cost, earlier usable-ready tick must strictly win.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.technician_k2_available_tick = 50  # Bottleneck bounds completion time

    # S_cheap: cost $10, usable tick 55 -> Z1 = 117.0
    s_cheap = PartSource(source_id="S_CHEAP", name="Slow Ground", usable_time_ticks=55, cost=10.0, atp=1, fitment_verified=True, quote_valid=True)
    # Alt 1: S_LATE: cost $40, usable tick 30 -> clears B4 at 44 -> ro1051 starts at max(44, 50)=50 -> Z1 = 60.0
    s_late = PartSource(source_id="S_LATE", name="Air Express Late", usable_time_ticks=30, cost=40.0, atp=1, fitment_verified=True, quote_valid=True)
    # Alt 2: S_EARLY: cost $40, usable tick 24 -> clears B4 at 38 -> ro1051 starts at max(38, 50)=50 -> Z1 = 60.0
    s_early = PartSource(source_id="S_EARLY", name="Air Express Early", usable_time_ticks=24, cost=40.0, atp=1, fitment_verified=True, quote_valid=True)

    # Intentionally place S_LATE before S_EARLY in sources
    snap.sources = [s_cheap, s_late, s_early]

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    # Both s_late and s_early qualify (delta $30 <= $50, Z1 60.0 < 117.0, cost $40 == $40)
    # S_EARLY has usable_time_ticks 24 < 30, so S_EARLY must win
    assert decision.selected_source_id == "S_EARLY"
    assert decision.freight_cost == 40.0
    assert decision.weighted_lateness == 60.0


def test_a2_plus_tie_break_lexicographically_lower_source_id_wins():
    """
    Stage 3.1 Task 3B: When two qualifying alternatives have equal weighted lateness,
    equal cost, AND equal usable-ready tick, lexicographically lower source ID must win.
    """
    snap = get_canonical_s_math_01_fixture(version=14)
    snap.technician_k2_available_tick = 50

    s_cheap = PartSource(source_id="S_CHEAP", name="Slow Ground", usable_time_ticks=55, cost=10.0, atp=1, fitment_verified=True, quote_valid=True)
    s_beta = PartSource(source_id="S_BETA", name="Courier Beta", usable_time_ticks=25, cost=40.0, atp=1, fitment_verified=True, quote_valid=True)
    s_alpha = PartSource(source_id="S_ALPHA", name="Courier Alpha", usable_time_ticks=25, cost=40.0, atp=1, fitment_verified=True, quote_valid=True)

    # Intentionally place S_BETA before S_ALPHA
    snap.sources = [s_cheap, s_beta, s_alpha]

    decision = solve_a2_plus_policy(snap, max_freight_budget_delta=50.0)

    # Both qualify with identical Z1, identical cost $40, identical usable tick 25
    # Lexicographical comparison: 'S_ALPHA' < 'S_BETA'
    assert decision.selected_source_id == "S_ALPHA"
    assert decision.freight_cost == 40.0
    assert decision.weighted_lateness == 60.0

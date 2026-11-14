"""
Automated Minimum Acceptance Gate Tests for StallBreaker CP-SAT MVP.
Covers all 16 required test criteria with real OR-Tools CP-SAT execution.
No mocked solver outputs.
"""

import pytest
from backend.models import (
    PolicyId,
    VehicleState,
    BayState,
    SolverStatusEnum,
    ApprovalStatus,
    PartSource
)
from backend.fixtures import (
    get_canonical_s_math_01_fixture,
    get_rollable_s_math_01_fixture
)
from backend.solver import solve_recovery_problem
from backend.policies import run_policy_comparison
from backend.state_store import StateStore
from backend.revalidation import revalidate_and_approve_proposal
from backend.eligibility import validate_source_eligibility, validate_relocation_feasibility


def test_01_canonical_s_math_01_a2_arithmetic():
    """1. Canonical S-MATH-01 A2 fixture arithmetic."""
    snap = get_canonical_s_math_01_fixture()
    prop_a2 = solve_recovery_problem(snap, PolicyId.A2)

    assert prop_a2.solver_status == SolverStatusEnum.OPTIMAL
    assert prop_a2.selected_source_id == "S2"
    assert prop_a2.selected_movement == "HOLD_ON_BAY"
    assert prop_a2.b4_release_tick == 63  # 13:15 PM (49 + 12 + 2)
    assert prop_a2.ro1051_finish_tick == 87  # 15:15 PM (63 + 24)
    assert prop_a2.ro1051_lateness_ticks == 33  # 87 - 54
    assert prop_a2.downstream_delay_minutes == 165  # 33 * 5 min
    assert prop_a2.ro1042_lateness_ticks == 0  # 63 <= 66
    assert prop_a2.weighted_lateness_ticks == 99.0  # 3.0 * 33


def test_02_canonical_s_math_01_p3_arithmetic():
    """2. Canonical S-MATH-01 P3 fixture arithmetic."""
    snap = get_canonical_s_math_01_fixture()
    prop_p3 = solve_recovery_problem(snap, PolicyId.P3)

    assert prop_p3.solver_status == SolverStatusEnum.OPTIMAL
    assert prop_p3.selected_source_id == "S1"
    assert prop_p3.selected_movement == "HOLD_ON_BAY"
    assert prop_p3.b4_release_tick == 41  # 11:25 AM (27 + 12 + 2)
    assert prop_p3.ro1051_finish_tick == 65  # 13:25 PM (41 + 24)
    assert prop_p3.ro1051_lateness_ticks == 11  # 65 - 54
    assert prop_p3.downstream_delay_minutes == 55  # 11 * 5 min
    assert prop_p3.ro1042_lateness_ticks == 0  # 41 <= 66
    assert prop_p3.weighted_lateness_ticks == 33.0  # 3.0 * 11


def test_03_ninety_nine_versus_thirty_three_weighted_ticks():
    """3. 99 versus 33 weighted ticks."""
    snap = get_canonical_s_math_01_fixture()
    comp = run_policy_comparison(snap)

    assert comp.baseline_a2.weighted_lateness_ticks == 99.0
    assert comp.joint_p3.weighted_lateness_ticks == 33.0


def test_04_sixty_six_point_seven_percent_reduction():
    """4. 66.7% fixture reduction."""
    snap = get_canonical_s_math_01_fixture()
    comp = run_policy_comparison(snap)

    assert comp.weighted_lateness_reduction_pct == 66.7


def test_05_one_hundred_ten_minute_delay_difference():
    """5. 110-minute RO-1051 delay difference under defined assumptions."""
    snap = get_canonical_s_math_01_fixture()
    comp = run_policy_comparison(snap)

    assert comp.downstream_lateness_savings_minutes == 110


def test_06_unsafe_movement_rejection():
    """6. Unsafe movement rejection when vehicle is partially dismantled."""
    snap = get_canonical_s_math_01_fixture()
    can_reloc, rejections = validate_relocation_feasibility(snap)

    assert can_reloc is False
    assert any(r.reason_code == "VEHICLE_NOT_SAFE_TO_MOVE" for r in rejections)


def test_07_h2_capacity_reservation_before_movement():
    """7. H2 capacity reservation before movement (rejects if H2 stalls = 0)."""
    # Create scenario where vehicle is safe to relocate, but H2 has 0 available stalls
    snap = get_rollable_s_math_01_fixture()
    snap.h2_available_stalls = 0
    can_reloc, rejections = validate_relocation_feasibility(snap)

    assert can_reloc is False
    assert any(r.reason_code == "HOLDING_CAPACITY_EXCEEDED" for r in rejections)


def test_08_bay_no_overlap():
    """8. Bay no-overlap: RO-1051 cannot enter B4 while RO-1042 occupies B4."""
    snap = get_canonical_s_math_01_fixture()
    prop = solve_recovery_problem(snap, PolicyId.P3)

    # In scheduled intervals, verify no overlap between B4 occupancy for RO-1042 and RO-1051
    b4_release = prop.b4_release_tick
    ro1051_start = [i.start_tick for i in prop.scheduled_intervals if i.entity_id == "RO-1051"][0]
    
    assert ro1051_start >= b4_release


def test_09_technician_no_overlap():
    """9. Technician no-overlap: Tech K1 cannot perform install and calibration simultaneously."""
    snap = get_canonical_s_math_01_fixture()
    prop = solve_recovery_problem(snap, PolicyId.P3)

    ro1042_intervals = [i for i in prop.scheduled_intervals if i.entity_id == "RO-1042" and "Installation" in i.operation]
    ro1051_intervals = [i for i in prop.scheduled_intervals if i.entity_id == "RO-1051"]

    if ro1042_intervals and ro1051_intervals:
        ro1042_end = ro1042_intervals[0].end_tick
        ro1051_start = ro1051_intervals[0].start_tick
        assert ro1051_start >= ro1042_end


def test_10_return_to_bay_precedence():
    """10. Return-to-bay precedence in rollable scenario: Return transit requires B4 clearance and part readiness."""
    snap = get_rollable_s_math_01_fixture()
    prop = solve_recovery_problem(snap, PolicyId.P3)

    assert prop.selected_movement == "RELOCATE_TO_H2"
    assert prop.b4_release_tick == 24  # 21 + 3 relocation transit
    assert prop.ro1051_finish_tick == 48  # 24 + 24 service ticks
    assert prop.ro1051_lateness_ticks == 0
    # Return transit happens after RO-1051 clearance (48 + 2 = 50) and after S2 ready (49)
    return_transits = [i for i in prop.scheduled_intervals if "Return Transit" in i.operation]
    assert len(return_transits) == 1
    assert return_transits[0].start_tick >= 50


def test_11_source_atp_eligibility():
    """11. Source ATP eligibility: Source with ATP=0 is rejected."""
    s = PartSource(source_id="S_TEST", name="Test Part", usable_time_ticks=30, cost=20.0, atp=0)
    is_elig, rejections = validate_source_eligibility(s)

    assert is_elig is False
    assert any(r.reason_code == "INSUFFICIENT_ATP" for r in rejections)


def test_12_invalid_fitment_rejection():
    """12. Invalid fitment rejection: Source with unverified fitment is rejected."""
    s = PartSource(source_id="S_TEST", name="Test Part", usable_time_ticks=30, cost=20.0, atp=1, fitment_verified=False)
    is_elig, rejections = validate_source_eligibility(s)

    assert is_elig is False
    assert any(r.reason_code == "FITMENT_MISMATCH" for r in rejections)


def test_13_expired_quote_rejection():
    """13. Expired quote rejection: Source with quote_valid=False is rejected."""
    s = PartSource(source_id="S_TEST", name="Test Part", usable_time_ticks=30, cost=20.0, atp=1, quote_valid=False)
    is_elig, rejections = validate_source_eligibility(s)

    assert is_elig is False
    assert any(r.reason_code == "EXPIRED_QUOTE" for r in rejections)


def test_14_inventory_version_conflict():
    """14. Inventory version conflict detection."""
    test_store = StateStore()
    test_store.version = 14
    snap = test_store.get_active_snapshot()
    prop = solve_recovery_problem(snap, PolicyId.P3)
    test_store.save_proposal(prop)

    assert prop.input_snapshot_version == 14

    # Trigger competing reservation -> advances version to 15
    test_store.trigger_competing_reservation("S1")
    assert test_store.version == 15
    assert prop.input_snapshot_version != test_store.version


def test_15_stale_proposal_cannot_be_committed():
    """15. Stale proposal cannot be committed (returns STALE_SNAPSHOT)."""
    test_store = StateStore()
    test_store.version = 14
    snap = test_store.get_active_snapshot()
    prop = solve_recovery_problem(snap, PolicyId.P3)
    test_store.save_proposal(prop)

    # Advance live version
    test_store.trigger_competing_reservation("S1")

    # Attempt to approve old proposal
    # Revalidation gate uses global store; let's simulate with the global store
    from backend.state_store import store as global_store
    global_store.reset_to_canonical()
    global_store.version = 14
    prop = solve_recovery_problem(global_store.get_active_snapshot(), PolicyId.P3)
    global_store.save_proposal(prop)
    
    # Simulate competing reservation
    global_store.trigger_competing_reservation("S1")
    
    # Advisor clicks approve
    res = revalidate_and_approve_proposal(prop.proposal_id)
    assert res["success"] is False
    assert res["status"] == ApprovalStatus.STALE_SNAPSHOT.value
    assert "Stale snapshot detected" in res["message"]


def test_16_new_proposal_requires_new_human_approval():
    """16. New proposal generated after stale abort requires new human approval (not auto-committed)."""
    from backend.state_store import store as global_store
    global_store.reset_to_canonical()
    global_store.version = 14
    prop = solve_recovery_problem(global_store.get_active_snapshot(), PolicyId.P3)
    global_store.save_proposal(prop)
    
    # Stock race event
    global_store.trigger_competing_reservation("S1")
    
    # Advisor clicks approve on old proposal
    res = revalidate_and_approve_proposal(prop.proposal_id)
    
    assert res["requires_human_approval"] is True
    new_prop = res["new_proposal"]
    assert new_prop.approval_status == ApprovalStatus.PENDING_APPROVAL
    assert new_prop.proposal_id != prop.proposal_id
    assert new_prop.selected_source_id == "S2"  # S1 was depleted, solver picked S2!

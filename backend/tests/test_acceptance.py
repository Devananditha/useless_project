"""
Automated Minimum Acceptance Gate & Integration Tests for StallBreaker CP-SAT MVP.
Covers all 16 canonical criteria PLUS integration tests for API contract, read-only GETs,
optimistic concurrency, benchmark integrity, and relocation event sequence.
No mocked solver outputs: all runs execute genuine Google OR-Tools CP-SAT models.
"""

import os
import json
import pytest

from backend.main import (
    solve_scenario,
    get_scenario,
    select_scenario,
    trigger_competing_reservation,
    approve_proposal,
    SolveRequest
)
from backend.models import (
    PolicyId,
    VehicleState,
    BayState,
    SolverStatusEnum,
    ApprovalStatus,
    PartSource,
    ScenarioSnapshot,
    RepairOrder,
    SolveResponse
)
from backend.fixtures import (
    get_canonical_s_math_01_fixture,
    get_rollable_s_math_01_fixture,
    tick_to_clock
)
from backend.solver import solve_recovery_problem
from backend.policies import run_policy_comparison
from backend.state_store import StateStore, store
from backend.revalidation import revalidate_and_approve_proposal
from backend.eligibility import validate_source_eligibility, validate_relocation_feasibility
from backend.benchmark import run_benchmark


# =========================================================================
# Canonical Arithmetic & State Machine Gates (1-16)
# =========================================================================

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
    snap = get_rollable_s_math_01_fixture()
    snap.h2_available_stalls = 0
    can_reloc, rejections = validate_relocation_feasibility(snap)

    assert can_reloc is False
    assert any(r.reason_code == "HOLDING_CAPACITY_EXCEEDED" for r in rejections)


def test_08_single_bay_milestone_precedence():
    """8. Single-bay milestone precedence: RO-1051 on Bay B4 begins only after RO-1042 installation and clearance transit complete."""
    snap = get_canonical_s_math_01_fixture()
    prop = solve_recovery_problem(snap, PolicyId.P3)

    b4_release = prop.b4_release_tick
    ro1051_start = [i.start_tick for i in prop.scheduled_intervals if i.entity_id == "RO-1051"][0]
    
    assert ro1051_start >= b4_release


def test_09_sequential_job_milestone_ordering():
    """9. Sequential job milestone ordering: On the single shared alignment hoist, RO-1051 calibration is scheduled strictly after RO-1042 completes installation and clearance via linear milestone precedence."""
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

    test_store.trigger_competing_reservation("S1")
    assert test_store.version == 15
    assert prop.input_snapshot_version != test_store.version


def test_15_stale_proposal_cannot_be_committed():
    """15. Stale proposal cannot be committed (returns STALE_SNAPSHOT)."""
    store.reset_to_canonical()
    store.version = 14
    prop = solve_recovery_problem(store.get_active_snapshot(), PolicyId.P3)
    store.save_proposal(prop)
    
    # Simulate competing reservation
    store.trigger_competing_reservation("S1")
    
    # Advisor clicks approve
    res = revalidate_and_approve_proposal(prop.proposal_id)
    assert res["success"] is False
    assert res["status"] == ApprovalStatus.STALE_SNAPSHOT.value
    assert "Stale snapshot detected" in res["message"]


def test_16_new_proposal_requires_new_human_approval():
    """16. New proposal generated after stale abort requires new human approval (not auto-committed)."""
    store.reset_to_canonical()
    store.version = 14
    prop = solve_recovery_problem(store.get_active_snapshot(), PolicyId.P3)
    store.save_proposal(prop)
    
    # Stock race event
    store.trigger_competing_reservation("S1")
    
    # Advisor clicks approve on old proposal
    res = revalidate_and_approve_proposal(prop.proposal_id)
    
    assert res["requires_human_approval"] is True
    new_prop = res["new_proposal"]
    assert new_prop.approval_status == ApprovalStatus.PENDING_APPROVAL
    assert new_prop.proposal_id != prop.proposal_id
    assert new_prop.selected_source_id == "S2"


# =========================================================================
# Integration & Defect Repair Tests (17-27)
# =========================================================================

def test_17_solve_api_response_shape():
    """17. Solve endpoint returns exact SolveResponse model: comparison, active_proposal, snapshot."""
    store.reset_to_canonical()
    req = SolveRequest(scenario_id="S-MATH-01", compare_a2_p3=True)
    res: SolveResponse = solve_scenario(req)

    assert res.comparison is not None
    assert res.active_proposal is not None
    assert res.snapshot is not None

    comp = res.comparison
    assert comp.baseline_a2 is not None
    assert comp.joint_p3 is not None
    assert comp.weighted_lateness_reduction_pct == 66.7
    assert res.active_proposal.proposal_id == comp.joint_p3.proposal_id
    assert res.snapshot.scenario_id == "S-MATH-01"


def test_18_scenario_get_is_read_only():
    """18. GET scenario endpoint is strictly read-only and does not mutate version or emit side effects."""
    store.reset_to_canonical()
    initial_version = store.version

    # First read-only retrieval
    snap1 = get_scenario("S-MATH-01")
    v1 = snap1.snapshot_version

    # Second read-only retrieval
    snap2 = get_scenario("S-MATH-01")
    v2 = snap2.snapshot_version

    # Verify no version mutation occurred
    assert v1 == initial_version
    assert v2 == initial_version
    assert store.version == initial_version


def test_19_repeated_get_does_not_invalidate_proposal():
    """19. Repeated GET calls do not invalidate an existing proposal."""
    store.reset_to_canonical()
    solve_res = solve_scenario(SolveRequest(scenario_id="S-MATH-01", compare_a2_p3=True))
    prop_id = solve_res.active_proposal.proposal_id

    # Perform multiple read-only GET requests
    for _ in range(5):
        snap = get_scenario("S-MATH-01")
        assert snap.scenario_id == "S-MATH-01"

    # Attempt approval of the original proposal
    appr_res = approve_proposal(prop_id)
    assert appr_res["success"] is True
    assert appr_res["status"] == "APPROVED"


def test_20_act_3_competing_reservation_structure_and_stale_rejection():
    """20. Act 3 competing reservation advances version and triggers stale rejection on approval."""
    store.reset_to_canonical()
    solve_res = solve_scenario(SolveRequest(scenario_id="S-MATH-01", compare_a2_p3=True))
    prop_id = solve_res.active_proposal.proposal_id
    v_orig = solve_res.snapshot.snapshot_version

    # Trigger stock race via endpoint handler
    race_res = trigger_competing_reservation("S-MATH-01", "S1")

    assert race_res["status"] == "COMPETING_RESERVATION_SIMULATED"
    assert race_res["affected_source"] == "S1"
    assert race_res["new_atp"] == 0
    assert race_res["new_snapshot_version"] == v_orig + 1
    assert "snapshot" in race_res

    # Attempt to approve old proposal
    appr_res = approve_proposal(prop_id)

    assert appr_res["success"] is False
    assert appr_res["status"] == "STALE_SNAPSHOT"
    assert appr_res["requires_human_approval"] is True
    assert appr_res["old_proposal"].proposal_id == prop_id
    assert appr_res["new_proposal"].selected_source_id == "S2"
    assert appr_res["new_proposal"].approval_status == ApprovalStatus.PENDING_APPROVAL


def test_21_replacement_proposal_requires_explicit_human_approval():
    """21. Replacement proposal can be explicitly authorized by advisor in subsequent call."""
    store.reset_to_canonical()
    solve_res = solve_scenario(SolveRequest(scenario_id="S-MATH-01", compare_a2_p3=True))
    old_id = solve_res.active_proposal.proposal_id

    trigger_competing_reservation("S-MATH-01", "S1")
    stale_appr = approve_proposal(old_id)
    new_prop_id = stale_appr["new_proposal"].proposal_id

    # Second approval explicitly targets new proposal
    commit_res = approve_proposal(new_prop_id)

    assert commit_res["success"] is True
    assert commit_res["status"] == "APPROVED"
    assert commit_res["proposal"].proposal_id == new_prop_id
    assert "Simulation only" in commit_res["message"]


def test_22_a2_and_p3_solver_statuses_and_lexicographic_passes():
    """22. Verify actual solver statuses and lexicographic multi-pass tracking."""
    snap = get_canonical_s_math_01_fixture()
    prop_p3 = solve_recovery_problem(snap, PolicyId.P3)

    assert prop_p3.pass1_status == SolverStatusEnum.OPTIMAL
    assert prop_p3.pass2_status == SolverStatusEnum.OPTIMAL
    assert prop_p3.solver_status == SolverStatusEnum.OPTIMAL

    prop_a2 = solve_recovery_problem(snap, PolicyId.A2)
    assert prop_a2.pass1_status == SolverStatusEnum.OPTIMAL
    assert prop_a2.pass2_status == SolverStatusEnum.OPTIMAL
    assert prop_a2.solver_status == SolverStatusEnum.OPTIMAL


def test_23_benchmark_status_counts_derived_from_actual_outputs():
    """23. Benchmark status counts are genuinely derived and written to artifact."""
    bench = run_benchmark(n=10, master_seed=42)

    assert bench["total_seeds"] == 10
    assert bench["valid_paired_seeds"] == 10
    assert "a2_status_distribution" in bench
    assert "p3_status_distribution" in bench
    assert sum(bench["a2_status_distribution"].values()) == 10
    assert sum(bench["p3_status_distribution"].values()) == 10
    assert bench["artifact_path"] is not None
    assert os.path.exists(bench["artifact_path"])

    with open(bench["artifact_path"], "r") as f:
        saved = json.load(f)
    assert saved["benchmark_id"] == bench["benchmark_id"]
    assert len(saved["records"]) == 10


def test_24_infeasible_runs_do_not_contaminate_lateness_averages():
    """24. Infeasible runs (sentinel lateness >= 900) are excluded from average calculation."""
    bench = run_benchmark(n=5, master_seed=42)
    # Average lateness must be reasonable (< 200 ticks), not contaminated by 999 sentinel
    assert bench["mean_p3_weighted_lateness"] < 200.0
    assert bench["mean_a2_weighted_lateness"] < 200.0


def test_25_ineligible_inventory_cannot_be_selected_by_solver():
    """25. Ineligible inventory cannot be selected by the solver."""
    snap = get_canonical_s_math_01_fixture()
    # Invalidate both sources
    snap.sources[0].fitment_verified = False  # S1 invalid fitment
    snap.sources[1].atp = 0                   # S2 zero stock

    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.solver_status == SolverStatusEnum.INFEASIBLE
    assert prop.selected_source_id is None
    assert prop.weighted_lateness_ticks >= 900.0


def test_26_act_2_relocation_timeline_full_sequence():
    """26. Act 2 relocation schedule contains all 7 chronological intervals including clearance and return transit."""
    snap = get_rollable_s_math_01_fixture()
    prop = solve_recovery_problem(snap, PolicyId.P3)

    assert prop.selected_movement == "RELOCATE_TO_H2"
    ops = [i.operation for i in prop.scheduled_intervals]

    assert any("Transit from Bay B4 to Holding H2" in op for op in ops)
    assert any("Fleet ADAS Calibration" in op for op in ops)
    assert any("Post-Service Clearance Transit" in op for op in ops)
    assert any("Staged in Holding H2" in op for op in ops)
    assert any("Return Transit from H2 to Bay B4" in op for op in ops)
    assert any("Part Installation" in op for op in ops)
    assert any("Final Verification & Bay Clearance" in op for op in ops)

    # Chronological timestamps
    # RO-1051 ADAS Calibration finishes at t=48 (12:00)
    adas_int = [i for i in prop.scheduled_intervals if "Fleet ADAS Calibration" in i.operation][0]
    assert adas_int.start_tick == 24
    assert adas_int.end_tick == 48

    # Bay clearance completes at t=50 (12:10)
    b4_clear = [i for i in prop.scheduled_intervals if "Post-Service Clearance Transit" in i.operation][0]
    assert b4_clear.start_tick == 48
    assert b4_clear.end_tick == 50

    # RO-1042 return transit: t=50 to 53 (12:10 to 12:25)
    ret_trans = [i for i in prop.scheduled_intervals if "Return Transit" in i.operation][0]
    assert ret_trans.start_tick == 50
    assert ret_trans.end_tick == 53

    # Installation on B4: t=53 to 65 (12:25 to 13:25)
    install_int = [i for i in prop.scheduled_intervals if "Part Installation" in i.operation][0]
    assert install_int.start_tick == 53
    assert install_int.end_tick == 65

    # Final clearance: t=65 to 67 (13:25 to 13:35)
    final_clear = [i for i in prop.scheduled_intervals if "Final Verification & Bay Clearance" in i.operation][0]
    assert final_clear.start_tick == 65
    assert final_clear.end_tick == 67


def test_27_canonical_fixture_promise_times_and_models():
    """27. Canonical fixture vehicle models, promises, and usable times match specification."""
    snap = get_canonical_s_math_01_fixture()

    assert snap.ro1042.vehicle_model == "Ford Explorer"
    assert snap.ro1042.promise_ticks == 66  # 13:30
    assert snap.ro1051.vehicle_model == "Ford F-150 Commercial"
    assert snap.ro1051.promise_ticks == 54  # 12:30

    s1 = [s for s in snap.sources if s.source_id == "S1"][0]
    s2 = [s for s in snap.sources if s.source_id == "S2"][0]

    assert s1.usable_time_ticks == 27  # 10:15 AM
    assert s1.cost == 55.0
    assert s2.usable_time_ticks == 49  # 12:05 PM
    assert s2.cost == 18.0


# =========================================================================
# Scenario-Scoped Identity & Earliest-Start Patch Tests (28-31)
# =========================================================================

def test_28_cross_scenario_approval_rejected():
    """28. Proposal approval is strictly rejected when proposal scenario_id != active scenario_id."""
    store.reset_to_canonical()
    # 1. Generate P3 proposal on canonical scenario S-MATH-01
    solve_res = solve_scenario(SolveRequest(scenario_id="S-MATH-01", compare_a2_p3=True))
    canon_prop_id = solve_res.active_proposal.proposal_id

    # 2. Switch to S-MATH-01-ROLLABLE (both have snapshot version 14)
    select_scenario("S-MATH-01-ROLLABLE")
    assert store.current_scenario_id == "S-MATH-01-ROLLABLE"
    assert store.version == 14

    # 3. Attempt to approve S-MATH-01 proposal while S-MATH-01-ROLLABLE is active
    appr_res = approve_proposal(canon_prop_id)

    # 4. Verification: Rejected for scenario mismatch
    assert appr_res["success"] is False
    assert appr_res["status"] == "SCENARIO_MISMATCH"
    assert "Scenario mismatch" in appr_res["message"]

    # 5. Generate fresh proposal for newly active scenario S-MATH-01-ROLLABLE
    fresh_solve = solve_scenario(SolveRequest(scenario_id="S-MATH-01-ROLLABLE", compare_a2_p3=True))
    fresh_prop_id = fresh_solve.active_proposal.proposal_id

    # 6. Verification: New proposal can be approved when scenario and version match
    commit_res = approve_proposal(fresh_prop_id)
    assert commit_res["success"] is True
    assert commit_res["status"] == "APPROVED"
    assert commit_res["proposal"].proposal_id == fresh_prop_id


def test_29_reverse_cross_scenario_approval_rejected():
    """29. Reverse cross-scenario approval rejection: S-MATH-01-ROLLABLE proposal rejected on S-MATH-01."""
    store.reset_to_canonical()
    select_scenario("S-MATH-01-ROLLABLE")

    # Generate proposal on S-MATH-01-ROLLABLE
    roll_solve = solve_scenario(SolveRequest(scenario_id="S-MATH-01-ROLLABLE", compare_a2_p3=True))
    roll_prop_id = roll_solve.active_proposal.proposal_id

    # Switch active scenario back to S-MATH-01
    select_scenario("S-MATH-01")
    assert store.current_scenario_id == "S-MATH-01"

    # Attempt to approve rollable proposal while S-MATH-01 is active
    appr_res = approve_proposal(roll_prop_id)
    assert appr_res["success"] is False
    assert appr_res["status"] == "SCENARIO_MISMATCH"
    assert "Scenario mismatch" in appr_res["message"]

    # Fresh proposal on S-MATH-01 approves successfully
    canon_solve = solve_scenario(SolveRequest(scenario_id="S-MATH-01", compare_a2_p3=True))
    canon_prop_id = canon_solve.active_proposal.proposal_id
    commit_res = approve_proposal(canon_prop_id)
    assert commit_res["success"] is True
    assert commit_res["status"] == "APPROVED"


def test_30_earliest_start_canonical_slack_promise():
    """30. Earliest feasible milestone start enforced via AddMaxEquality under zero-lateness slack conditions (Canonical)."""
    snap = get_canonical_s_math_01_fixture()
    # Provide abundant slack so lateness is 0 regardless of start time
    snap.ro1042.promise_ticks = 100  # 16:20 PM (abundant slack: finish 63 <= 100)
    snap.ro1051.promise_ticks = 100  # 16:20 PM (abundant slack: finish 87 <= 100)

    prop = solve_recovery_problem(snap, PolicyId.P3)

    # In Pass 1, weighted lateness is 0
    assert prop.weighted_lateness_ticks == 0.0
    # In Pass 2, freight cost is minimized -> selects S2 ($18.00 freight, usable at tick 49)
    assert prop.selected_source_id == "S2"

    # AddMaxEquality guarantees install start is strictly max(current_t=21, ready_time=49) = 49
    # Cannot be delayed arbitrarily to tick 50, 60, etc.
    install_int = [i for i in prop.scheduled_intervals if "Part Installation" in i.operation][0]
    assert install_int.start_tick == 49
    assert install_int.end_tick == 49 + 12  # 61

    # B4 release must be strictly 49 + 12 + 2 = 63
    assert prop.b4_release_tick == 63
    # RO-1051 finish must be strictly 63 + 24 = 87
    assert prop.ro1051_finish_tick == 87


def test_31_earliest_start_rollable_slack_promise():
    """31. Earliest feasible milestone start enforced via AddMaxEquality under zero-lateness slack conditions (Rollable)."""
    snap = get_rollable_s_math_01_fixture()
    snap.ro1042.promise_ticks = 100  # 16:20 PM (abundant slack: finish 67 <= 100)
    snap.ro1051.promise_ticks = 50   # 12:10 PM (forces relocation: finish 48 <= 50, whereas hold yields >= 65)

    prop = solve_recovery_problem(snap, PolicyId.P3)

    assert prop.weighted_lateness_ticks == 0.0
    assert prop.selected_movement == "RELOCATE_TO_H2"
    assert prop.selected_source_id == "S2"

    # RO-1051 on B4: 24 to 48. B4 clearance ends at 50. S2 ready at 49.
    # AddMaxEquality strictly forces return start = max(50, 49) = 50.
    ret_trans = [i for i in prop.scheduled_intervals if "Return Transit" in i.operation][0]
    assert ret_trans.start_tick == 50
    assert ret_trans.end_tick == 53

    # Installation on B4 must start immediately upon arrival at 53
    install_int = [i for i in prop.scheduled_intervals if "Part Installation" in i.operation][0]
    assert install_int.start_tick == 53
    assert install_int.end_tick == 65

    # Final clearance must end at 67
    final_clear = [i for i in prop.scheduled_intervals if "Final Verification & Bay Clearance" in i.operation][0]
    assert final_clear.start_tick == 65
    assert final_clear.end_tick == 67


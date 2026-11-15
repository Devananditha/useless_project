"""
Test Suite: Independent Solution Verifier & Mutation Testing (Stage 2)
Verifies that backend/verifier.py independently certifies physical, temporal,
and mathematical invariants without importing OR-Tools or calling any solver.
Includes adversarial mutation tests corrupting valid proposals.
"""

import copy
import pytest
from backend.models import (
    PolicyId,
    Proposal,
    SolverStatusEnum,
    ScheduledInterval
)
from backend.fixtures import (
    get_canonical_s_math_01_fixture,
    get_rollable_s_math_01_fixture,
    get_s_math_02_fixture,
    get_s_math_03_fixture
)
from backend.solver import solve_recovery_problem
from backend.verifier import (
    verify_proposal,
    VerificationStatus
)


# -----------------------------------------------------------------------------
# 1. Verification of Valid Solver Proposals
# -----------------------------------------------------------------------------

def test_verifier_accepts_valid_s_math_01_proposal():
    """Verify that a legitimate CP-SAT solution on S-MATH-01 is certified."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    res = verify_proposal(prop, snap)
    assert res.verification_status == VerificationStatus.VERIFIED
    assert len(res.violations) == 0
    assert len(res.checked_invariants) >= 7
    assert "VERIFIED" in res.verification_summary


def test_verifier_accepts_valid_s_math_01_rollable_proposal():
    """Verify that a legitimate relocation proposal on S-MATH-01-ROLLABLE is certified."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    assert prop.selected_movement == "RELOCATE_TO_H2"
    res = verify_proposal(prop, snap)
    assert res.verification_status == VerificationStatus.VERIFIED
    assert len(res.violations) == 0


def test_verifier_accepts_valid_s_math_02_proposal():
    """Verify that legitimate S-MATH-02 solution (selecting S2) is certified."""
    snap = get_s_math_02_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    assert prop.selected_source_id == "S2"
    assert prop.weighted_lateness_ticks == 0.0
    res = verify_proposal(prop, snap)
    assert res.verification_status == VerificationStatus.VERIFIED
    assert len(res.violations) == 0


def test_verifier_accepts_valid_s_math_03_proposal():
    """Verify that legitimate S-MATH-03 solution (HOLD_ON_BAY, S1) is certified."""
    snap = get_s_math_03_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    assert prop.selected_movement == "HOLD_ON_BAY"
    assert prop.selected_source_id == "S1"
    assert prop.weighted_lateness_ticks == 45.0
    res = verify_proposal(prop, snap)
    assert res.verification_status == VerificationStatus.VERIFIED
    assert len(res.violations) == 0


# -----------------------------------------------------------------------------
# 2. Adversarial Mutation Testing
# -----------------------------------------------------------------------------

def test_mutation_01_ineligible_source_insufficient_atp():
    """Corrupt proposal by selecting an inventory source with ATP = 0."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    # Mutate snapshot so selected source has ATP=0
    corrupt_snap = snap.model_copy(deep=True)
    for s in corrupt_snap.sources:
        if s.source_id == prop.selected_source_id:
            s.atp = 0
            
    res = verify_proposal(prop, corrupt_snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "INSUFFICIENT_ATP" in violation_codes


def test_mutation_02_invalid_fitment_source():
    """Corrupt proposal by selecting a source with unverified fitment."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_snap = snap.model_copy(deep=True)
    for s in corrupt_snap.sources:
        if s.source_id == prop.selected_source_id:
            s.fitment_verified = False
            
    res = verify_proposal(prop, corrupt_snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "INVALID_FITMENT" in violation_codes


def test_mutation_03_expired_quote_source():
    """Corrupt proposal by selecting an expired quote source."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_snap = snap.model_copy(deep=True)
    for s in corrupt_snap.sources:
        if s.source_id == prop.selected_source_id:
            s.quote_valid = False
            
    res = verify_proposal(prop, corrupt_snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "EXPIRED_QUOTE" in violation_codes


def test_mutation_04_install_starts_before_usable_ready_tick():
    """Corrupt proposal by shifting installation earlier than part usable arrival."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    # Selected source S1 usable at t=27. Corrupt install start to t=22.
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if "Part Installation" in iv.operation:
            new_intervals.append(iv.model_copy(update={"start_tick": 22, "end_tick": 34}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "INSTALL_BEFORE_PART_READY" in violation_codes


def test_mutation_05_unsafe_vehicle_relocated_to_h2():
    """Corrupt proposal by setting RELOCATE_TO_H2 on a partially dismantled vehicle."""
    snap = get_canonical_s_math_01_fixture(version=14)
    # On canonical S-MATH-01, vehicle is PARTIALLY_DISMANTLED and is_rollable=False
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.selected_movement = "RELOCATE_TO_H2"
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "UNSAFE_RELOCATION_UNROLLABLE" in violation_codes
    assert "MISSING_TECHNICIAN_SIGNOFF" in violation_codes


def test_mutation_06_relocation_to_saturated_holding():
    """Corrupt proposal by moving vehicle to H2 when h2_available_stalls = 0."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    # Saturate holding lot
    corrupt_snap = snap.model_copy(deep=True)
    corrupt_snap.h2_available_stalls = 0
    
    res = verify_proposal(prop, corrupt_snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "HOLDING_CAPACITY_EXCEEDED" in violation_codes


def test_mutation_07_clearance_omitted_or_shortened():
    """Corrupt proposal by reducing clearance interval to 1 tick (requires 2)."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if "Clearance" in iv.operation:
            new_intervals.append(iv.model_copy(update={"start_tick": iv.start_tick, "end_tick": iv.start_tick + 1}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "CLEARANCE_SHORTENED" in violation_codes


def test_mutation_08_overlapping_bay_occupancy():
    """Corrupt proposal by scheduling RO-1051 before RO-1042 finishes clearance."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1051":
            # Start RO-1051 at tick 30 (while RO-1042 is still on bay)
            new_intervals.append(iv.model_copy(update={"start_tick": 30, "end_tick": 54}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "BAY_OCCUPANCY_OVERLAP" in violation_codes


def test_mutation_09_technician_overlap():
    """Corrupt proposal in S-MATH-02 by scheduling RO-1051 before Tech K2 is available."""
    snap = get_s_math_02_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1051":
            # Schedule RO-1051 to start at tick 45 (violating Tech K2 availability at t=60)
            new_intervals.append(iv.model_copy(update={"start_tick": 45, "end_tick": 69}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "TECHNICIAN_OVERLAP" in violation_codes


def test_mutation_10_context_mismatch_scenario_and_version():
    """Corrupt proposal by changing its scenario identity or snapshot version."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    # Scenario mismatch
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scenario_id = "S-MATH-02"
    res1 = verify_proposal(corrupt_prop, snap)
    assert res1.verification_status == VerificationStatus.REJECTED
    assert "SCENARIO_IDENTITY_MISMATCH" in [v.violation_code for v in res1.violations]
    
    # Version mismatch
    corrupt_prop2 = prop.model_copy(deep=True)
    corrupt_prop2.input_snapshot_version = 99
    res2 = verify_proposal(corrupt_prop2, snap)
    assert res2.verification_status == VerificationStatus.REJECTED
    assert "SNAPSHOT_VERSION_MISMATCH" in [v.violation_code for v in res2.violations]


def test_mutation_11_falsified_lateness_arithmetic():
    """Corrupt proposal by claiming artificially low lateness values."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.ro1051_lateness_ticks = 0  # True lateness is 11 ticks
    corrupt_prop.weighted_lateness_ticks = 0.0  # True weighted lateness is 33.0
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    violation_codes = [v.violation_code for v in res.violations]
    assert "LATENESS_ARITHMETIC_MISMATCH" in violation_codes
    assert "WEIGHTED_LATENESS_MISMATCH" in violation_codes


def test_infeasible_proposal_cannot_be_verified():
    """Infeasible solver proposal must be rejected by the verifier."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P0)  # Policy P0 produces infeasible proposal
    assert prop.solver_status == SolverStatusEnum.INFEASIBLE
    
    res = verify_proposal(prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "SOLVER_STATUS_INFEASIBLE" in [v.violation_code for v in res.violations]


def test_insufficient_evidence_when_intervals_missing():
    """Missing scheduled intervals must yield INSUFFICIENT_EVIDENCE."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scheduled_intervals = []
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert "MISSING_CRITICAL_EVIDENCE" in [v.violation_code for v in res.violations]


# -----------------------------------------------------------------------------
# 3. Stage 2.2 Sequence Reconstruction & Missing Evidence Mutations
# -----------------------------------------------------------------------------

def test_mutation_12_missing_ro1042_install_interval():
    """Missing RO-1042 installation interval fails closed with INSUFFICIENT_EVIDENCE."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scheduled_intervals = [
        iv for iv in corrupt_prop.scheduled_intervals
        if not (iv.entity_id == "RO-1042" and iv.entity_type == "JOB" and ("Installation" in iv.operation or "Install" in iv.operation))
    ]
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert "MISSING_RO1042_INSTALL_INTERVAL" in [v.violation_code for v in res.violations]


def test_mutation_13_missing_ro1051_service_interval():
    """Missing RO-1051 service interval fails closed with INSUFFICIENT_EVIDENCE."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scheduled_intervals = [
        iv for iv in corrupt_prop.scheduled_intervals
        if not (iv.entity_id == "RO-1051" and iv.entity_type == "JOB")
    ]
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert "MISSING_RO1051_SERVICE_INTERVAL" in [v.violation_code for v in res.violations]


def test_mutation_14_missing_outbound_relocation_interval():
    """Missing outbound relocation transit fails closed with INSUFFICIENT_EVIDENCE."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scheduled_intervals = [
        iv for iv in corrupt_prop.scheduled_intervals
        if not (iv.entity_id == "RO-1042" and iv.entity_type == "TRANSIT" and ("Holding H2" in iv.operation or "to Holding H2" in iv.operation))
    ]
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert "MISSING_OUTBOUND_TRANSIT_INTERVAL" in [v.violation_code for v in res.violations]


def test_mutation_15_missing_return_transit_interval():
    """Missing return transit interval fails closed with INSUFFICIENT_EVIDENCE."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scheduled_intervals = [
        iv for iv in corrupt_prop.scheduled_intervals
        if not (iv.entity_id == "RO-1042" and iv.entity_type == "TRANSIT" and "Return" in iv.operation)
    ]
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert "MISSING_RETURN_TRANSIT_INTERVAL" in [v.violation_code for v in res.violations]


def test_mutation_16_shortened_outbound_transit():
    """Shortened outbound transit violates facility duration and is REJECTED."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1042" and iv.entity_type == "TRANSIT" and ("Holding H2" in iv.operation or "to Holding H2" in iv.operation):
            new_intervals.append(iv.model_copy(update={"start_tick": iv.start_tick, "end_tick": iv.start_tick + 1}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "RELOCATION_TRANSIT_SHORTENED" in [v.violation_code for v in res.violations]


def test_mutation_17_shortened_return_transit():
    """Shortened return transit violates facility duration and is REJECTED."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1042" and iv.entity_type == "TRANSIT" and "Return" in iv.operation:
            new_intervals.append(iv.model_copy(update={"start_tick": iv.start_tick, "end_tick": iv.start_tick + 1}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "RELOCATION_TRANSIT_SHORTENED" in [v.violation_code for v in res.violations]


def test_mutation_18_install_before_vehicle_return():
    """RO-1042 installation scheduled before return arrival is REJECTED."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1042" and ("Installation" in iv.operation or "Install" in iv.operation):
            new_intervals.append(iv.model_copy(update={"start_tick": 35, "end_tick": 47}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "INSTALL_BEFORE_VEHICLE_RETURN" in [v.violation_code for v in res.violations]


def test_mutation_19_ro1051_starts_before_ro1042_clears():
    """RO-1051 starting before RO-1042 clears Bay B4 is REJECTED for bay overlap."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1051":
            new_intervals.append(iv.model_copy(update={"start_tick": 30, "end_tick": 54}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "BAY_OCCUPANCY_OVERLAP" in [v.violation_code for v in res.violations]


def test_mutation_20_proposal_b4_release_tick_mismatch():
    """Proposal reporting falsified b4_release_tick is REJECTED."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.b4_release_tick = 10
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "B4_RELEASE_MISMATCH" in [v.violation_code for v in res.violations]


def test_mutation_21_proposal_ro1051_finish_tick_mismatch():
    """Proposal reporting falsified ro1051_finish_tick is REJECTED."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.ro1051_finish_tick = 50
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "RO1051_FINISH_MISMATCH" in [v.violation_code for v in res.violations]


def test_mutation_22_clearance_discontinuity():
    """Discontinuity between installation end and clearance start is REJECTED."""
    snap = get_canonical_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1042" and "Clearance" in iv.operation:
            new_intervals.append(iv.model_copy(update={"start_tick": 45, "end_tick": 47}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "CLEARANCE_DISCONTINUITY" in [v.violation_code for v in res.violations]


def test_mutation_23_missing_final_clearance_relocation():
    """Missing final clearance interval in relocation scenario fails closed with INSUFFICIENT_EVIDENCE."""
    snap = get_rollable_s_math_01_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    assert prop.selected_movement == "RELOCATE_TO_H2"
    
    corrupt_prop = prop.model_copy(deep=True)
    corrupt_prop.scheduled_intervals = [
        iv for iv in corrupt_prop.scheduled_intervals
        if not (iv.entity_id == "RO-1042" and "Clearance" in iv.operation)
    ]
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE
    assert "MISSING_FINAL_CLEARANCE_INTERVAL" in [v.violation_code for v in res.violations]


def test_mutation_24_s_math_02_ro1051_before_tech_k2_available():
    """RO-1051 scheduled before Tech K2 is available in S-MATH-02 is REJECTED."""
    snap = get_s_math_02_fixture(version=14)
    prop = solve_recovery_problem(snap, PolicyId.P3)
    
    corrupt_prop = prop.model_copy(deep=True)
    new_intervals = []
    for iv in corrupt_prop.scheduled_intervals:
        if iv.entity_id == "RO-1051":
            new_intervals.append(iv.model_copy(update={"start_tick": 45, "end_tick": 69}))
        else:
            new_intervals.append(iv)
    corrupt_prop.scheduled_intervals = new_intervals
    
    res = verify_proposal(corrupt_prop, snap)
    assert res.verification_status == VerificationStatus.REJECTED
    assert "TECHNICIAN_OVERLAP" in [v.violation_code for v in res.violations]

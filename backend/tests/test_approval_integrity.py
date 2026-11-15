"""
Adversarial Verifier-to-Approval Integrity Test Suite for StallBreaker 2.

Exhaustively verifies that unverified, rejected, tampered, stale, or cross-scenario
proposals can NEVER bypass verification gates to reach APPROVED status.
Tests all 8 canonical lifecycle and integrity gates (Tests A through H).
"""

import copy
import pytest
from backend.state_store import store
from backend.models import (
    ApprovalStatus,
    SolverStatusEnum,
    PolicyId,
    Proposal
)
from backend.solver import solve_recovery_problem
from backend.verifier import (
    verify_proposal,
    compute_proposal_digest,
    VerificationStatus
)
from backend.revalidation import revalidate_and_approve_proposal
from backend.main import approve_proposal, select_scenario


@pytest.fixture(autouse=True)
def reset_store_before_each_test():
    """Ensure clean canonical state before every test run."""
    store.reset_to_canonical()
    yield
    store.reset_to_canonical()


def test_a_rejected_proposal_bypass_blocked():
    """
    Test A: A proposal in REJECTED state cannot be approved.
    Must return success=False, status=REJECTED, and log REJECTED_PROPOSAL_COMMIT_BLOCKED.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    v_res = verify_proposal(proposal, snap)
    proposal.verification_result = v_res.model_dump()
    proposal.approval_status = ApprovalStatus.REJECTED
    store.save_proposal(proposal)

    initial_event_count = len(store.events)
    res = revalidate_and_approve_proposal(proposal.proposal_id)

    assert res["success"] is False
    assert res["status"] == ApprovalStatus.REJECTED.value
    assert "cannot be approved" in res["message"].lower()

    # Verify proposal remains REJECTED in store
    saved = store.get_proposal(proposal.proposal_id)
    assert saved.approval_status == ApprovalStatus.REJECTED

    # Verify guard event logged and no commit event created
    events = store.events[initial_event_count:]
    assert any(e.event_type == "REJECTED_PROPOSAL_COMMIT_BLOCKED" for e in events)
    assert not any(e.event_type == "PROPOSAL_COMMITTED" for e in events)


def test_b_missing_certificate_bypass_blocked():
    """
    Test B: A proposal with no verification certificate (verification_result=None)
    cannot be approved. Gate 5 must catch this, reject the proposal, and log UNVERIFIED_PROPOSAL_ABORT.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    proposal.verification_result = None  # Strip certificate
    proposal.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(proposal)

    initial_event_count = len(store.events)
    res = revalidate_and_approve_proposal(proposal.proposal_id)

    assert res["success"] is False
    assert res["status"] == "UNVERIFIED_PROPOSAL"
    assert "lacks an independent verification certificate" in res["message"]

    # Verify proposal transitioned to REJECTED
    saved = store.get_proposal(proposal.proposal_id)
    assert saved.approval_status == ApprovalStatus.REJECTED

    events = store.events[initial_event_count:]
    assert any(e.event_type == "UNVERIFIED_PROPOSAL_ABORT" for e in events)
    assert not any(e.event_type == "PROPOSAL_COMMITTED" for e in events)


def test_c_insufficient_evidence_blocked():
    """
    Test C: A proposal with INSUFFICIENT_EVIDENCE cannot be committed.
    Gate 2 and Gate 5 must enforce non-bypassable rejection.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    proposal.verification_result = {
        "certificate_id": "CERT-TEST-INSUFF",
        "proposal_id": proposal.proposal_id,
        "verification_status": VerificationStatus.INSUFFICIENT_EVIDENCE.value,
        "proposal_digest": compute_proposal_digest(proposal),
        "checked_invariants": ["I1"],
        "violations": [],
        "verification_summary": "Missing interval telemetry."
    }
    proposal.approval_status = ApprovalStatus.INSUFFICIENT_EVIDENCE
    store.save_proposal(proposal)

    res = revalidate_and_approve_proposal(proposal.proposal_id)

    assert res["success"] is False
    assert res["status"] == ApprovalStatus.INSUFFICIENT_EVIDENCE.value
    assert "insufficient_evidence" in res["message"].lower()

    saved = store.get_proposal(proposal.proposal_id)
    assert saved.approval_status == ApprovalStatus.INSUFFICIENT_EVIDENCE


def test_d_tampered_decision_digest_blocked():
    """
    Test D: A verified proposal whose decision fields are mutated after certification
    must be detected by Gate 6 (SHA-256 digest mismatch) and rejected as CERTIFICATE_TAMPERED.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    v_res = verify_proposal(proposal, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    proposal.verification_result = v_res.model_dump()
    proposal.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(proposal)

    # Maliciously tamper with decision fields post-certification
    proposal.selected_source_id = "S4"  # Changed from S1/S2 to an invalid/cheaper source
    store.save_proposal(proposal)

    initial_event_count = len(store.events)
    res = revalidate_and_approve_proposal(proposal.proposal_id)

    assert res["success"] is False
    assert res["status"] == "CERTIFICATE_TAMPERED"
    assert "modified after certificate generation" in res["message"]

    saved = store.get_proposal(proposal.proposal_id)
    assert saved.approval_status == ApprovalStatus.REJECTED

    events = store.events[initial_event_count:]
    assert any(e.event_type == "CERTIFICATE_TAMPERED_ABORT" for e in events)
    assert not any(e.event_type == "PROPOSAL_COMMITTED" for e in events)


def test_d2_tampered_schedule_digest_blocked():
    """
    Test D2: Tampering with schedule ticks (b4_release_tick) after certification
    must also be caught by Gate 6.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    v_res = verify_proposal(proposal, snap)
    proposal.verification_result = v_res.model_dump()
    proposal.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(proposal)

    # Tamper with schedule tick
    proposal.b4_release_tick += 5
    store.save_proposal(proposal)

    res = revalidate_and_approve_proposal(proposal.proposal_id)
    assert res["success"] is False
    assert res["status"] == "CERTIFICATE_TAMPERED"


def test_e_snapshot_state_changed_after_verification():
    """
    Test E: If the live inventory/snapshot advances (e.g. competing reservation consumes S1),
    the proposal evaluated under the earlier version is rejected as STALE_SNAPSHOT,
    the old proposal is marked STALE_SNAPSHOT, and an automated re-solve is triggered.
    """
    snap = store.get_active_snapshot()
    initial_version = snap.snapshot_version

    proposal = solve_recovery_problem(snap, PolicyId.P3)
    v_res = verify_proposal(proposal, snap)
    proposal.verification_result = v_res.model_dump()
    proposal.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(proposal)

    # Simulate stock race advancing snapshot version
    updated_snap = store.trigger_competing_reservation("S1")
    assert updated_snap.snapshot_version > initial_version

    initial_event_count = len(store.events)
    res = revalidate_and_approve_proposal(proposal.proposal_id)

    assert res["success"] is False
    assert res["status"] == ApprovalStatus.STALE_SNAPSHOT.value
    assert "stale snapshot detected" in res["message"].lower()

    # The old proposal must be marked STALE_SNAPSHOT
    old_p = store.get_proposal(proposal.proposal_id)
    assert old_p.approval_status == ApprovalStatus.STALE_SNAPSHOT

    # A replacement proposal must have been generated and requires human approval
    assert res["requires_human_approval"] is True
    assert "new_proposal" in res
    assert res["new_proposal"].approval_status == ApprovalStatus.PENDING_APPROVAL
    assert res["new_proposal"].input_snapshot_version == updated_snap.snapshot_version

    events = store.events[initial_event_count:]
    assert any(e.event_type == "STALE_SNAPSHOT_ABORT" for e in events)
    assert any(e.event_type == "RE_SOLVE_REQUESTED" for e in events)
    assert any(e.event_type == "AWAITING_HUMAN_APPROVAL" for e in events)
    assert not any(e.event_type == "PROPOSAL_COMMITTED" for e in events)


def test_f_scenario_changed_after_verification():
    """
    Test F: A proposal evaluated for scenario S-MATH-01 cannot be approved if the active
    scenario has been switched to S-MATH-02. Gate 3 must reject cross-scenario commit.
    """
    store.select_scenario("S-MATH-01")
    snap_01 = store.get_active_snapshot()

    prop_01 = solve_recovery_problem(snap_01, PolicyId.P3)
    v_res = verify_proposal(prop_01, snap_01)
    prop_01.verification_result = v_res.model_dump()
    prop_01.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(prop_01)

    # Switch active scenario to S-MATH-02
    store.select_scenario("S-MATH-02")
    assert store.current_scenario_id == "S-MATH-02"

    initial_event_count = len(store.events)
    res = revalidate_and_approve_proposal(prop_01.proposal_id)

    assert res["success"] is False
    assert res["status"] == "SCENARIO_MISMATCH"
    assert "scenario mismatch" in res["message"].lower()

    # The proposal must NOT have been approved
    saved_01 = store.get_proposal(prop_01.proposal_id)
    assert saved_01.approval_status != ApprovalStatus.APPROVED

    events = store.events[initial_event_count:]
    assert any(e.event_type == "SCENARIO_MISMATCH_ABORT" for e in events)
    assert not any(e.event_type == "PROPOSAL_COMMITTED" for e in events)


def test_g_repeated_approval_idempotent():
    """
    Test G: Once a proposal is APPROVED, subsequent calls to approve the same proposal
    must be cleanly idempotent: returns success=True, status=ALREADY_APPROVED,
    and produces NO duplicate PROPOSAL_COMMITTED events.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    v_res = verify_proposal(proposal, snap)
    assert v_res.verification_status == VerificationStatus.VERIFIED
    proposal.verification_result = v_res.model_dump()
    proposal.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(proposal)

    # First approval: transitions to APPROVED
    first_res = revalidate_and_approve_proposal(proposal.proposal_id)
    assert first_res["success"] is True
    assert first_res["status"] == ApprovalStatus.APPROVED.value

    # Count commit events after first approval
    commit_events = [e for e in store.events if e.event_type == "PROPOSAL_COMMITTED"]
    assert len(commit_events) == 1

    # Second approval call (simulating double click or network retry)
    second_res = revalidate_and_approve_proposal(proposal.proposal_id)
    assert second_res["success"] is True
    assert second_res["status"] == "ALREADY_APPROVED"
    assert "already approved" in second_res["message"].lower()

    # Third approval call via API route wrapper
    third_res = approve_proposal(proposal.proposal_id)
    assert third_res["success"] is True
    assert third_res["status"] == "ALREADY_APPROVED"

    # Crucial assertion: ZERO duplicate PROPOSAL_COMMITTED events
    commit_events_after = [e for e in store.events if e.event_type == "PROPOSAL_COMMITTED"]
    assert len(commit_events_after) == 1


def test_h_replacement_proposal_requires_explicit_approval():
    """
    Test H: A stale abort produces a replacement proposal that is verified and put in
    PENDING_APPROVAL state. It must NOT be automatically committed.
    When explicitly approved on a second call, it passes all gates and reaches APPROVED.
    """
    snap = store.get_active_snapshot()
    prop_orig = solve_recovery_problem(snap, PolicyId.P3)
    v_orig = verify_proposal(prop_orig, snap)
    prop_orig.verification_result = v_orig.model_dump()
    prop_orig.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(prop_orig)

    # Invalidate snapshot
    store.trigger_competing_reservation("S1")

    # First attempt: aborted due to stale snapshot
    abort_res = revalidate_and_approve_proposal(prop_orig.proposal_id)
    assert abort_res["success"] is False
    assert abort_res["status"] == ApprovalStatus.STALE_SNAPSHOT.value
    assert abort_res["requires_human_approval"] is True

    replacement_proposal = abort_res["new_proposal"]
    replacement_id = replacement_proposal.proposal_id

    # Replacement proposal must NOT be approved yet
    saved_replacement = store.get_proposal(replacement_id)
    assert saved_replacement.approval_status == ApprovalStatus.PENDING_APPROVAL
    assert saved_replacement.verification_result is not None
    assert saved_replacement.verification_result["verification_status"] == VerificationStatus.VERIFIED.value

    # Now the human advisor explicitly reviews and approves the replacement proposal
    approve_res = revalidate_and_approve_proposal(replacement_id)
    assert approve_res["success"] is True
    assert approve_res["status"] == ApprovalStatus.APPROVED.value

    # Verify committed state
    committed_replacement = store.get_proposal(replacement_id)
    assert committed_replacement.approval_status == ApprovalStatus.APPROVED

    # Exactly one commit event logged (for the replacement, none for the stale original)
    commit_events = [e for e in store.events if e.event_type == "PROPOSAL_COMMITTED"]
    assert len(commit_events) == 1
    assert commit_events[0].details["proposal_id"] == replacement_id


def test_i_stale_snapshot_proposal_cannot_transition_to_approved():
    """
    Test I: A proposal with status STALE_SNAPSHOT can never transition to APPROVED.
    Gate 2 must reject approval even if snapshot versions happen to match.
    """
    snap = store.get_active_snapshot()
    proposal = solve_recovery_problem(snap, PolicyId.P3)
    v_res = verify_proposal(proposal, snap)
    proposal.verification_result = v_res.model_dump()
    proposal.approval_status = ApprovalStatus.STALE_SNAPSHOT
    store.save_proposal(proposal)

    res = revalidate_and_approve_proposal(proposal.proposal_id)
    assert res["success"] is False
    assert res["status"] == ApprovalStatus.STALE_SNAPSHOT.value
    assert "cannot be approved" in res["message"].lower()

    saved = store.get_proposal(proposal.proposal_id)
    assert saved.approval_status == ApprovalStatus.STALE_SNAPSHOT

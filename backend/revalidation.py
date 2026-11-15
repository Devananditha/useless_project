"""
Optimistic Concurrency, Independent Verification & Pre-Execution Revalidation Gate.
Enforces non-bypassable verification certificates, decision-payload integrity digests,
stale state snapshot aborts, scenario isolation, and idempotent approval state transitions.

Prototype Security Scope:
The decision-payload SHA-256 digest validates payload consistency and detects accidental
or in-memory modifications within the active local session. Production deployment requires
isolated certificate storage, cryptographic keyed signing (HMAC/Ed25519), and durable
transactional state persistence.
"""

from typing import Dict, Any, Tuple
from backend.models import (
    Proposal,
    ApprovalStatus
)
from backend.state_store import store
from backend.policies import run_policy_comparison
from backend.verifier import (
    verify_proposal,
    compute_proposal_digest,
    VerificationStatus
)


def revalidate_and_approve_proposal(proposal_id: str) -> Dict[str, Any]:
    """
    Evaluates advisor approval of a recovery proposal against:
    1. Idempotency (already approved).
    2. Terminal rejection protection (cannot re-approve REJECTED or INSUFFICIENT_EVIDENCE proposals).
    3. Scenario identity constraint (cross-scenario approval forbidden).
    4. Optimistic concurrency snapshot version (stale inventory triggers automated re-solve).
    5. Certificate presence and valid VERIFIED status.
    6. Anti-tampering proposal decision digest match.
    7. Commit-time invariant re-verification against the live immutable snapshot.
    """
    proposal = store.get_proposal(proposal_id)
    if not proposal:
        return {
            "success": False,
            "status": "NOT_FOUND",
            "message": f"Proposal ID '{proposal_id}' not found in active session."
        }

    current_snapshot = store.get_active_snapshot()
    proposal_v = proposal.input_snapshot_version
    current_v = current_snapshot.snapshot_version

    # -------------------------------------------------------------------------
    # Gate 1: Idempotency Check
    # -------------------------------------------------------------------------
    if proposal.approval_status == ApprovalStatus.APPROVED:
        return {
            "success": True,
            "status": "ALREADY_APPROVED",
            "message": f"Proposal {proposal.proposal_id} is already approved and committed. No duplicate commitment event created.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Gate 2: Terminal Rejection / Insufficient Evidence Guard
    # -------------------------------------------------------------------------
    if proposal.approval_status == ApprovalStatus.REJECTED:
        store.log_event(
            event_type="REJECTED_PROPOSAL_COMMIT_BLOCKED",
            description=f"Commit blocked for proposal {proposal.proposal_id}: Proposal was previously marked REJECTED.",
            version_before=current_v,
            version_after=current_v,
            details={"proposal_id": proposal.proposal_id}
        )
        return {
            "success": False,
            "status": ApprovalStatus.REJECTED.value,
            "message": f"Commit rejected: Proposal {proposal.proposal_id} is in REJECTED state. It cannot be approved without a fresh solver run.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    if proposal.approval_status == ApprovalStatus.INSUFFICIENT_EVIDENCE:
        return {
            "success": False,
            "status": ApprovalStatus.INSUFFICIENT_EVIDENCE.value,
            "message": f"Commit rejected: Proposal {proposal.proposal_id} has INSUFFICIENT_EVIDENCE and cannot be authorized.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    if proposal.approval_status == ApprovalStatus.STALE_SNAPSHOT:
        store.log_event(
            event_type="STALE_PROPOSAL_COMMIT_BLOCKED",
            description=f"Commit blocked for proposal {proposal.proposal_id}: Proposal is in terminal STALE_SNAPSHOT state.",
            version_before=current_v,
            version_after=current_v,
            details={"proposal_id": proposal.proposal_id}
        )
        return {
            "success": False,
            "status": ApprovalStatus.STALE_SNAPSHOT.value,
            "message": f"Commit rejected: Proposal {proposal.proposal_id} is in STALE_SNAPSHOT state. It cannot be approved; a fresh solver run is required.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Gate 3: Enforce Scenario Identity
    # -------------------------------------------------------------------------
    if proposal.scenario_id != current_snapshot.scenario_id:
        store.log_event(
            event_type="SCENARIO_MISMATCH_ABORT",
            description=(
                f"Commit rejected for proposal {proposal.proposal_id}: Proposal was generated for scenario "
                f"'{proposal.scenario_id}', but the currently active scenario is '{current_snapshot.scenario_id}'. "
                f"Cross-scenario proposal commitment is strictly forbidden."
            ),
            version_before=current_v,
            version_after=current_v,
            details={
                "proposal_id": proposal.proposal_id,
                "proposal_scenario_id": proposal.scenario_id,
                "active_scenario_id": current_snapshot.scenario_id
            }
        )
        return {
            "success": False,
            "status": "SCENARIO_MISMATCH",
            "message": (
                f"Commit rejected: Scenario mismatch. Proposal {proposal.proposal_id} belongs to scenario "
                f"'{proposal.scenario_id}', but the active scenario is '{current_snapshot.scenario_id}'."
            ),
            "proposal": proposal,
            "requires_human_approval": True,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Gate 4: Optimistic Concurrency Snapshot Version
    # -------------------------------------------------------------------------
    if proposal_v != current_v:
        proposal.approval_status = ApprovalStatus.STALE_SNAPSHOT
        store.log_event(
            event_type="STALE_SNAPSHOT_ABORT",
            description=(
                f"Commit aborted for proposal {proposal.proposal_id}: Proposal was evaluated under snapshot v{proposal_v}, "
                f"but live inventory has advanced to v{current_v}. Optimistic concurrency check failed."
            ),
            version_before=proposal_v,
            version_after=current_v,
            details={
                "proposal_id": proposal.proposal_id,
                "proposal_version": proposal_v,
                "current_version": current_v
            }
        )

        # Trigger automated re-solve under the current snapshot
        store.log_event(
            event_type="RE_SOLVE_REQUESTED",
            description=(
                f"Automated re-solve triggered under live snapshot v{current_v}. "
                "Evaluating eligible sources against remaining inventory."
            ),
            version_before=current_v,
            version_after=current_v
        )

        new_comparison = run_policy_comparison(current_snapshot)
        # Verify both replacement proposals
        v_a2 = verify_proposal(new_comparison.baseline_a2, current_snapshot)
        new_comparison.baseline_a2.verification_result = v_a2.model_dump()
        v_p3 = verify_proposal(new_comparison.joint_p3, current_snapshot)
        new_comparison.joint_p3.verification_result = v_p3.model_dump()

        new_proposal = new_comparison.joint_p3
        if v_p3.verification_status == VerificationStatus.VERIFIED:
            new_proposal.approval_status = ApprovalStatus.PENDING_APPROVAL
        elif v_p3.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE:
            new_proposal.approval_status = ApprovalStatus.INSUFFICIENT_EVIDENCE
        else:
            new_proposal.approval_status = ApprovalStatus.REJECTED

        store.save_proposal(new_comparison.baseline_a2)
        store.save_proposal(new_comparison.joint_p3)

        store.log_event(
            event_type="AWAITING_HUMAN_APPROVAL",
            description=(
                f"New recovery proposal {new_proposal.proposal_id} generated under snapshot v{current_v} "
                f"(Selected: {new_proposal.selected_source_id or 'None'}, Lat: {new_proposal.downstream_delay_minutes}m). "
                "CRITICAL: Human authorization required before execution."
            ),
            version_before=current_v,
            version_after=current_v,
            details={"new_proposal_id": new_proposal.proposal_id}
        )

        return {
            "success": False,
            "status": ApprovalStatus.STALE_SNAPSHOT.value,
            "message": (
                f"Commit rejected: Stale snapshot detected (Proposal: v{proposal_v}, Live: v{current_v}). "
                f"A new recovery proposal ({new_proposal.proposal_id}) was computed and requires your authorization."
            ),
            "old_proposal": proposal,
            "new_proposal": new_proposal,
            "new_comparison": new_comparison,
            "requires_human_approval": True,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Gate 5: Verification Certificate Existence & Status Check
    # -------------------------------------------------------------------------
    cert_dict = proposal.verification_result
    if not cert_dict:
        proposal.approval_status = ApprovalStatus.REJECTED
        store.log_event(
            event_type="UNVERIFIED_PROPOSAL_ABORT",
            description=f"Commit rejected for proposal {proposal.proposal_id}: Proposal lacks an independent verification certificate.",
            version_before=current_v,
            version_after=current_v,
            details={"proposal_id": proposal.proposal_id}
        )
        return {
            "success": False,
            "status": "UNVERIFIED_PROPOSAL",
            "message": f"Commit rejected: Proposal {proposal.proposal_id} lacks an independent verification certificate.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    cert_status = cert_dict.get("verification_status")
    if cert_status != VerificationStatus.VERIFIED.value:
        if cert_status == VerificationStatus.INSUFFICIENT_EVIDENCE.value:
            proposal.approval_status = ApprovalStatus.INSUFFICIENT_EVIDENCE
            fail_status = "INSUFFICIENT_EVIDENCE"
        else:
            proposal.approval_status = ApprovalStatus.REJECTED
            fail_status = "VERIFICATION_REJECTED"

        store.log_event(
            event_type="UNVERIFIED_PROPOSAL_ABORT",
            description=f"Commit rejected for proposal {proposal.proposal_id}: Certificate status is '{cert_status}'.",
            version_before=current_v,
            version_after=current_v,
            details={"proposal_id": proposal.proposal_id, "verification_status": cert_status}
        )
        return {
            "success": False,
            "status": fail_status,
            "message": f"Commit rejected: Proposal {proposal.proposal_id} verification status is '{cert_status}'.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Gate 6: Anti-Tampering Digest Validation
    # -------------------------------------------------------------------------
    computed_digest = compute_proposal_digest(proposal)
    recorded_digest = cert_dict.get("proposal_digest")
    if computed_digest != recorded_digest:
        proposal.approval_status = ApprovalStatus.REJECTED
        store.log_event(
            event_type="CERTIFICATE_TAMPERED_ABORT",
            description=f"Commit rejected for proposal {proposal.proposal_id}: Proposal decision digest mismatch (tampered after verification).",
            version_before=current_v,
            version_after=current_v,
            details={
                "proposal_id": proposal.proposal_id,
                "recorded_digest": recorded_digest,
                "computed_digest": computed_digest
            }
        )
        return {
            "success": False,
            "status": "CERTIFICATE_TAMPERED",
            "message": f"Commit rejected: Proposal {proposal.proposal_id} decision fields were modified after certificate generation.",
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Gate 7: Immediate Commit-Time Re-Verification
    # -------------------------------------------------------------------------
    commit_v_res = verify_proposal(proposal, current_snapshot)
    proposal.verification_result = commit_v_res.model_dump()
    if commit_v_res.verification_status != VerificationStatus.VERIFIED:
        proposal.approval_status = ApprovalStatus.REJECTED
        store.log_event(
            event_type="COMMIT_VERIFICATION_FAILED",
            description=f"Commit-time independent verification failed for proposal {proposal.proposal_id}: {[v.violation_code for v in commit_v_res.violations]}",
            version_before=current_v,
            version_after=current_v,
            details={"proposal_id": proposal.proposal_id, "violations": [v.model_dump() for v in commit_v_res.violations]}
        )
        return {
            "success": False,
            "status": "COMMIT_VERIFICATION_FAILED",
            "message": f"Commit rejected: Commit-time verification failed ({commit_v_res.verification_summary}).",
            "violations": [v.model_dump() for v in commit_v_res.violations],
            "proposal": proposal,
            "requires_human_approval": False,
            "current_snapshot": current_snapshot
        }

    # -------------------------------------------------------------------------
    # Authorization Accepted
    # -------------------------------------------------------------------------
    proposal.approval_status = ApprovalStatus.APPROVED
    store.log_event(
        event_type="PROPOSAL_COMMITTED",
        description=(
            f"Service Advisor authorized recovery proposal {proposal.proposal_id} in local prototype. "
            f"Source {proposal.selected_source_id} locked at ${proposal.parts_freight_cost:.2f}. "
            f"Bay B4 release scheduled at {proposal.b4_release_clock}. (Simulation only — no real DMS dispatch executed)."
        ),
        version_before=current_v,
        version_after=current_v,
        details={
            "proposal_id": proposal.proposal_id,
            "approved_by": "Service Advisor K. Vance",
            "certificate_id": commit_v_res.certificate_id
        }
    )

    return {
        "success": True,
        "status": ApprovalStatus.APPROVED.value,
        "message": f"Proposal {proposal.proposal_id} successfully authorized by Service Advisor in local prototype session (Simulation only — no real DMS dispatch or inventory reservation executed).",
        "proposal": proposal,
        "requires_human_approval": False,
        "current_snapshot": current_snapshot
    }

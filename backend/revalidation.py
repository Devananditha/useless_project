"""
Optimistic Concurrency & Pre-Execution Revalidation Gate.
Detects stale state snapshots, aborts unauthorized commits, and triggers re-solve workflows.
"""

from typing import Dict, Any, Tuple
from backend.models import (
    Proposal,
    ApprovalStatus
)
from backend.state_store import store
from backend.solver import solve_recovery_problem
from backend.policies import run_policy_comparison


def revalidate_and_approve_proposal(proposal_id: str) -> Dict[str, Any]:
    """
    Evaluates approval of a recovery proposal against the current state snapshot version.
    If versions differ:
    1. Rejects commit with STALE_SNAPSHOT.
    2. Logs stale snapshot rejection event.
    3. Triggers re-solve with current inventory state.
    4. Returns new proposal awaiting human approval (does NOT auto-commit).
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

    # Check optimistic concurrency version
    if proposal_v != current_v:
        # State drift detected! Stale proposal abort
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

        # Trigger re-solve under the current snapshot
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
        store.save_proposal(new_comparison.baseline_a2)
        store.save_proposal(new_comparison.joint_p3)
        new_proposal = new_comparison.joint_p3

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

    # Versions match: Advisor authorization accepted in local prototype state
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
        details={"proposal_id": proposal.proposal_id, "approved_by": "Service Advisor K. Vance"}
    )

    return {
        "success": True,
        "status": ApprovalStatus.APPROVED.value,
        "message": f"Proposal {proposal.proposal_id} successfully authorized by Service Advisor in local prototype session (Simulation only — no real DMS dispatch or inventory reservation executed).",
        "proposal": proposal,
        "requires_human_approval": False,
        "current_snapshot": current_snapshot
    }

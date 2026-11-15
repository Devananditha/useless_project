"""
FastAPI Application Entrypoint for StallBreaker Live MVP.
Exposes RESTful API contracts for solver execution, scenario switching,
concurrency aborts, and advisor approval.
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from pydantic import BaseModel

from backend.models import (
    ScenarioSnapshot,
    Proposal,
    PolicyComparisonResult,
    PolicyId,
    SolveResponse,
    ApprovalStatus
)
from backend.state_store import store
from backend.solver import solve_recovery_problem
from backend.policies import run_policy_comparison
from backend.revalidation import revalidate_and_approve_proposal
from backend.benchmark import run_benchmark
from backend.verifier import verify_proposal, VerificationStatus


app = FastAPI(
    title="StallBreaker Live CP-SAT Service Recovery API",
    description="Backend engine for Tekion Tek-Qubit 2026 UC04 MVP",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SolveRequest(BaseModel):
    scenario_id: Optional[str] = None
    policy_id: PolicyId = PolicyId.P3
    compare_a2_p3: bool = True


class ApprovalRequest(BaseModel):
    proposal_id: str


@app.get("/api/health")
def get_health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "StallBreaker CP-SAT Recovery Demonstrator",
        "solver": "Google OR-Tools CP-SAT",
        "active_scenario": store.current_scenario_id,
        "snapshot_version": store.version
    }


@app.get("/api/scenarios")
def list_scenarios() -> Dict[str, Any]:
    scenarios_list = []
    for sc_id, snap in store.snapshots.items():
        scenarios_list.append({
            "scenario_id": sc_id,
            "name": snap.scenario_name,
            "description": snap.description,
            "is_active": store.current_scenario_id == sc_id
        })
    return {
        "scenarios": scenarios_list,
        "active_scenario_id": store.current_scenario_id,
        "active_snapshot_version": store.version
    }


@app.get("/api/scenarios/{scenario_id}")
def get_scenario(scenario_id: str) -> ScenarioSnapshot:
    """
    Read-only retrieval of a scenario snapshot.
    Does NOT increment version, reset state, or alter active proposal.
    """
    try:
        return store.get_scenario(scenario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/scenarios/{scenario_id}/select")
def select_scenario(scenario_id: str) -> Dict[str, Any]:
    """
    Explicit action to switch the active scenario in the state store.
    """
    try:
        snap = store.select_scenario(scenario_id)
        return {
            "status": "SCENARIO_SELECTED",
            "active_scenario_id": store.current_scenario_id,
            "snapshot": snap
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/solve", response_model=SolveResponse)
def solve_scenario(request: SolveRequest) -> SolveResponse:
    """
    Executes actual Google OR-Tools CP-SAT solver against active scenario snapshot.
    If compare_a2_p3 is True, executes real solver for BOTH A2 and P3 and returns comparative data.
    """
    snapshot = store.get_active_snapshot()
    if request.scenario_id and request.scenario_id != snapshot.scenario_id:
        snapshot = store.select_scenario(request.scenario_id)

    def _verify_and_log(prop: Proposal, snap: ScenarioSnapshot):
        v_res = verify_proposal(prop, snap)
        prop.verification_result = v_res.model_dump()
        if v_res.verification_status != VerificationStatus.VERIFIED:
            if v_res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE:
                prop.approval_status = ApprovalStatus.INSUFFICIENT_EVIDENCE
            else:
                prop.approval_status = ApprovalStatus.REJECTED
            prop.feasibility_explanations.append(f"INDEPENDENT VERIFICATION FAILED: {v_res.verification_summary}")
            store.log_event(
                event_type="PROPOSAL_VERIFICATION_FAILED",
                description=f"Proposal {prop.proposal_id} failed verification: {[v.violation_code for v in v_res.violations]}",
                version_before=snap.snapshot_version,
                version_after=snap.snapshot_version,
                details={"proposal_id": prop.proposal_id, "violations": [v.model_dump() for v in v_res.violations]}
            )
        else:
            prop.approval_status = ApprovalStatus.PENDING_APPROVAL
            store.log_event(
                event_type="PROPOSAL_VERIFIED",
                description=f"Proposal {prop.proposal_id} certified across {len(v_res.checked_invariants)} invariants.",
                version_before=snap.snapshot_version,
                version_after=snap.snapshot_version,
                details={"proposal_id": prop.proposal_id, "summary": v_res.verification_summary}
            )

    if request.compare_a2_p3:
        comparison: PolicyComparisonResult = run_policy_comparison(snapshot)
        _verify_and_log(comparison.baseline_a2, snapshot)
        _verify_and_log(comparison.joint_p3, snapshot)
        store.save_proposal(comparison.baseline_a2)
        store.save_proposal(comparison.joint_p3)
        return SolveResponse(
            comparison=comparison,
            active_proposal=comparison.joint_p3,
            snapshot=snapshot
        )
    else:
        proposal: Proposal = solve_recovery_problem(snapshot, request.policy_id)
        _verify_and_log(proposal, snapshot)
        store.save_proposal(proposal)
        return SolveResponse(
            comparison=None,
            active_proposal=proposal,
            snapshot=snapshot
        )


@app.post("/api/scenarios/{scenario_id}/events/competing-reservation")
def trigger_competing_reservation(scenario_id: str, source_id: str = "S1") -> Dict[str, Any]:
    """
    Simulates external stock race: competing reservation consumes source (default S1), advancing version (e.g. v14 -> v15).
    """
    if scenario_id != store.current_scenario_id:
        store.select_scenario(scenario_id)
    updated_snap = store.trigger_competing_reservation(source_id=source_id)
    return {
        "status": "COMPETING_RESERVATION_SIMULATED",
        "affected_source": source_id,
        "new_atp": 0,
        "new_snapshot_version": updated_snap.snapshot_version,
        "snapshot": updated_snap
    }


@app.post("/api/proposals/{proposal_id}/approve")
def approve_proposal(proposal_id: str) -> Dict[str, Any]:
    """
    Service Advisor click 'Approve & Commit'.
    Checks optimistic concurrency version. If stale, rejects and triggers automated re-solve.
    """
    result = revalidate_and_approve_proposal(proposal_id)
    return result


@app.post("/api/proposals/{proposal_id}/revalidate")
def revalidate_proposal(proposal_id: str) -> Dict[str, Any]:
    """Manual pre-execution revalidation endpoint."""
    return revalidate_and_approve_proposal(proposal_id)


@app.post("/api/proposals/{proposal_id}/verify")
def verify_proposal_endpoint(proposal_id: str) -> Dict[str, Any]:
    """Independent pure-Python certificate verification of an emitted proposal."""
    prop = store.get_proposal(proposal_id)
    if not prop:
        raise HTTPException(status_code=404, detail=f"Proposal '{proposal_id}' not found.")
    snap = store.get_active_snapshot()
    v_res = verify_proposal(prop, snap)
    prop.verification_result = v_res.model_dump()
    if v_res.verification_status != VerificationStatus.VERIFIED:
        if v_res.verification_status == VerificationStatus.INSUFFICIENT_EVIDENCE:
            prop.approval_status = ApprovalStatus.INSUFFICIENT_EVIDENCE
        else:
            prop.approval_status = ApprovalStatus.REJECTED
    else:
        if prop.approval_status not in (ApprovalStatus.APPROVED, ApprovalStatus.STALE_SNAPSHOT):
            prop.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(prop)
    return {
        "status": v_res.verification_status.value,
        "proposal_id": proposal_id,
        "verification": v_res.model_dump()
    }


@app.get("/api/events")
def get_audit_events() -> Dict[str, Any]:
    return {
        "total_events": len(store.events),
        "events": store.events[::-1]  # Return newest first
    }


@app.post("/api/reset")
def reset_system() -> Dict[str, Any]:
    snap = store.reset_to_canonical()
    return {
        "status": "RESET_SUCCESSFUL",
        "snapshot": snap,
        "version": snap.snapshot_version
    }


@app.post("/api/benchmark/run")
def trigger_benchmark(n: int = 100, master_seed: int = 42) -> Dict[str, Any]:
    """Runs actual CP-SAT solver across n deterministic paired seeds."""
    return run_benchmark(n=n, master_seed=master_seed)

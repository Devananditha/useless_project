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
    PolicyId
)
from backend.state_store import store
from backend.solver import solve_recovery_problem
from backend.policies import run_policy_comparison
from backend.revalidation import revalidate_and_approve_proposal
from backend.benchmark import run_benchmark


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
    return {
        "scenarios": [
            {
                "scenario_id": "S-MATH-01",
                "name": "Canonical S-MATH-01: Hoist Lock Disruption",
                "description": "Partially dismantled Ford Explorer on Bay B4; H2 holding saturated. Pure hoist-lock sourcing decision.",
                "is_active": store.current_scenario_id == "S-MATH-01"
            },
            {
                "scenario_id": "S-MATH-01-ROLLABLE",
                "name": "Alternate S-MATH-01-ROLLABLE: Relocatable Vehicle",
                "description": "Ford Explorer certified safe to relocate; 1 available stall in H2 holding. Solver dynamically evaluates relocation.",
                "is_active": store.current_scenario_id == "S-MATH-01-ROLLABLE"
            }
        ],
        "active_scenario_id": store.current_scenario_id,
        "active_snapshot_version": store.version
    }


@app.get("/api/scenarios/{scenario_id}")
def get_scenario(scenario_id: str) -> ScenarioSnapshot:
    try:
        return store.select_scenario(scenario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/solve")
def solve_scenario(request: SolveRequest) -> Dict[str, Any]:
    """
    Executes actual Google OR-Tools CP-SAT solver against active scenario snapshot.
    If compare_a2_p3 is True, executes real solver for BOTH A2 and P3 and returns comparative data.
    """
    snapshot = store.get_active_snapshot()
    if request.scenario_id and request.scenario_id != snapshot.scenario_id:
        snapshot = store.select_scenario(request.scenario_id)

    if request.compare_a2_p3:
        comparison: PolicyComparisonResult = run_policy_comparison(snapshot)
        store.save_proposal(comparison.baseline_a2)
        store.save_proposal(comparison.joint_p3)
        return {
            "comparison": comparison,
            "active_proposal": comparison.joint_p3,
            "snapshot": snapshot
        }
    else:
        proposal: Proposal = solve_recovery_problem(snapshot, request.policy_id)
        store.save_proposal(proposal)
        return {
            "active_proposal": proposal,
            "snapshot": snapshot
        }


@app.post("/api/scenarios/{scenario_id}/events/competing-reservation")
def trigger_competing_reservation(scenario_id: str) -> Dict[str, Any]:
    """
    Simulates external stock race: competing reservation consumes S1, advancing version (v14 -> v15).
    """
    if scenario_id != store.current_scenario_id:
        store.select_scenario(scenario_id)
    updated_snap = store.trigger_competing_reservation(source_id="S1")
    return {
        "status": "COMPETING_RESERVATION_SIMULATED",
        "affected_source": "S1",
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

"""
Independent Solution Verifier for StallBreaker Proposals.
Standalone, pure-Python certificate checker.
DOES NOT import Google OR-Tools or execute constraint solvers.
Inspects emitted proposals against immutable scenario snapshots to verify
temporal, physical, resource, and mathematical invariants.

Security Scope:
Computes a decision-payload integrity digest over all decision-relevant fields
to detect in-memory tampering within the local demonstration session.
Does not claim protection against a privileged state-store attacker; production
deployments require cryptographic keyed signing (HMAC/Ed25519) and isolated certificate storage.
"""

from datetime import datetime
from enum import Enum
import hashlib
import json
import uuid
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field

from backend.models import (
    ScenarioSnapshot,
    Proposal,
    SolverStatusEnum,
    VehicleState
)


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class VerificationViolation(BaseModel):
    violation_code: str = Field(..., description="Machine-readable violation identifier")
    description: str = Field(..., description="Human-readable explanation of the invariant failure")
    entity_id: Optional[str] = Field(default=None, description="Affected entity e.g. RO-1042, B4, K2")
    severity: str = Field(default="ERROR", description="ERROR or WARNING")


class VerificationResult(BaseModel):
    verification_status: VerificationStatus
    proposal_id: str
    scenario_id: str
    snapshot_version: int
    proposal_digest: str = Field(..., description="Deterministic SHA-256 digest of proposal decision fields")
    certificate_id: str = Field(..., description="Unique certificate identifier, e.g. CERT-...")
    violations: List[VerificationViolation] = Field(default_factory=list)
    checked_invariants: List[str] = Field(default_factory=list)
    verification_summary: str
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


def compute_proposal_digest(proposal: Proposal) -> str:
    """
    Computes a deterministic SHA-256 decision-payload integrity digest over all decision-relevant fields.
    Covers source assignment, physical movement, all milestone and completion ticks,
    freight cost (in integer cents), weighted lateness (in scaled integer units), and scheduled interval boundaries.
    Any alteration of these fields invalidates the verification certificate.
    Does NOT include verification_result or approval_status to avoid circularity and allow state transitions.
    """
    parts_freight_cents = int(round(float(proposal.parts_freight_cost) * 100))
    weighted_lateness_scaled = int(round(float(proposal.weighted_lateness_ticks) * 10000))

    sorted_intervals = [
        {
            "entity_type": str(iv.entity_type),
            "entity_id": str(iv.entity_id),
            "operation": str(iv.operation),
            "start_tick": int(iv.start_tick),
            "end_tick": int(iv.end_tick)
        }
        for iv in proposal.scheduled_intervals
    ]
    sorted_intervals.sort(
        key=lambda x: (x["entity_type"], x["entity_id"], x["start_tick"], x["end_tick"], x["operation"])
    )

    canonical_dict = {
        "proposal_id": str(proposal.proposal_id),
        "scenario_id": str(proposal.scenario_id),
        "policy_id": str(proposal.policy_id.value if hasattr(proposal.policy_id, "value") else proposal.policy_id),
        "input_snapshot_version": int(proposal.input_snapshot_version),
        "selected_source_id": str(proposal.selected_source_id) if proposal.selected_source_id is not None else None,
        "selected_source_name": str(proposal.selected_source_name) if proposal.selected_source_name is not None else None,
        "selected_movement": str(proposal.selected_movement),
        "b4_release_tick": int(proposal.b4_release_tick),
        "ro1042_finish_tick": int(proposal.ro1042_finish_tick),
        "ro1051_finish_tick": int(proposal.ro1051_finish_tick),
        "ro1042_lateness_ticks": int(proposal.ro1042_lateness_ticks),
        "ro1051_lateness_ticks": int(proposal.ro1051_lateness_ticks),
        "downstream_delay_minutes": int(proposal.downstream_delay_minutes),
        "parts_freight_cents": parts_freight_cents,
        "weighted_lateness_scaled": weighted_lateness_scaled,
        "solver_status": str(proposal.solver_status.value if hasattr(proposal.solver_status, "value") else proposal.solver_status),
        "pass1_status": str(proposal.pass1_status.value) if (proposal.pass1_status and hasattr(proposal.pass1_status, "value")) else (str(proposal.pass1_status) if proposal.pass1_status else None),
        "pass2_status": str(proposal.pass2_status.value) if (proposal.pass2_status and hasattr(proposal.pass2_status, "value")) else (str(proposal.pass2_status) if proposal.pass2_status else None),
        "scheduled_intervals": sorted_intervals
    }
    canonical_json = json.dumps(canonical_dict, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def verify_proposal(proposal: Proposal, snapshot: ScenarioSnapshot) -> VerificationResult:
    """
    Independently inspects an emitted Proposal against the immutable ScenarioSnapshot.
    Reconstructs facts from emitted decisions, scheduled intervals, and snapshot preconditions.
    Does NOT invoke OR-Tools or call any solver.
    """
    violations: List[VerificationViolation] = []
    checked_invariants: List[str] = []
    digest = compute_proposal_digest(proposal)
    cert_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"

    # -------------------------------------------------------------------------
    # Invariant 1: Scenario & Snapshot Version Context Binding
    # -------------------------------------------------------------------------
    inv_name = "INV-CONTEXT-BIND: Scenario Identity & Snapshot Version Match"
    checked_invariants.append(inv_name)
    if proposal.scenario_id != snapshot.scenario_id:
        violations.append(VerificationViolation(
            violation_code="SCENARIO_IDENTITY_MISMATCH",
            description=f"Proposal generated for scenario '{proposal.scenario_id}', but evaluated against '{snapshot.scenario_id}'.",
            entity_id=proposal.scenario_id
        ))
    if proposal.input_snapshot_version != snapshot.snapshot_version:
        violations.append(VerificationViolation(
            violation_code="SNAPSHOT_VERSION_MISMATCH",
            description=f"Proposal bound to snapshot version v{proposal.input_snapshot_version}, but current snapshot is v{snapshot.snapshot_version}.",
            entity_id=str(proposal.input_snapshot_version)
        ))

    # -------------------------------------------------------------------------
    # Invariant 2: Solver Feasibility Status Check
    # -------------------------------------------------------------------------
    inv_name = "INV-SOLVER-STATUS: Feasible/Optimal Solver State"
    checked_invariants.append(inv_name)
    if proposal.solver_status not in (SolverStatusEnum.OPTIMAL, SolverStatusEnum.FEASIBLE):
        violations.append(VerificationViolation(
            violation_code="SOLVER_STATUS_INFEASIBLE",
            description=f"Proposal reports non-feasible solver status '{proposal.solver_status.value}'. Infeasible solutions cannot be certified.",
            entity_id=proposal.proposal_id
        ))
        return VerificationResult(
            verification_status=VerificationStatus.REJECTED,
            proposal_id=proposal.proposal_id,
            scenario_id=snapshot.scenario_id,
            snapshot_version=snapshot.snapshot_version,
            proposal_digest=digest,
            certificate_id=cert_id,
            violations=violations,
            checked_invariants=checked_invariants,
            verification_summary=f"REJECTED: Solver reported non-feasible status '{proposal.solver_status.value}'."
        )

    # -------------------------------------------------------------------------
    # Invariant 3: Critical Evidence Completeness Check
    # -------------------------------------------------------------------------
    inv_name = "INV-EVIDENCE-COMPLETE: Critical Proposal Fields Present"
    checked_invariants.append(inv_name)
    if not proposal.selected_source_id or not proposal.scheduled_intervals:
        violations.append(VerificationViolation(
            violation_code="MISSING_CRITICAL_EVIDENCE",
            description="Proposal lacks selected source ID or scheduled intervals required for independent certificate verification.",
            entity_id=proposal.proposal_id
        ))
        return VerificationResult(
            verification_status=VerificationStatus.INSUFFICIENT_EVIDENCE,
            proposal_id=proposal.proposal_id,
            scenario_id=snapshot.scenario_id,
            snapshot_version=snapshot.snapshot_version,
            proposal_digest=digest,
            certificate_id=cert_id,
            violations=violations,
            checked_invariants=checked_invariants,
            verification_summary="Verification aborted: critical evidence missing from proposal payload."
        )

    # -------------------------------------------------------------------------
    # Invariant 4: Part Sourcing Existence & ATP Eligibility
    # -------------------------------------------------------------------------
    inv_name = "INV-SRC-ELIGIBILITY: Source Exists and Passes ATP/Fitment/Quote Gating"
    checked_invariants.append(inv_name)
    matching_sources = [s for s in snapshot.sources if s.source_id == proposal.selected_source_id]
    if not matching_sources:
        violations.append(VerificationViolation(
            violation_code="UNKNOWN_SOURCE_SELECTED",
            description=f"Selected source '{proposal.selected_source_id}' does not exist in scenario candidate source list.",
            entity_id=proposal.selected_source_id
        ))
        selected_source = None
    else:
        selected_source = matching_sources[0]
        # Check negative quantity
        if selected_source.atp < 0:
            violations.append(VerificationViolation(
                violation_code="NEGATIVE_INVENTORY",
                description=f"Source '{selected_source.source_id}' reports impossible negative ATP ({selected_source.atp}).",
                entity_id=selected_source.source_id
            ))
        elif selected_source.atp < 1:
            violations.append(VerificationViolation(
                violation_code="INSUFFICIENT_ATP",
                description=f"Source '{selected_source.source_id}' has ATP = {selected_source.atp}; cannot satisfy unit requirement.",
                entity_id=selected_source.source_id
            ))
        if not selected_source.fitment_verified:
            violations.append(VerificationViolation(
                violation_code="INVALID_FITMENT",
                description=f"Source '{selected_source.source_id}' part fitment is not verified for vehicle VIN.",
                entity_id=selected_source.source_id
            ))
        if not selected_source.quote_valid:
            violations.append(VerificationViolation(
                violation_code="EXPIRED_QUOTE",
                description=f"Source '{selected_source.source_id}' price/logistics quote has expired.",
                entity_id=selected_source.source_id
            ))
        if abs(proposal.parts_freight_cost - selected_source.cost) > 0.01:
            violations.append(VerificationViolation(
                violation_code="FREIGHT_COST_MISMATCH",
                description=f"Proposal reports freight cost ${proposal.parts_freight_cost:.2f}, but source '{selected_source.source_id}' cost is ${selected_source.cost:.2f}.",
                entity_id=selected_source.source_id
            ))

    # -------------------------------------------------------------------------
    # Invariant 5: Temporal Readiness - Installation Cannot Precede Usable Ready Time
    # -------------------------------------------------------------------------
    inv_name = "INV-TIME-READY: Part Installation Starts At Or After Usable Ready Tick"
    checked_invariants.append(inv_name)
    # Reconstruct RO-1042 install start from scheduled intervals
    ro1042_install_intervals = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "RO-1042" and ("Installation" in iv.operation or "Part" in iv.operation or "Install" in iv.operation)
    ]
    if ro1042_install_intervals and selected_source:
        actual_install_start = ro1042_install_intervals[0].start_tick
        if actual_install_start < selected_source.usable_time_ticks:
            violations.append(VerificationViolation(
                violation_code="INSTALL_BEFORE_PART_READY",
                description=(
                    f"RO-1042 installation scheduled to start at tick {actual_install_start}, "
                    f"prior to source '{selected_source.source_id}' usable-ready tick {selected_source.usable_time_ticks}."
                ),
                entity_id="RO-1042"
            ))

    # -------------------------------------------------------------------------
    # Invariant 6: Physical Vehicle Safety & Relocation Gating
    # -------------------------------------------------------------------------
    inv_name = "INV-SAFE-RELOC: Vehicle Mobility & Certified Signoff for Relocation"
    checked_invariants.append(inv_name)
    if proposal.selected_movement == "RELOCATE_TO_H2":
        ro = snapshot.ro1042
        if not ro.is_rollable or ro.current_vehicle_state == VehicleState.PARTIALLY_DISMANTLED:
            violations.append(VerificationViolation(
                violation_code="UNSAFE_RELOCATION_UNROLLABLE",
                description=(
                    f"Proposal relocated RO-1042, but vehicle is in state '{ro.current_vehicle_state.value}' "
                    f"with is_rollable={ro.is_rollable}. Physical movement violates safety Invariant CE-1."
                ),
                entity_id="RO-1042"
            ))
        if not ro.technician_signoff_recorded:
            violations.append(VerificationViolation(
                violation_code="MISSING_TECHNICIAN_SIGNOFF",
                description="Relocation selected without recorded certified technician safety signoff.",
                entity_id="RO-1042"
            ))
        if snapshot.h2_available_stalls < 1:
            violations.append(VerificationViolation(
                violation_code="HOLDING_CAPACITY_EXCEEDED",
                description=f"Relocation scheduled to H2, but available holding stalls is {snapshot.h2_available_stalls}.",
                entity_id="H2"
            ))

    # -------------------------------------------------------------------------
    # Invariant 7: Precedence, Bay Occupancy & Clearance Continuity
    # -------------------------------------------------------------------------
    inv_name = "INV-BAY-OCCUPANCY: Hoist Bay B4 Non-Overlapping Scheduling & Clearance"
    checked_invariants.append(inv_name)
    # Collect all intervals utilizing Bay B4
    bay_intervals = sorted(
        [iv for iv in proposal.scheduled_intervals if iv.entity_type in ("BAY", "JOB") and (iv.entity_id == "B4" or "Bay B4" in iv.operation or iv.entity_id in ("RO-1042", "RO-1051"))],
        key=lambda x: (x.start_tick, x.end_tick)
    )
    # Filter strictly to intervals occupying Bay B4 physically
    # In HOLD_ON_BAY: RO-1042 install -> RO-1042 clear -> RO-1051
    # Check that clearance exists and is not omitted
    clearance_intervals = [
        iv for iv in proposal.scheduled_intervals
        if "Clearance" in iv.operation or "clearance" in iv.operation.lower()
    ]
    if not clearance_intervals:
        violations.append(VerificationViolation(
            violation_code="CLEARANCE_OMITTED",
            description="Required post-service bay clearance interval was completely omitted from proposal schedule.",
            entity_id="B4"
        ))
    else:
        for civ in clearance_intervals:
            dur = civ.end_tick - civ.start_tick
            if dur < snapshot.clearance_duration_ticks:
                violations.append(VerificationViolation(
                    violation_code="CLEARANCE_SHORTENED",
                    description=f"Bay clearance duration ({dur} ticks) is less than facility requirement ({snapshot.clearance_duration_ticks} ticks).",
                    entity_id="B4"
                ))

    # Check pairwise non-overlap of active jobs on Bay B4
    active_job_intervals = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_type == "JOB" and iv.entity_id in ("RO-1042", "RO-1051") and "Clearance" not in iv.operation
    ]
    active_job_intervals.sort(key=lambda x: x.start_tick)
    for i in range(len(active_job_intervals) - 1):
        first = active_job_intervals[i]
        second = active_job_intervals[i + 1]
        # In HOLD_ON_BAY, between RO-1042 install and RO-1051, there must be clearance duration
        if proposal.selected_movement == "HOLD_ON_BAY":
            if second.start_tick < first.end_tick + snapshot.clearance_duration_ticks:
                violations.append(VerificationViolation(
                    violation_code="BAY_OCCUPANCY_OVERLAP",
                    description=(
                        f"Bay B4 active jobs overlap or lack mandatory clearance: "
                        f"{first.entity_id} ({first.start_tick}->{first.end_tick}) and "
                        f"{second.entity_id} ({second.start_tick}->{second.end_tick})."
                    ),
                    entity_id="B4"
                ))

    # -------------------------------------------------------------------------
    # Invariant 8: Resource / Technician Overlap
    # -------------------------------------------------------------------------
    inv_name = "INV-TECH-OVERLAP: No Overlapping Assignments on Constrained Technicians"
    checked_invariants.append(inv_name)
    # Check technician K2 availability constraint if present
    tech_k2_busy_until = snapshot.technician_k2_available_tick
    if tech_k2_busy_until is not None:
        ro1051_intervals = [iv for iv in proposal.scheduled_intervals if iv.entity_id == "RO-1051" and iv.entity_type == "JOB"]
        if ro1051_intervals:
            ro1051_start = ro1051_intervals[0].start_tick
            if ro1051_start < tech_k2_busy_until:
                violations.append(VerificationViolation(
                    violation_code="TECHNICIAN_OVERLAP",
                    description=(
                        f"RO-1051 assigned to Tech K2 starts at tick {ro1051_start}, "
                        f"violating Tech K2 preceding commitment busy until tick {tech_k2_busy_until}."
                    ),
                    entity_id="K2"
                ))

    # -------------------------------------------------------------------------
    # Invariant 9: Customer Promise & Lateness Arithmetic Verification
    # -------------------------------------------------------------------------
    inv_name = "INV-LATENESS-MATH: Independent Verification of Objective Functions"
    checked_invariants.append(inv_name)
    p_1042 = snapshot.ro1042.promise_ticks
    p_1051 = snapshot.ro1051.promise_ticks
    w_1042 = snapshot.ro1042.priority_weight
    w_1051 = snapshot.ro1051.priority_weight

    expected_lateness_1042 = max(0, proposal.ro1042_finish_tick - p_1042)
    expected_lateness_1051 = max(0, proposal.ro1051_finish_tick - p_1051)
    expected_weighted_lateness = float(w_1042 * expected_lateness_1042 + w_1051 * expected_lateness_1051)

    if proposal.ro1042_lateness_ticks != expected_lateness_1042:
        violations.append(VerificationViolation(
            violation_code="LATENESS_ARITHMETIC_MISMATCH",
            description=(
                f"RO-1042 lateness mismatch: proposal reports {proposal.ro1042_lateness_ticks} ticks, "
                f"but finish tick {proposal.ro1042_finish_tick} - promise {p_1042} = {expected_lateness_1042} ticks."
            ),
            entity_id="RO-1042"
        ))

    if proposal.ro1051_lateness_ticks != expected_lateness_1051:
        violations.append(VerificationViolation(
            violation_code="LATENESS_ARITHMETIC_MISMATCH",
            description=(
                f"RO-1051 lateness mismatch: proposal reports {proposal.ro1051_lateness_ticks} ticks, "
                f"but finish tick {proposal.ro1051_finish_tick} - promise {p_1051} = {expected_lateness_1051} ticks."
            ),
            entity_id="RO-1051"
        ))

    if abs(proposal.weighted_lateness_ticks - expected_weighted_lateness) > 0.001:
        violations.append(VerificationViolation(
            violation_code="WEIGHTED_LATENESS_MISMATCH",
            description=(
                f"Weighted lateness mismatch: proposal reports {proposal.weighted_lateness_ticks:.1f} ticks, "
                f"but independent arithmetic yields {expected_weighted_lateness:.1f} ticks."
            ),
            entity_id=proposal.proposal_id
        ))

    # -------------------------------------------------------------------------
    # Synthesize Final Verdict
    # -------------------------------------------------------------------------
    if violations:
        status = VerificationStatus.REJECTED
        summary = f"REJECTED: Proposal failed {len(violations)} independent invariant check(s)."
    else:
        status = VerificationStatus.VERIFIED
        summary = f"VERIFIED: Proposal successfully certified across all {len(checked_invariants)} independent physical and temporal invariants."

    return VerificationResult(
        verification_status=status,
        proposal_id=proposal.proposal_id,
        scenario_id=snapshot.scenario_id,
        snapshot_version=snapshot.snapshot_version,
        proposal_digest=digest,
        certificate_id=cert_id,
        violations=violations,
        checked_invariants=checked_invariants,
        verification_summary=summary
    )


def validate_proposal_certificate(
    proposal: Proposal,
    snapshot: ScenarioSnapshot
) -> Tuple[bool, Optional[str], Optional[VerificationResult]]:
    """
    Validates certificate binding and executes commit-time independent reverification.
    Returns (is_valid, failure_code_or_reason, reverified_result).
    """
    cert = proposal.verification_result
    if not cert:
        return False, "MISSING_CERTIFICATE", None

    # Check status in certificate
    cert_status = cert.get("verification_status") if isinstance(cert, dict) else cert.verification_status.value
    if cert_status != VerificationStatus.VERIFIED.value:
        return False, "CERTIFICATE_NOT_VERIFIED", None

    # Anti-tampering check: verify proposal decision digest
    recorded_digest = cert.get("proposal_digest") if isinstance(cert, dict) else cert.proposal_digest
    current_digest = compute_proposal_digest(proposal)
    if recorded_digest != current_digest:
        return False, "CERTIFICATE_TAMPERED", None

    # Immediate commit-time invariant verification against live immutable snapshot
    commit_v_res = verify_proposal(proposal, snapshot)
    if commit_v_res.verification_status != VerificationStatus.VERIFIED:
        return False, "COMMIT_VERIFICATION_FAILED", commit_v_res

    return True, None, commit_v_res

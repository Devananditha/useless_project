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
    skipped_checks: List[str] = Field(default_factory=list)
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
    skipped_checks: List[str] = []
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
            skipped_checks=skipped_checks,
            verification_summary=f"REJECTED: Solver reported non-feasible status '{proposal.solver_status.value}'."
        )

    # -------------------------------------------------------------------------
    # Invariant 3: Critical & Mandatory Evidence Completeness
    # -------------------------------------------------------------------------
    inv_name = "INV-EVIDENCE-COMPLETE: Critical & Mandatory Schedule Events Present"
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
            skipped_checks=skipped_checks,
            verification_summary="INSUFFICIENT_EVIDENCE: Critical proposal evidence missing."
        )

    # Semantic classification of emitted schedule intervals
    ro1042_install = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "RO-1042" and iv.entity_type == "JOB" and (
            "Part Installation" in iv.operation or "Install" in iv.operation or "Installation" in iv.operation
        )
    ]
    ro1042_clearance = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "RO-1042" and ("Clearance" in iv.operation or "clearance" in iv.operation.lower())
    ]
    ro1051_service = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "RO-1051" and iv.entity_type == "JOB" and "Clearance" not in iv.operation
    ]
    outbound_transit = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "RO-1042" and iv.entity_type == "TRANSIT" and (
            "Holding H2" in iv.operation or "to Holding H2" in iv.operation or "Transit from Bay B4" in iv.operation
        )
    ]
    h2_holding = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "H2" and iv.entity_type == "HOLDING"
    ]
    ro1051_clearance = [
        iv for iv in proposal.scheduled_intervals
        if ("Clearance" in iv.operation and ("RO-1051" in iv.operation or iv.entity_id == "B4"))
    ]
    return_transit = [
        iv for iv in proposal.scheduled_intervals
        if iv.entity_id == "RO-1042" and iv.entity_type == "TRANSIT" and (
            "Return" in iv.operation or "H2 to Bay B4" in iv.operation
        )
    ]

    # Explicit mandatory event presence checks per movement mode
    if proposal.selected_movement == "HOLD_ON_BAY":
        if not ro1042_install:
            violations.append(VerificationViolation(
                violation_code="MISSING_RO1042_INSTALL_INTERVAL",
                description="Required RO-1042 part installation interval is missing from proposal schedule.",
                entity_id="RO-1042"
            ))
        if not ro1042_clearance:
            violations.append(VerificationViolation(
                violation_code="MISSING_RO1042_CLEARANCE_INTERVAL",
                description="Required RO-1042 bay clearance interval is missing from proposal schedule.",
                entity_id="RO-1042"
            ))
        if not ro1051_service:
            violations.append(VerificationViolation(
                violation_code="MISSING_RO1051_SERVICE_INTERVAL",
                description="Required RO-1051 service interval is missing from proposal schedule.",
                entity_id="RO-1051"
            ))
    elif proposal.selected_movement == "RELOCATE_TO_H2":
        # Always check physical safety for relocation attempts regardless of intervals present
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

        if not outbound_transit:
            violations.append(VerificationViolation(
                violation_code="MISSING_OUTBOUND_TRANSIT_INTERVAL",
                description="Required outbound relocation transit interval to H2 is missing from proposal schedule.",
                entity_id="RO-1042"
            ))
        if not h2_holding:
            violations.append(VerificationViolation(
                violation_code="MISSING_H2_HOLDING_INTERVAL",
                description="Required H2 holding staging interval is missing from proposal schedule.",
                entity_id="H2"
            ))
        if not ro1051_service:
            violations.append(VerificationViolation(
                violation_code="MISSING_RO1051_SERVICE_INTERVAL",
                description="Required RO-1051 fleet service interval is missing from proposal schedule.",
                entity_id="RO-1051"
            ))
        if not ro1051_clearance:
            violations.append(VerificationViolation(
                violation_code="MISSING_RO1051_CLEARANCE_INTERVAL",
                description="Required RO-1051 post-service clearance interval is missing from proposal schedule.",
                entity_id="B4"
            ))
        if not return_transit:
            violations.append(VerificationViolation(
                violation_code="MISSING_RETURN_TRANSIT_INTERVAL",
                description="Required return transit interval from H2 to Bay B4 is missing from proposal schedule.",
                entity_id="RO-1042"
            ))
        if not ro1042_install:
            violations.append(VerificationViolation(
                violation_code="MISSING_RO1042_INSTALL_INTERVAL",
                description="Required RO-1042 installation interval upon return is missing from proposal schedule.",
                entity_id="RO-1042"
            ))
        if not ro1042_clearance:
            violations.append(VerificationViolation(
                violation_code="MISSING_FINAL_CLEARANCE_INTERVAL",
                description="Required final RO-1042 clearance interval is missing from proposal schedule.",
                entity_id="RO-1042"
            ))

    # Fail closed on missing mandatory schedule evidence if no other physical safety violation occurred
    missing_codes = [v.violation_code for v in violations if v.violation_code.startswith("MISSING_")]
    has_rejection_fault = any(
        not v.violation_code.startswith("MISSING_") for v in violations
    )
    if missing_codes:
        final_status = VerificationStatus.REJECTED if has_rejection_fault else VerificationStatus.INSUFFICIENT_EVIDENCE
        summary_prefix = "REJECTED" if has_rejection_fault else "INSUFFICIENT_EVIDENCE"
        return VerificationResult(
            verification_status=final_status,
            proposal_id=proposal.proposal_id,
            scenario_id=snapshot.scenario_id,
            snapshot_version=snapshot.snapshot_version,
            proposal_digest=digest,
            certificate_id=cert_id,
            violations=violations,
            checked_invariants=checked_invariants,
            skipped_checks=skipped_checks,
            verification_summary=f"{summary_prefix}: Proposal failed validation (missing schedule evidence: {missing_codes})."
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
    # Invariant 5 & 6: Movement Sequence & Chronological Reconstruction
    # -------------------------------------------------------------------------
    recon_ro1042_finish: int = proposal.ro1042_finish_tick
    recon_ro1051_finish: int = proposal.ro1051_finish_tick

    if proposal.selected_movement == "HOLD_ON_BAY":
        checked_invariants.append("INV-TIME-READY: Part Arrival Respects Usable Ready Tick")
        checked_invariants.append("INV-BAY-OCCUPANCY: Bay B4 Mutual Exclusion & Clearance")
        checked_invariants.append("INV-SCHEDULE-CHRONOLOGY: Ordered Non-Overlapping Operations")
        checked_invariants.append("INV-MILESTONE-RECONSTRUCTION: Completion Milestones Reconstructed")
        skipped_checks.append("INV-RELOC-TIMELINE: Not applicable in HOLD_ON_BAY movement mode")

        inst = ro1042_install[0]
        clr = ro1042_clearance[0]
        srv = ro1051_service[0]

        # 1. Part readiness
        if selected_source and inst.start_tick < selected_source.usable_time_ticks:
            violations.append(VerificationViolation(
                violation_code="INSTALL_BEFORE_PART_READY",
                description=(
                    f"RO-1042 installation scheduled to start at tick {inst.start_tick}, "
                    f"prior to source '{selected_source.source_id}' usable-ready tick {selected_source.usable_time_ticks}."
                ),
                entity_id="RO-1042"
            ))
        if inst.start_tick < snapshot.current_tick:
            violations.append(VerificationViolation(
                violation_code="EVENT_BEFORE_CURRENT_TIME",
                description=f"RO-1042 installation scheduled at tick {inst.start_tick}, before snapshot current tick {snapshot.current_tick}.",
                entity_id="RO-1042"
            ))

        # 2. Installation duration
        dur_inst = inst.end_tick - inst.start_tick
        if dur_inst != snapshot.ro1042.service_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="INSTALL_DURATION_MISMATCH",
                description=f"RO-1042 installation duration ({dur_inst} ticks) != requirement ({snapshot.ro1042.service_duration_ticks} ticks).",
                entity_id="RO-1042"
            ))

        # 3. Clearance continuity
        if clr.start_tick != inst.end_tick:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_DISCONTINUITY",
                description=f"RO-1042 clearance start (tick {clr.start_tick}) does not match installation finish (tick {inst.end_tick}).",
                entity_id="RO-1042"
            ))

        # 4. Clearance duration
        dur_clr = clr.end_tick - clr.start_tick
        if dur_clr < snapshot.clearance_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_SHORTENED",
                description=f"Bay clearance duration ({dur_clr} ticks) < facility requirement ({snapshot.clearance_duration_ticks} ticks).",
                entity_id="B4"
            ))

        # 5. RO-1042 finish tick reconstruction
        recon_ro1042_finish = clr.end_tick
        if proposal.ro1042_finish_tick != recon_ro1042_finish:
            violations.append(VerificationViolation(
                violation_code="RO1042_FINISH_MISMATCH",
                description=f"Proposal reports RO-1042 finish at tick {proposal.ro1042_finish_tick}, but reconstructed clearance ends at tick {recon_ro1042_finish}.",
                entity_id="RO-1042"
            ))

        # 6. Bay B4 first release reconstruction
        recon_b4_release = clr.end_tick
        if proposal.b4_release_tick != recon_b4_release:
            violations.append(VerificationViolation(
                violation_code="B4_RELEASE_MISMATCH",
                description=f"Proposal reports Bay B4 release at tick {proposal.b4_release_tick}, but physical clearance ends at tick {recon_b4_release}.",
                entity_id="B4"
            ))

        # 7. RO-1051 start precedence
        if srv.start_tick < recon_b4_release:
            violations.append(VerificationViolation(
                violation_code="BAY_OCCUPANCY_OVERLAP",
                description=(
                    f"RO-1051 starts at tick {srv.start_tick} on Bay B4 before RO-1042 clears the hoist at tick {recon_b4_release}."
                ),
                entity_id="B4"
            ))

        # 8. RO-1051 service duration
        dur_srv = srv.end_tick - srv.start_tick
        if dur_srv != snapshot.ro1051.service_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="SERVICE_DURATION_MISMATCH",
                description=f"RO-1051 service duration ({dur_srv} ticks) != requirement ({snapshot.ro1051.service_duration_ticks} ticks).",
                entity_id="RO-1051"
            ))

        # 9. RO-1051 finish tick reconstruction
        recon_ro1051_finish = srv.end_tick
        if proposal.ro1051_finish_tick != recon_ro1051_finish:
            violations.append(VerificationViolation(
                violation_code="RO1051_FINISH_MISMATCH",
                description=f"Proposal reports RO-1051 finish at tick {proposal.ro1051_finish_tick}, but reconstructed service ends at tick {recon_ro1051_finish}.",
                entity_id="RO-1051"
            ))

        # 10. Technician constraint
        tech_avail = snapshot.technician_k2_available_tick or snapshot.ro1051.technician_available_tick
        if tech_avail is not None:
            checked_invariants.append("INV-TECH-CONSTRAINTS: Technician K2 Availability Constraint")
            if srv.start_tick < tech_avail:
                violations.append(VerificationViolation(
                    violation_code="TECHNICIAN_OVERLAP",
                    description=f"RO-1051 starts at tick {srv.start_tick}, violating Tech K2 availability at tick {tech_avail}.",
                    entity_id="K2"
                ))
        else:
            skipped_checks.append("INV-TECH-CONSTRAINTS: Unconstrained technician pool in active scenario")

    elif proposal.selected_movement == "RELOCATE_TO_H2":
        inv_name = "INV-SAFE-RELOC: Vehicle Mobility & Certified Signoff for Relocation"
        checked_invariants.append(inv_name)

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

        checked_invariants.append("INV-RELOC-TIMELINE: Full Outbound, Staging, Return & Reassembly Sequence")
        checked_invariants.append("INV-TIME-READY: Part Arrival Respects Usable Ready Tick")
        checked_invariants.append("INV-BAY-OCCUPANCY: Bay B4 Mutual Exclusion & Clearance")
        checked_invariants.append("INV-SCHEDULE-CHRONOLOGY: Ordered Non-Overlapping Operations")
        checked_invariants.append("INV-MILESTONE-RECONSTRUCTION: Completion Milestones Reconstructed")

        out = outbound_transit[0]
        srv = ro1051_service[0]
        srv_clr = ro1051_clearance[0]
        hold = h2_holding[0]
        ret = return_transit[0]
        inst = ro1042_install[0]
        clr = ro1042_clearance[0]

        # 1. Outbound transit start & duration
        if out.start_tick < snapshot.current_tick:
            violations.append(VerificationViolation(
                violation_code="EVENT_BEFORE_CURRENT_TIME",
                description=f"Outbound transit scheduled at tick {out.start_tick}, before snapshot current tick {snapshot.current_tick}.",
                entity_id="RO-1042"
            ))
        dur_out = out.end_tick - out.start_tick
        if dur_out < snapshot.relocation_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="RELOCATION_TRANSIT_SHORTENED",
                description=f"Outbound relocation transit duration ({dur_out} ticks) < facility requirement ({snapshot.relocation_duration_ticks} ticks).",
                entity_id="RO-1042"
            ))
        elif dur_out != snapshot.relocation_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="RELOCATION_TRANSIT_DURATION_MISMATCH",
                description=f"Outbound relocation duration ({dur_out} ticks) != requirement ({snapshot.relocation_duration_ticks} ticks).",
                entity_id="RO-1042"
            ))

        # 2. Reconstructed Bay B4 first release
        recon_b4_release = out.end_tick
        if proposal.b4_release_tick != recon_b4_release:
            violations.append(VerificationViolation(
                violation_code="B4_RELEASE_MISMATCH",
                description=f"Proposal reports Bay B4 release at tick {proposal.b4_release_tick}, but physical outbound transit ends at tick {recon_b4_release}.",
                entity_id="B4"
            ))

        # 3. RO-1051 start on Bay B4
        if srv.start_tick < out.end_tick:
            violations.append(VerificationViolation(
                violation_code="BAY_OCCUPANCY_OVERLAP",
                description=(
                    f"RO-1051 starts at tick {srv.start_tick} on Bay B4 before RO-1042 clears the bay at tick {out.end_tick}."
                ),
                entity_id="B4"
            ))

        # Technician check
        tech_avail = snapshot.technician_k2_available_tick or snapshot.ro1051.technician_available_tick
        if tech_avail is not None:
            checked_invariants.append("INV-TECH-CONSTRAINTS: Technician K2 Availability Constraint")
            if srv.start_tick < tech_avail:
                violations.append(VerificationViolation(
                    violation_code="TECHNICIAN_OVERLAP",
                    description=f"RO-1051 starts at tick {srv.start_tick}, violating Tech K2 availability at tick {tech_avail}.",
                    entity_id="K2"
                ))
        else:
            skipped_checks.append("INV-TECH-CONSTRAINTS: Unconstrained technician pool in active scenario")

        # 4. RO-1051 duration & finish reconstruction
        dur_srv = srv.end_tick - srv.start_tick
        if dur_srv != snapshot.ro1051.service_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="SERVICE_DURATION_MISMATCH",
                description=f"RO-1051 service duration ({dur_srv} ticks) != requirement ({snapshot.ro1051.service_duration_ticks} ticks).",
                entity_id="RO-1051"
            ))
        recon_ro1051_finish = srv.end_tick
        if proposal.ro1051_finish_tick != recon_ro1051_finish:
            violations.append(VerificationViolation(
                violation_code="RO1051_FINISH_MISMATCH",
                description=f"Proposal reports RO-1051 finish at tick {proposal.ro1051_finish_tick}, but reconstructed service ends at tick {recon_ro1051_finish}.",
                entity_id="RO-1051"
            ))

        # 5. RO-1051 clearance continuity & duration
        if srv_clr.start_tick != srv.end_tick:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_DISCONTINUITY",
                description=f"RO-1051 clearance start (tick {srv_clr.start_tick}) does not match service end (tick {srv.end_tick}).",
                entity_id="B4"
            ))
        dur_srv_clr = srv_clr.end_tick - srv_clr.start_tick
        if dur_srv_clr < snapshot.clearance_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_SHORTENED",
                description=f"RO-1051 post-service clearance duration ({dur_srv_clr} ticks) < facility requirement ({snapshot.clearance_duration_ticks} ticks).",
                entity_id="B4"
            ))
        b4_free_after_1051 = srv_clr.end_tick

        # 6. Holding stage continuity
        if hold.start_tick != out.end_tick:
            violations.append(VerificationViolation(
                violation_code="HOLDING_CHRONOLOGY_INVALID",
                description=f"H2 holding start (tick {hold.start_tick}) does not match outbound transit arrival (tick {out.end_tick}).",
                entity_id="H2"
            ))
        if hold.end_tick != ret.start_tick:
            violations.append(VerificationViolation(
                violation_code="HOLDING_CHRONOLOGY_INVALID",
                description=f"H2 holding end (tick {hold.end_tick}) does not match return transit departure (tick {ret.start_tick}).",
                entity_id="H2"
            ))

        # 7. Return transit start precedence
        if ret.start_tick < b4_free_after_1051:
            violations.append(VerificationViolation(
                violation_code="RETURN_BEFORE_BAY_AVAILABLE",
                description=(
                    f"Return transit begins at tick {ret.start_tick} before Bay B4 is cleared by RO-1051 at tick {b4_free_after_1051}."
                ),
                entity_id="RO-1042"
            ))

        # 8. Return transit duration
        dur_ret = ret.end_tick - ret.start_tick
        if dur_ret < snapshot.relocation_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="RELOCATION_TRANSIT_SHORTENED",
                description=f"Return transit duration ({dur_ret} ticks) < facility requirement ({snapshot.relocation_duration_ticks} ticks).",
                entity_id="RO-1042"
            ))
        elif dur_ret != snapshot.relocation_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="RELOCATION_TRANSIT_DURATION_MISMATCH",
                description=f"Return transit duration ({dur_ret} ticks) != requirement ({snapshot.relocation_duration_ticks} ticks).",
                entity_id="RO-1042"
            ))

        # 9. RO-1042 installation after return
        if inst.start_tick < ret.end_tick:
            violations.append(VerificationViolation(
                violation_code="INSTALL_BEFORE_VEHICLE_RETURN",
                description=f"RO-1042 installation starts at tick {inst.start_tick} before vehicle return transit arrival at tick {ret.end_tick}.",
                entity_id="RO-1042"
            ))
        elif inst.start_tick != ret.end_tick:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_DISCONTINUITY",
                description=f"RO-1042 installation start (tick {inst.start_tick}) does not match vehicle return arrival (tick {ret.end_tick}).",
                entity_id="RO-1042"
            ))
        if selected_source and inst.start_tick < selected_source.usable_time_ticks:
            violations.append(VerificationViolation(
                violation_code="INSTALL_BEFORE_PART_READY",
                description=(
                    f"RO-1042 installation scheduled to start at tick {inst.start_tick}, "
                    f"prior to source '{selected_source.source_id}' usable-ready tick {selected_source.usable_time_ticks}."
                ),
                entity_id="RO-1042"
            ))
        dur_inst = inst.end_tick - inst.start_tick
        if dur_inst != snapshot.ro1042.service_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="INSTALL_DURATION_MISMATCH",
                description=f"RO-1042 installation duration ({dur_inst} ticks) != requirement ({snapshot.ro1042.service_duration_ticks} ticks).",
                entity_id="RO-1042"
            ))

        # 10. Final clearance continuity & duration
        if clr.start_tick != inst.end_tick:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_DISCONTINUITY",
                description=f"Final clearance start (tick {clr.start_tick}) does not match installation finish (tick {inst.end_tick}).",
                entity_id="RO-1042"
            ))
        dur_clr = clr.end_tick - clr.start_tick
        if dur_clr < snapshot.clearance_duration_ticks:
            violations.append(VerificationViolation(
                violation_code="CLEARANCE_SHORTENED",
                description=f"Final bay clearance duration ({dur_clr} ticks) < facility requirement ({snapshot.clearance_duration_ticks} ticks).",
                entity_id="B4"
            ))

        # Reconstructed RO-1042 finish
        recon_ro1042_finish = clr.end_tick
        if proposal.ro1042_finish_tick != recon_ro1042_finish:
            violations.append(VerificationViolation(
                violation_code="RO1042_FINISH_MISMATCH",
                description=f"Proposal reports RO-1042 finish at tick {proposal.ro1042_finish_tick}, but reconstructed clearance ends at tick {recon_ro1042_finish}.",
                entity_id="RO-1042"
            ))

    # -------------------------------------------------------------------------
    # Invariant 7: Independent Lateness & Objective Function Calculation
    # -------------------------------------------------------------------------
    inv_name = "INV-LATENESS-RECONSTRUCTION: Independent Objective Function Calculation"
    checked_invariants.append(inv_name)

    p_1042 = snapshot.ro1042.promise_ticks
    p_1051 = snapshot.ro1051.promise_ticks
    w_1042 = snapshot.ro1042.priority_weight
    w_1051 = snapshot.ro1051.priority_weight

    expected_lateness_1042 = max(0, recon_ro1042_finish - p_1042)
    expected_lateness_1051 = max(0, recon_ro1051_finish - p_1051)
    expected_weighted_lateness = float(w_1042 * expected_lateness_1042 + w_1051 * expected_lateness_1051)

    if proposal.ro1042_lateness_ticks != expected_lateness_1042:
        violations.append(VerificationViolation(
            violation_code="LATENESS_ARITHMETIC_MISMATCH",
            description=(
                f"RO-1042 lateness mismatch: proposal reports {proposal.ro1042_lateness_ticks} ticks, "
                f"but finish tick {recon_ro1042_finish} - promise {p_1042} = {expected_lateness_1042} ticks."
            ),
            entity_id="RO-1042"
        ))

    if proposal.ro1051_lateness_ticks != expected_lateness_1051:
        violations.append(VerificationViolation(
            violation_code="LATENESS_ARITHMETIC_MISMATCH",
            description=(
                f"RO-1051 lateness mismatch: proposal reports {proposal.ro1051_lateness_ticks} ticks, "
                f"but finish tick {recon_ro1051_finish} - promise {p_1051} = {expected_lateness_1051} ticks."
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
        summary = f"VERIFIED: Proposal certified across {len(checked_invariants)} physical and temporal invariants."

    return VerificationResult(
        verification_status=status,
        proposal_id=proposal.proposal_id,
        scenario_id=snapshot.scenario_id,
        snapshot_version=snapshot.snapshot_version,
        proposal_digest=digest,
        certificate_id=cert_id,
        violations=violations,
        checked_invariants=checked_invariants,
        skipped_checks=skipped_checks,
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

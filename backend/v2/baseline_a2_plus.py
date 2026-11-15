"""
StallBreaker 2.0 — V2 Research Baseline
Module: baseline_a2_plus.py

Implementation of the study-defined A2+ deterministic single-next-RO lookahead heuristic.
Provides an independent, pure-Python baseline evaluating candidate part sources against
immediate downstream bottleneck repair orders without invoking mixed-integer solvers (CP-SAT).

Conforms strictly to:
- docs/STALLBREAKER2_PHASED_BUILD_PLAN.md (Sections 6.1, 6.2, 6.3)
- Tekion Hackathon 2026 Theme 1, UC04 specifications
"""

import time
from typing import List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field

from backend.models import (
    ScenarioSnapshot,
    PartSource,
    VehicleState,
    ScheduledInterval,
    RejectedOption,
    Proposal,
    PolicyId,
    SolverStatusEnum,
    ApprovalStatus
)
from backend.eligibility import validate_source_eligibility
from backend.fixtures import tick_to_clock


# -----------------------------------------------------------------------------
# 1. Dedicated V2 Data Models
# -----------------------------------------------------------------------------

class A2PlusCandidatePlan(BaseModel):
    """Evaluation record of a single eligible candidate part source under A2+ lookahead."""
    source_id: str = Field(..., description="Part source identifier (e.g. S1, S2)")
    source_name: str = Field(..., description="Supplier description")
    source_cost: float = Field(..., description="Landed freight/procurement cost ($)")
    usable_time_ticks: int = Field(..., description="Tick at which part is on-site and usable")
    freight_delta_from_cheapest: float = Field(default=0.0, description="Additional cost over cheapest source ($)")
    selected_movement: str = Field(..., description="HOLD_ON_BAY or RELOCATE_TO_H2")
    
    # Milestone and finish ticks
    b4_release_tick: int
    b4_release_clock: str
    ro1042_finish_tick: int
    ro1042_finish_clock: str
    ro1051_finish_tick: int
    ro1051_finish_clock: str
    
    # Lateness and objective metrics
    ro1042_lateness_ticks: int
    ro1051_lateness_ticks: int
    weighted_lateness: float
    downstream_delay_minutes: int
    
    # Qualification status
    qualifies_for_upgrade: bool = False
    disqualification_reason: Optional[str] = None
    scheduled_intervals: List[ScheduledInterval] = Field(default_factory=list)


class A2PlusDecision(BaseModel):
    """
    Dedicated typed result model for A2+ deterministic lookahead heuristic decisions.
    Conforms to Stage 3 architectural boundaries and provides strict heuristic labeling.
    """
    decision_id: str = Field(..., description="Deterministic decision identifier")
    scenario_id: str = Field(..., description="Scenario identifier e.g. S-MATH-01")
    snapshot_version: int = Field(..., description="Input snapshot version number")
    policy: str = Field(default="A2_PLUS", description="Policy designation")
    status: str = Field(default="HEURISTIC", description="HEURISTIC, FEASIBLE, or INFEASIBLE")
    is_feasible: bool = Field(default=True, description="Whether a valid feasible schedule was derived")
    
    # Sourcing & movement decisions
    selected_source_id: Optional[str] = None
    selected_source_name: Optional[str] = None
    selected_movement: str = "HOLD_ON_BAY"
    
    # Critical timestamps & milestones
    b4_release_tick: Optional[int] = None
    b4_release_clock: Optional[str] = None
    ro1042_finish_tick: Optional[int] = None
    ro1042_finish_clock: Optional[str] = None
    ro1051_finish_tick: Optional[int] = None
    ro1051_finish_clock: Optional[str] = None
    
    # Objective metrics
    ro1042_lateness_ticks: Optional[int] = None
    ro1051_lateness_ticks: Optional[int] = None
    weighted_lateness: Optional[float] = None
    downstream_delay_minutes: Optional[int] = None
    freight_cost: Optional[float] = None
    max_freight_budget_delta: float = 50.0
    
    # Lookahead evaluation ledger
    candidate_evaluations: List[A2PlusCandidatePlan] = Field(default_factory=list)
    selection_explanations: List[str] = Field(default_factory=list)
    scheduled_intervals: List[ScheduledInterval] = Field(default_factory=list)
    rejected_options: List[RejectedOption] = Field(default_factory=list)
    solve_time_ms: float = 0.0


# -----------------------------------------------------------------------------
# 2. Physical Relocation Gating
# -----------------------------------------------------------------------------

def check_a2_plus_relocation_gating(snapshot: ScenarioSnapshot) -> Tuple[bool, List[RejectedOption]]:
    """
    Evaluates physical relocation preconditions for RO-1042.
    Relocation to Holding Location H2 is permitted ONLY when:
    1. RO-1042 is physically rollable (is_rollable == True).
    2. Vehicle state is not PARTIALLY_DISMANTLED.
    3. Certified technician safety sign-off is recorded.
    4. Holding Location H2 has at least one available stall (h2_available_stalls >= 1).

    If any condition fails, returns (False, rejections), dictating HOLD_ON_BAY.
    """
    rejections: List[RejectedOption] = []
    ro = snapshot.ro1042

    if not ro.is_rollable:
        rejections.append(RejectedOption(
            candidate_id="RELOCATE_TO_H2",
            reason_code="VEHICLE_NOT_ROLLABLE",
            description=f"RO-1042 has is_rollable=False. Vehicle cannot physically roll off Bay B4."
        ))

    if ro.current_vehicle_state == VehicleState.PARTIALLY_DISMANTLED:
        rejections.append(RejectedOption(
            candidate_id="RELOCATE_TO_H2",
            reason_code="VEHICLE_PARTIALLY_DISMANTLED",
            description="Vehicle is in PARTIALLY_DISMANTLED state on Bay B4 alignment hoist (Invariant CE-1)."
        ))

    if not ro.technician_signoff_recorded:
        rejections.append(RejectedOption(
            candidate_id="RELOCATE_TO_H2",
            reason_code="MISSING_TECHNICIAN_SIGNOFF",
            description="Digital certified technician safety sign-off is not recorded."
        ))

    if snapshot.h2_available_stalls < 1:
        rejections.append(RejectedOption(
            candidate_id="RELOCATE_TO_H2",
            reason_code="HOLDING_CAPACITY_EXCEEDED",
            description=(
                f"Holding location H2 has {snapshot.h2_available_stalls} available stalls "
                f"(Capacity: {snapshot.h2_capacity}). Saturated buffer blocks vehicle staging."
            )
        ))

    return (len(rejections) == 0, rejections)


# -----------------------------------------------------------------------------
# 3. Pure-Python Deterministic Schedule Evaluator
# -----------------------------------------------------------------------------

def evaluate_deterministic_schedule(
    snapshot: ScenarioSnapshot,
    source: PartSource,
    movement: str
) -> A2PlusCandidatePlan:
    """
    Pure-Python deterministic schedule simulator for a given candidate part source and movement mode.
    Constructs the exact chronological milestone sequence, resolves technician constraints,
    generates all physical ScheduledIntervals, and calculates weighted lateness.
    Does NOT call OR-Tools or CP-SAT.
    """
    current_t = snapshot.current_tick
    reloc_out_dur = snapshot.relocation_duration_ticks
    clear_dur = snapshot.clearance_duration_ticks
    ro1042_dur = snapshot.ro1042.service_duration_ticks
    ro1051_dur = snapshot.ro1051.service_duration_ticks

    # Technician availability resolution (explicit None check conforming to Stage 2.2.2 semantics)
    tech_avail = (
        snapshot.technician_k2_available_tick
        if snapshot.technician_k2_available_tick is not None
        else snapshot.ro1051.technician_available_tick
    )

    scheduled_intervals: List[ScheduledInterval] = []

    if movement == "HOLD_ON_BAY":
        # Vehicle remains on Bay B4
        install_start = max(current_t, source.usable_time_ticks)
        install_end = install_start + ro1042_dur
        clear_end = install_end + clear_dur
        
        b4_first_release = clear_end
        ro1042_finish = clear_end

        # RO-1051 start on B4 respects technician availability
        if tech_avail is not None:
            ro1051_start = max(b4_first_release, int(tech_avail))
        else:
            ro1051_start = b4_first_release
        
        ro1051_finish = ro1051_start + ro1051_dur

        # Build intervals
        if install_start > current_t:
            scheduled_intervals.append(ScheduledInterval(
                entity_type="BAY",
                entity_id="B4",
                operation="Bay B4: Stalled Waiting for Part",
                start_tick=current_t,
                end_tick=install_start,
                start_clock=tick_to_clock(current_t),
                end_clock=tick_to_clock(install_start)
            ))

        scheduled_intervals.append(ScheduledInterval(
            entity_type="JOB",
            entity_id="RO-1042",
            operation="RO-1042: Part Installation (Tech K1)",
            start_tick=install_start,
            end_tick=install_end,
            start_clock=tick_to_clock(install_start),
            end_clock=tick_to_clock(install_end)
        ))

        scheduled_intervals.append(ScheduledInterval(
            entity_type="JOB",
            entity_id="RO-1042",
            operation="RO-1042: Final Verification & Bay Clearance",
            start_tick=install_end,
            end_tick=clear_end,
            start_clock=tick_to_clock(install_end),
            end_clock=tick_to_clock(clear_end)
        ))

        scheduled_intervals.append(ScheduledInterval(
            entity_type="JOB",
            entity_id="RO-1051",
            operation="RO-1051: Fleet ADAS Calibration (Bay B4)",
            start_tick=ro1051_start,
            end_tick=ro1051_finish,
            start_clock=tick_to_clock(ro1051_start),
            end_clock=tick_to_clock(ro1051_finish)
        ))

    elif movement == "RELOCATE_TO_H2":
        # Vehicle relocates to Holding Location H2, freeing Bay B4
        t_h2_arr = current_t + reloc_out_dur
        b4_first_release = t_h2_arr

        scheduled_intervals.append(ScheduledInterval(
            entity_type="TRANSIT",
            entity_id="RO-1042",
            operation="RO-1042: Transit from Bay B4 to Holding H2",
            start_tick=current_t,
            end_tick=t_h2_arr,
            start_clock=tick_to_clock(current_t),
            end_clock=tick_to_clock(t_h2_arr)
        ))

        # RO-1051 on Bay B4 constrained by technician availability
        if tech_avail is not None:
            ro1051_start = max(b4_first_release, int(tech_avail))
        else:
            ro1051_start = b4_first_release

        ro1051_finish = ro1051_start + ro1051_dur
        scheduled_intervals.append(ScheduledInterval(
            entity_type="JOB",
            entity_id="RO-1051",
            operation="RO-1051: Fleet ADAS Calibration (Bay B4)",
            start_tick=ro1051_start,
            end_tick=ro1051_finish,
            start_clock=tick_to_clock(ro1051_start),
            end_clock=tick_to_clock(ro1051_finish)
        ))

        # Post-service clearance of Bay B4
        b4_free_after_1051 = ro1051_finish + clear_dur
        scheduled_intervals.append(ScheduledInterval(
            entity_type="BAY",
            entity_id="B4",
            operation="Bay B4: Post-Service Clearance Transit (RO-1051)",
            start_tick=ro1051_finish,
            end_tick=b4_free_after_1051,
            start_clock=tick_to_clock(ro1051_finish),
            end_clock=tick_to_clock(b4_free_after_1051)
        ))

        # RO-1042 return transit and reassembly
        ro1042_return_start = max(b4_free_after_1051, source.usable_time_ticks)
        ro1042_return_arr = ro1042_return_start + reloc_out_dur
        install_end = ro1042_return_arr + ro1042_dur
        ro1042_finish = install_end + clear_dur

        scheduled_intervals.append(ScheduledInterval(
            entity_type="HOLDING",
            entity_id="H2",
            operation="RO-1042: Staged in Holding H2 (Awaiting Part & B4)",
            start_tick=t_h2_arr,
            end_tick=ro1042_return_start,
            start_clock=tick_to_clock(t_h2_arr),
            end_clock=tick_to_clock(ro1042_return_start)
        ))

        scheduled_intervals.append(ScheduledInterval(
            entity_type="TRANSIT",
            entity_id="RO-1042",
            operation="RO-1042: Return Transit from H2 to Bay B4",
            start_tick=ro1042_return_start,
            end_tick=ro1042_return_arr,
            start_clock=tick_to_clock(ro1042_return_start),
            end_clock=tick_to_clock(ro1042_return_arr)
        ))

        scheduled_intervals.append(ScheduledInterval(
            entity_type="JOB",
            entity_id="RO-1042",
            operation="RO-1042: Part Installation (Bay B4)",
            start_tick=ro1042_return_arr,
            end_tick=install_end,
            start_clock=tick_to_clock(ro1042_return_arr),
            end_clock=tick_to_clock(install_end)
        ))

        scheduled_intervals.append(ScheduledInterval(
            entity_type="JOB",
            entity_id="RO-1042",
            operation="RO-1042: Final Verification & Bay Clearance",
            start_tick=install_end,
            end_tick=ro1042_finish,
            start_clock=tick_to_clock(install_end),
            end_clock=tick_to_clock(ro1042_finish)
        ))

    else:
        raise ValueError(f"Unsupported movement type: {movement}")

    # Lateness calculations against customer promise targets
    p1 = snapshot.ro1042.promise_ticks
    p2 = snapshot.ro1051.promise_ticks
    w1 = snapshot.ro1042.priority_weight
    w2 = snapshot.ro1051.priority_weight

    late_1042 = max(0, ro1042_finish - p1)
    late_1051 = max(0, ro1051_finish - p2)
    weighted_late = float(w1 * late_1042 + w2 * late_1051)
    delay_min = late_1051 * 5

    return A2PlusCandidatePlan(
        source_id=source.source_id,
        source_name=source.name,
        source_cost=source.cost,
        usable_time_ticks=source.usable_time_ticks,
        freight_delta_from_cheapest=0.0,
        selected_movement=movement,
        b4_release_tick=b4_first_release,
        b4_release_clock=tick_to_clock(b4_first_release),
        ro1042_finish_tick=ro1042_finish,
        ro1042_finish_clock=tick_to_clock(ro1042_finish),
        ro1051_finish_tick=ro1051_finish,
        ro1051_finish_clock=tick_to_clock(ro1051_finish),
        ro1042_lateness_ticks=late_1042,
        ro1051_lateness_ticks=late_1051,
        weighted_lateness=weighted_late,
        downstream_delay_minutes=delay_min,
        qualifies_for_upgrade=False,
        disqualification_reason=None,
        scheduled_intervals=scheduled_intervals
    )


# -----------------------------------------------------------------------------
# 4. Infeasible Decision Factory
# -----------------------------------------------------------------------------

def create_infeasible_a2_plus_decision(
    snapshot: ScenarioSnapshot,
    rejection_reasons: List[RejectedOption],
    max_freight_budget_delta: float = 50.0,
    solve_time_ms: float = 0.0
) -> A2PlusDecision:
    """Creates a truthful, non-fabricated infeasible decision when no eligible source exists."""
    decision_id = f"DEC-A2P-{snapshot.scenario_id}-V{snapshot.snapshot_version}"
    return A2PlusDecision(
        decision_id=decision_id,
        scenario_id=snapshot.scenario_id,
        snapshot_version=snapshot.snapshot_version,
        policy="A2_PLUS",
        status="INFEASIBLE",
        is_feasible=False,
        selected_source_id=None,
        selected_source_name=None,
        selected_movement="HOLD_ON_BAY",
        b4_release_tick=None,
        b4_release_clock=None,
        ro1042_finish_tick=None,
        ro1042_finish_clock=None,
        ro1051_finish_tick=None,
        ro1051_finish_clock=None,
        ro1042_lateness_ticks=None,
        ro1051_lateness_ticks=None,
        weighted_lateness=None,
        downstream_delay_minutes=None,
        freight_cost=None,
        max_freight_budget_delta=max_freight_budget_delta,
        candidate_evaluations=[],
        selection_explanations=[
            "All candidate part sources failed eligibility checks (zero ATP, expired quote, or fitment mismatch).",
            "No feasible recovery schedule could be constructed."
        ],
        scheduled_intervals=[],
        rejected_options=rejection_reasons,
        solve_time_ms=solve_time_ms
    )


# -----------------------------------------------------------------------------
# 5. Core A2+ Policy Solver
# -----------------------------------------------------------------------------

def solve_a2_plus_policy(
    snapshot: ScenarioSnapshot,
    max_freight_budget_delta: float = 50.0
) -> A2PlusDecision:
    """
    Solves service recovery disruption using the A2+ deterministic single-step lookahead heuristic.

    Policy Pipeline:
    Step A: Filter candidate sources by ATP > 0, fitment verification, and quote validity.
    Step B: Evaluate physical safety preconditions to determine vehicle movement mode.
    Step C: Establish baseline candidate using cheapest eligible landed cost source (S_cheap).
    Step D: One-step downstream lookahead evaluating alternatives:
            Qualifies only if Z1(alt) < Z1(cheap) AND cost(alt) - cost(cheap) <= max_freight_budget_delta.
    Step E: Select best qualifying alternative (lowest Z1, tie-break by cost, usable tick, source ID),
            or strictly retain S_cheap if no alternative qualifies.
    """
    t_start = time.perf_counter()
    decision_id = f"DEC-A2P-{snapshot.scenario_id}-V{snapshot.snapshot_version}"

    # Step A: Source eligibility
    rejected_options: List[RejectedOption] = []
    eligible_sources: List[PartSource] = []
    for s in snapshot.sources:
        is_elig, rejections = validate_source_eligibility(s)
        if is_elig:
            eligible_sources.append(s)
        else:
            rejected_options.extend(rejections)

    if not eligible_sources:
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        return create_infeasible_a2_plus_decision(
            snapshot=snapshot,
            rejection_reasons=rejected_options,
            max_freight_budget_delta=max_freight_budget_delta,
            solve_time_ms=elapsed_ms
        )

    # Step B: Physical relocation gating
    can_relocate, reloc_rejections = check_a2_plus_relocation_gating(snapshot)
    if not can_relocate:
        rejected_options.extend(reloc_rejections)
        selected_movement = "HOLD_ON_BAY"
    else:
        selected_movement = "RELOCATE_TO_H2"

    # Step C: Cheapest source anchor
    # Deterministic sorting: 1. Lowest cost, 2. Earliest usable tick, 3. Source ID
    sorted_sources = sorted(
        eligible_sources,
        key=lambda s: (s.cost, s.usable_time_ticks, s.source_id)
    )
    s_cheap = sorted_sources[0]
    base_plan = evaluate_deterministic_schedule(snapshot, s_cheap, selected_movement)
    base_plan.freight_delta_from_cheapest = 0.0
    base_plan.qualifies_for_upgrade = True  # Anchor baseline is always qualified
    base_z1 = base_plan.weighted_lateness

    candidate_evaluations: List[A2PlusCandidatePlan] = [base_plan]
    qualifying_alternatives: List[A2PlusCandidatePlan] = []

    # Step D: One-step downstream lookahead across alternative sources
    for s_alt in sorted_sources[1:]:
        freight_delta = round(s_alt.cost - s_cheap.cost, 4)
        alt_plan = evaluate_deterministic_schedule(snapshot, s_alt, selected_movement)
        alt_plan.freight_delta_from_cheapest = freight_delta

        # Two necessary conditions for upgrade:
        # 1. Strictly lower weighted lateness than cheapest anchor
        # 2. Freight surcharge within max_freight_budget_delta
        improves_lateness = (alt_plan.weighted_lateness < base_z1)
        within_budget = (freight_delta <= max_freight_budget_delta)

        if improves_lateness and within_budget:
            alt_plan.qualifies_for_upgrade = True
            qualifying_alternatives.append(alt_plan)
        else:
            alt_plan.qualifies_for_upgrade = False
            reasons = []
            if not improves_lateness:
                reasons.append(
                    f"Weighted lateness {alt_plan.weighted_lateness:.1f} ticks does not strictly improve "
                    f"upon cheapest anchor ({base_z1:.1f} ticks)"
                )
            if not within_budget:
                reasons.append(
                    f"Freight delta ${freight_delta:.2f} exceeds permitted budget ${max_freight_budget_delta:.2f}"
                )
            alt_plan.disqualification_reason = "; ".join(reasons)

        candidate_evaluations.append(alt_plan)

    # Step E: Candidate selection
    explanations: List[str] = [
        f"A2+ Heuristic Evaluation for Scenario {snapshot.scenario_id} (Snapshot v{snapshot.snapshot_version}).",
        f"Physical relocation gating determined movement: {selected_movement}.",
        f"Cheapest source anchor: {s_cheap.source_id} ({s_cheap.name}) at ${s_cheap.cost:.2f} "
        f"with baseline weighted lateness Z1 = {base_z1:.1f} ticks."
    ]

    if qualifying_alternatives:
        # Deterministic ranking among qualifying alternatives:
        # 1. Lowest weighted lateness
        # 2. Lowest landed cost
        # 3. Earliest usable-ready time
        # 4. Source ID
        qualifying_alternatives.sort(
            key=lambda p: (
                p.weighted_lateness,
                p.source_cost,
                p.usable_time_ticks,
                p.source_id
            )
        )
        selected_plan = qualifying_alternatives[0]
        lateness_reduction = base_z1 - selected_plan.weighted_lateness
        explanations.append(
            f"LOOKAHEAD UPGRADE: Sourcing upgraded from {s_cheap.source_id} (${s_cheap.cost:.2f}) "
            f"to {selected_plan.source_id} (${selected_plan.source_cost:.2f}). "
            f"Incurred freight delta of +${selected_plan.freight_delta_from_cheapest:.2f} (budget: ${max_freight_budget_delta:.2f}) "
            f"to achieve strict weighted lateness reduction of {lateness_reduction:.1f} ticks "
            f"({selected_plan.weighted_lateness:.1f} vs {base_z1:.1f})."
        )
    else:
        selected_plan = base_plan
        explanations.append(
            f"CHEAPEST RETAINED: No qualifying alternative source offered strictly lower weighted lateness "
            f"within the ${max_freight_budget_delta:.2f} freight surcharge budget. "
            f"Retained cheapest source {s_cheap.source_id} (${s_cheap.cost:.2f}) with Z1 = {base_z1:.1f} ticks."
        )

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    return A2PlusDecision(
        decision_id=decision_id,
        scenario_id=snapshot.scenario_id,
        snapshot_version=snapshot.snapshot_version,
        policy="A2_PLUS",
        status="HEURISTIC",
        is_feasible=True,
        selected_source_id=selected_plan.source_id,
        selected_source_name=selected_plan.source_name,
        selected_movement=selected_plan.selected_movement,
        b4_release_tick=selected_plan.b4_release_tick,
        b4_release_clock=selected_plan.b4_release_clock,
        ro1042_finish_tick=selected_plan.ro1042_finish_tick,
        ro1042_finish_clock=selected_plan.ro1042_finish_clock,
        ro1051_finish_tick=selected_plan.ro1051_finish_tick,
        ro1051_finish_clock=selected_plan.ro1051_finish_clock,
        ro1042_lateness_ticks=selected_plan.ro1042_lateness_ticks,
        ro1051_lateness_ticks=selected_plan.ro1051_lateness_ticks,
        weighted_lateness=selected_plan.weighted_lateness,
        downstream_delay_minutes=selected_plan.downstream_delay_minutes,
        freight_cost=selected_plan.source_cost,
        max_freight_budget_delta=max_freight_budget_delta,
        candidate_evaluations=candidate_evaluations,
        selection_explanations=explanations,
        scheduled_intervals=selected_plan.scheduled_intervals,
        rejected_options=rejected_options,
        solve_time_ms=elapsed_ms
    )


# -----------------------------------------------------------------------------
# 6. Verifier Compatibility View & Adapter
# -----------------------------------------------------------------------------

class A2PlusVerifierView(BaseModel):
    """
    Dedicated verifier-input projection/view for A2+ decisions.
    Preserves policy_id='A2_PLUS' in the decision digest and invariant checks without
    modifying the legacy PolicyId enum or the production Proposal model.
    Provides all decision-relevant fields required by compute_proposal_digest() and verify_proposal().
    """
    proposal_id: str
    run_id: str
    scenario_id: str
    policy_id: str = "A2_PLUS"
    input_snapshot_version: int
    selected_source_id: Optional[str] = None
    selected_source_name: Optional[str] = None
    selected_movement: Optional[str] = "HOLD_ON_BAY"
    b4_release_tick: int
    b4_release_clock: str
    ro1051_finish_tick: int
    ro1051_finish_clock: str
    ro1042_finish_tick: int
    ro1042_finish_clock: str
    weighted_lateness_ticks: float
    ro1042_lateness_ticks: int
    ro1051_lateness_ticks: int
    downstream_delay_minutes: int
    parts_freight_cost: float
    solver_status: SolverStatusEnum = SolverStatusEnum.FEASIBLE
    pass1_status: Optional[SolverStatusEnum] = None
    pass2_status: Optional[SolverStatusEnum] = None
    best_bound: Optional[float] = None
    solve_time_ms: float = 0.0
    feasibility_explanations: List[str] = Field(default_factory=list)
    rejected_options: List[RejectedOption] = Field(default_factory=list)
    scheduled_intervals: List[ScheduledInterval] = Field(default_factory=list)
    approval_status: ApprovalStatus = ApprovalStatus.PENDING_APPROVAL
    verification_result: Optional[Dict[str, Any]] = None


def a2_plus_to_verifier_view(decision: A2PlusDecision) -> A2PlusVerifierView:
    """
    Creates a dedicated verifier-input projection (A2PlusVerifierView) from a feasible A2PlusDecision.
    Preserves policy_id='A2_PLUS' in the decision digest and invariant checks without
    modifying the legacy PolicyId enum or the production Proposal model.

    Raises:
        ValueError: If the decision is infeasible (is_feasible is False or status is INFEASIBLE),
                    preventing fabrication of artificial milestone/lateness values.
    """
    if not decision.is_feasible or decision.status == "INFEASIBLE":
        raise ValueError(
            f"Cannot project infeasible A2PlusDecision '{decision.decision_id}' into a verifier view. "
            "Infeasible decisions have unpopulated milestones (None) and must not be fabricated."
        )

    if (
        decision.b4_release_tick is None
        or decision.ro1051_finish_tick is None
        or decision.ro1042_finish_tick is None
        or decision.weighted_lateness is None
        or decision.freight_cost is None
    ):
        raise ValueError(
            f"Cannot project A2PlusDecision '{decision.decision_id}' with missing critical milestone values."
        )

    return A2PlusVerifierView(
        proposal_id=f"PROP-{decision.decision_id}",
        run_id=f"RUN-{decision.decision_id}",
        scenario_id=decision.scenario_id,
        policy_id="A2_PLUS",
        input_snapshot_version=decision.snapshot_version,
        selected_source_id=decision.selected_source_id,
        selected_source_name=decision.selected_source_name,
        selected_movement=decision.selected_movement,
        b4_release_tick=decision.b4_release_tick,
        b4_release_clock=decision.b4_release_clock or "08:00",
        ro1051_finish_tick=decision.ro1051_finish_tick,
        ro1051_finish_clock=decision.ro1051_finish_clock or "08:00",
        ro1042_finish_tick=decision.ro1042_finish_tick,
        ro1042_finish_clock=decision.ro1042_finish_clock or "08:00",
        weighted_lateness_ticks=decision.weighted_lateness,
        ro1042_lateness_ticks=decision.ro1042_lateness_ticks or 0,
        ro1051_lateness_ticks=decision.ro1051_lateness_ticks or 0,
        downstream_delay_minutes=decision.downstream_delay_minutes or 0,
        parts_freight_cost=decision.freight_cost,
        solver_status=SolverStatusEnum.FEASIBLE,
        solve_time_ms=decision.solve_time_ms,
        feasibility_explanations=decision.selection_explanations,
        rejected_options=decision.rejected_options,
        scheduled_intervals=decision.scheduled_intervals,
        approval_status=ApprovalStatus.PENDING_APPROVAL
    )


# Backwards-compatibility alias for research/verifier test imports
a2_plus_to_proposal_adapter = a2_plus_to_verifier_view

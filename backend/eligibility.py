"""
Eligibility and Feasibility Validation Gates.
Validates parts inventory availability, fitment, quotes, and physical vehicle safety preconditions.
"""

from typing import List, Tuple
from backend.models import (
    ScenarioSnapshot,
    PartSource,
    RejectedOption,
    VehicleState
)


def validate_source_eligibility(source: PartSource) -> Tuple[bool, List[RejectedOption]]:
    """
    Validates a candidate part source against ATP, fitment, and quote validity.
    Returns (is_eligible, list_of_rejections).
    """
    rejections = []
    
    if source.atp < 1:
        rejections.append(RejectedOption(
            candidate_id=source.source_id,
            reason_code="INSUFFICIENT_ATP",
            description=f"Source {source.source_id} ({source.name}) has ATP = {source.atp}. Zero units reservable."
        ))

    if not source.fitment_verified:
        rejections.append(RejectedOption(
            candidate_id=source.source_id,
            reason_code="FITMENT_MISMATCH",
            description=f"Source {source.source_id} part number does not match OEM VIN specification for vehicle."
        ))

    if not source.quote_valid:
        rejections.append(RejectedOption(
            candidate_id=source.source_id,
            reason_code="EXPIRED_QUOTE",
            description=f"Source {source.source_id} freight/holding quotation window has expired."
        ))

    return (len(rejections) == 0, rejections)


def validate_relocation_feasibility(snapshot: ScenarioSnapshot) -> Tuple[bool, List[RejectedOption]]:
    """
    Validates whether RO-1042 can be physically relocated off Bay B4 into Holding Location H2.
    Requires:
    1. Vehicle physical state must be SAFE_TO_RELOCATE.
    2. Certified technician signoff must be recorded.
    3. Holding location H2 must have at least 1 available stall (capacity > 0).
    """
    rejections = []
    ro = snapshot.ro1042

    # Check vehicle physical state
    if ro.current_vehicle_state != VehicleState.SAFE_TO_RELOCATE:
        rejections.append(RejectedOption(
            candidate_id="RELOCATE_TO_H2",
            reason_code="VEHICLE_NOT_SAFE_TO_MOVE",
            description=(
                f"Vehicle is in state '{ro.current_vehicle_state.value}'. "
                "Movement is strictly blocked until mechanical reassembly is complete "
                "and certified technician sign-off is logged (Invariant CE-1)."
            )
        ))
    elif not ro.technician_signoff_recorded:
        rejections.append(RejectedOption(
            candidate_id="RELOCATE_TO_H2",
            reason_code="MISSING_TECHNICIAN_SIGNOFF",
            description="Vehicle mechanical check recorded but digital technician sign-off is missing."
        ))

    # Check holding capacity
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

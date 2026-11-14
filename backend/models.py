"""
Pydantic data models and schemas for StallBreaker CP-SAT MVP.
Conforms strictly to Tekion Theme 1, UC04 specifications and canonical fixture S-MATH-01.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PolicyId(str, Enum):
    P0 = "P0"  # Wait / No Recovery
    P1 = "P1"  # Manager Heuristic Baseline
    A2 = "A2"  # Fixed-Source Sequential Baseline
    P3 = "P3"  # StallBreaker Joint Policy


class VehicleState(str, Enum):
    PARTIALLY_DISMANTLED = "PARTIALLY_DISMANTLED"
    REPAIR_MECHANICALLY_COMPLETE = "REPAIR_MECHANICALLY_COMPLETE"
    FINAL_VERIFICATION_IN_PROGRESS = "FINAL_VERIFICATION_IN_PROGRESS"
    SAFE_TO_MOVE = "SAFE_TO_MOVE"
    IN_CLEARANCE_TRANSIT = "IN_CLEARANCE_TRANSIT"
    IN_CUSTOMER_PICKUP_STAGING = "IN_CUSTOMER_PICKUP_STAGING"
    # Relocation states
    SAFE_TO_RELOCATE = "SAFE_TO_RELOCATE"
    IN_RELOCATION_TRANSIT = "IN_RELOCATION_TRANSIT"
    IN_HOLDING = "IN_HOLDING"


class BayState(str, Enum):
    OCCUPIED = "OCCUPIED"
    CLEARANCE_PENDING = "CLEARANCE_PENDING"
    AVAILABLE_FOR_ALLOCATION = "AVAILABLE_FOR_ALLOCATION"


class SolverStatusEnum(str, Enum):
    OPTIMAL = "OPTIMAL"
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    UNKNOWN = "UNKNOWN"
    MODEL_INVALID = "MODEL_INVALID"


class ApprovalStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    STALE_SNAPSHOT = "STALE_SNAPSHOT"


class PartSource(BaseModel):
    source_id: str = Field(..., description="Unique ID, e.g. S1, S2")
    name: str = Field(..., description="Supplier name e.g. Hotshot Courier, Sister Store")
    usable_time_ticks: int = Field(..., description="Tick at which part is on site and usable (1 tick = 5 min)")
    cost: float = Field(..., description="Landed procurement/freight cost ($)")
    atp: int = Field(default=1, description="Available-To-Promise stock quantity (0 or 1)")
    fitment_verified: bool = Field(default=True, description="VIN and OEM parts catalogue fitment match")
    quote_valid: bool = Field(default=True, description="Whether courier quote/holding window is active")
    source_version: int = Field(default=1, description="Inventory version tag for concurrency checks")


class RepairOrder(BaseModel):
    ro_id: str = Field(..., description="RO identifier, e.g. RO-1042, RO-1051")
    customer_name: str
    vehicle_model: str
    is_commercial_fleet: bool = False
    promise_ticks: int = Field(..., description="Promise time in ticks from origin 08:00 (1 tick = 5 min)")
    priority_weight: float = Field(default=1.0, description="Priority multiplier (e.g. 1.0 retail, 3.0 fleet)")
    service_duration_ticks: int = Field(..., description="Required duration for service operation in ticks")
    required_bay: str = "B4"
    requires_alignment_hoist: bool = True
    current_vehicle_state: VehicleState = VehicleState.PARTIALLY_DISMANTLED
    technician_signoff_recorded: bool = False


class ScheduledInterval(BaseModel):
    entity_type: str = Field(..., description="JOB, BAY, TECH, TRANSIT, HOLDING")
    entity_id: str = Field(..., description="e.g. RO-1042, B4, K1, H2")
    operation: str = Field(..., description="e.g. Part Installation, ADAS Calibration, Clearance Transit")
    start_tick: int
    end_tick: int
    start_clock: str
    end_clock: str


class RejectedOption(BaseModel):
    candidate_id: str
    reason_code: str
    description: str


class Proposal(BaseModel):
    proposal_id: str
    run_id: str
    scenario_id: str
    policy_id: PolicyId
    input_snapshot_version: int
    selected_source_id: Optional[str] = None
    selected_source_name: Optional[str] = None
    selected_movement: str = "HOLD_ON_BAY"  # "HOLD_ON_BAY" or "RELOCATE_TO_H2"
    
    # Critical timestamps & milestones
    b4_release_tick: int
    b4_release_clock: str
    ro1051_finish_tick: int
    ro1051_finish_clock: str
    ro1042_finish_tick: int
    ro1042_finish_clock: str
    
    # Objective metrics
    weighted_lateness_ticks: float
    ro1042_lateness_ticks: int
    ro1051_lateness_ticks: int
    downstream_delay_minutes: int
    parts_freight_cost: float
    
    # Solver execution metrics
    solver_status: SolverStatusEnum
    best_bound: Optional[float] = None
    solve_time_ms: float
    
    # Explanations & auditing
    feasibility_explanations: List[str] = []
    rejected_options: List[RejectedOption] = []
    scheduled_intervals: List[ScheduledInterval] = []
    approval_status: ApprovalStatus = ApprovalStatus.PENDING_APPROVAL


class PolicyComparisonResult(BaseModel):
    scenario_id: str
    snapshot_version: int
    baseline_a2: Proposal
    joint_p3: Proposal
    
    # Comparison summary metrics
    weighted_lateness_reduction_pct: float
    downstream_lateness_savings_minutes: int
    freight_cost_delta: float
    summary_verdict: str


class ScenarioSnapshot(BaseModel):
    scenario_id: str
    scenario_name: str
    description: str
    snapshot_version: int
    current_tick: int = 21  # 09:45 AM
    current_clock: str = "09:45"
    
    # Assets & state
    ro1042: RepairOrder
    ro1051: RepairOrder
    sources: List[PartSource]
    bay_b4_state: BayState
    h2_capacity: int = 1
    h2_available_stalls: int = 0
    relocation_duration_ticks: int = 3  # 15 minutes each way
    clearance_duration_ticks: int = 2   # 10 minutes (1 verify + 1 transit)
    technician_k1_available: bool = True


class AuditEvent(BaseModel):
    event_id: str
    timestamp: str
    event_type: str
    description: str
    version_before: int
    version_after: int
    details: Dict[str, Any] = {}

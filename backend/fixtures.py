"""
Scenario fixtures for StallBreaker CP-SAT MVP.
Preserves canonical S-MATH-01 parameters and defines S-MATH-01-ROLLABLE variant.
"""

from backend.models import (
    ScenarioSnapshot,
    RepairOrder,
    PartSource,
    BayState,
    VehicleState
)


def tick_to_clock(tick: int) -> str:
    """Converts tick (from 08:00 origin, 5 min per tick) to HH:MM format."""
    total_minutes = 8 * 60 + tick * 5
    hours = total_minutes // 60
    mins = total_minutes % 60
    return f"{hours:02d}:{mins:02d}"


def get_canonical_s_math_01_fixture(version: int = 1) -> ScenarioSnapshot:
    """
    Canonical S-MATH-01 fixture:
    - Initial disruption at t=21 (09:45 AM).
    - RO-1042 (Ford Explorer, Sarah Jenkins): brake overhaul, promise t=66 (13:30), weight 1.0.
      Vehicle is PARTIALLY_DISMANTLED on Bay B4; NO technician signoff recorded.
    - RO-1051 (Ford F-150, Commercial Fleet): ADAS alignment calibration, promise t=54 (12:30), weight 3.0.
      Requires Bay B4 specialized alignment hoist. Service duration 24 ticks (120 min).
    - Bay B4: OCCUPIED by RO-1042.
    - Holding location H2: Capacity 1, available stalls = 0 (SATURATED).
    - Source S1 (Hotshot Courier): usable at t=27 (10:15 AM), landed freight $55.00, atp=1.
    - Source S2 (Sister Store Transfer): usable at t=49 (12:05 PM), landed freight $18.00, atp=1.
    - Installation duration: 12 ticks (60 min).
    - Clearance duration: 2 ticks (10 min = 1 tick verify + 1 tick transit).
    """
    ro1042 = RepairOrder(
        ro_id="RO-1042",
        customer_name="Sarah Jenkins",
        vehicle_model="Ford Explorer",
        is_commercial_fleet=False,
        promise_ticks=66,
        priority_weight=1.0,
        service_duration_ticks=12,
        required_bay="B4",
        requires_alignment_hoist=True,
        current_vehicle_state=VehicleState.PARTIALLY_DISMANTLED,
        technician_signoff_recorded=False
    )

    ro1051 = RepairOrder(
        ro_id="RO-1051",
        customer_name="Commercial Fleet Account",
        vehicle_model="Ford F-150 Commercial",
        is_commercial_fleet=True,
        promise_ticks=54,
        priority_weight=3.0,
        service_duration_ticks=24,
        required_bay="B4",
        requires_alignment_hoist=True,
        current_vehicle_state=VehicleState.SAFE_TO_MOVE,
        technician_signoff_recorded=True
    )

    sources = [
        PartSource(
            source_id="S1",
            name="Hotshot Courier Express",
            usable_time_ticks=27,
            cost=55.00,
            atp=1,
            fitment_verified=True,
            quote_valid=True,
            source_version=version
        ),
        PartSource(
            source_id="S2",
            name="Sister Store Shuttle Transfer",
            usable_time_ticks=49,
            cost=18.00,
            atp=1,
            fitment_verified=True,
            quote_valid=True,
            source_version=version
        )
    ]

    return ScenarioSnapshot(
        scenario_id="S-MATH-01",
        scenario_name="Canonical S-MATH-01: Hoist Lock Disruption",
        description="Ford Explorer immobilized on Bay B4 alignment hoist; H2 holding lot saturated. Sourcing must be solved under hoist lock.",
        snapshot_version=version,
        current_tick=21,
        current_clock=tick_to_clock(21),
        ro1042=ro1042,
        ro1051=ro1051,
        sources=sources,
        bay_b4_state=BayState.OCCUPIED,
        h2_capacity=1,
        h2_available_stalls=0,
        relocation_duration_ticks=3,
        clearance_duration_ticks=2,
        technician_k1_available=True
    )


def get_rollable_s_math_01_fixture(version: int = 1) -> ScenarioSnapshot:
    """
    Alternate S-MATH-01-ROLLABLE fixture:
    - RO-1042 is in verified SAFE_TO_RELOCATE state with technician signoff recorded.
    - Holding location H2 has 1 available stall (RESERVABLE).
    - Relocation requires 3 ticks (15 min) each way.
    - Permits the solver to evaluate relocation to H2 vs holding on Bay B4.
    """
    ro1042 = RepairOrder(
        ro_id="RO-1042",
        customer_name="Sarah Jenkins",
        vehicle_model="Ford Explorer",
        is_commercial_fleet=False,
        promise_ticks=66,
        priority_weight=1.0,
        service_duration_ticks=12,
        required_bay="B4",
        requires_alignment_hoist=True,
        current_vehicle_state=VehicleState.SAFE_TO_RELOCATE,
        technician_signoff_recorded=True
    )

    ro1051 = RepairOrder(
        ro_id="RO-1051",
        customer_name="Commercial Fleet Account",
        vehicle_model="Ford F-150 Commercial",
        is_commercial_fleet=True,
        promise_ticks=54,
        priority_weight=3.0,
        service_duration_ticks=24,
        required_bay="B4",
        requires_alignment_hoist=True,
        current_vehicle_state=VehicleState.SAFE_TO_MOVE,
        technician_signoff_recorded=True
    )

    sources = [
        PartSource(
            source_id="S1",
            name="Hotshot Courier Express",
            usable_time_ticks=27,
            cost=55.00,
            atp=1,
            fitment_verified=True,
            quote_valid=True,
            source_version=version
        ),
        PartSource(
            source_id="S2",
            name="Sister Store Shuttle Transfer",
            usable_time_ticks=49,
            cost=18.00,
            atp=1,
            fitment_verified=True,
            quote_valid=True,
            source_version=version
        )
    ]

    return ScenarioSnapshot(
        scenario_id="S-MATH-01-ROLLABLE",
        scenario_name="Alternate S-MATH-01-ROLLABLE: Relocatable Vehicle",
        description="Ford Explorer certified safe to relocate with 1 open stall in H2 holding. Solver can choose to relocate or hold on hoist.",
        snapshot_version=version,
        current_tick=21,
        current_clock=tick_to_clock(21),
        ro1042=ro1042,
        ro1051=ro1051,
        sources=sources,
        bay_b4_state=BayState.OCCUPIED,
        h2_capacity=1,
        h2_available_stalls=1,
        relocation_duration_ticks=3,
        clearance_duration_ticks=2,
        technician_k1_available=True
    )

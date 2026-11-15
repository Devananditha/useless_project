"""
Test Suite: Multi-Scenario Registry & State Store Isolation (Stage 1)
Verifies deterministic loading, typed snapshot generation, instance isolation,
and error handling across S-MATH-01, S-MATH-02, and S-MATH-03.
"""

import pytest
from backend.models import (
    ScenarioSnapshot,
    VehicleState,
    BayState
)
from backend.fixtures import (
    get_canonical_s_math_01_fixture,
    get_rollable_s_math_01_fixture,
    get_s_math_02_fixture,
    get_s_math_03_fixture,
    SCENARIO_REGISTRY
)
from backend.state_store import StateStore


def test_registry_contains_all_scenarios():
    """Ensure SCENARIO_REGISTRY contains S-MATH-01, S-MATH-01-ROLLABLE, S-MATH-02, and S-MATH-03."""
    expected_ids = {"S-MATH-01", "S-MATH-01-ROLLABLE", "S-MATH-02", "S-MATH-03"}
    assert expected_ids.issubset(set(SCENARIO_REGISTRY.keys()))


def test_fixture_constructors_return_typed_snapshots():
    """Verify each fixture constructor produces a valid ScenarioSnapshot."""
    for sc_id, builder in SCENARIO_REGISTRY.items():
        snap = builder(version=14)
        assert isinstance(snap, ScenarioSnapshot)
        assert snap.scenario_id == sc_id
        assert snap.snapshot_version == 14
        assert snap.ro1042 is not None
        assert snap.ro1051 is not None
        assert len(snap.sources) >= 2


def test_s_math_02_structured_technician_constraints():
    """Verify S-MATH-02 represents Master Tech K2 commitment as structured data."""
    snap = get_s_math_02_fixture(version=14)
    assert snap.scenario_id == "S-MATH-02"
    assert snap.technician_k2_available_tick == 60
    assert snap.ro1051.assigned_technician_id == "K2"
    assert snap.ro1051.technician_available_tick == 60
    assert snap.technician_assignments is not None
    assert "RO-1030" in snap.technician_assignments
    assert snap.technician_assignments["RO-1030"]["busy_until_tick"] == 60
    assert snap.ro1042.promise_ticks == 84
    assert snap.ro1051.promise_ticks == 90


def test_s_math_03_structured_physical_safety_state():
    """Verify S-MATH-03 represents physical vehicle safety as structured fields."""
    snap = get_s_math_03_fixture(version=14)
    assert snap.scenario_id == "S-MATH-03"
    assert snap.ro1042.current_vehicle_state == VehicleState.PARTIALLY_DISMANTLED
    assert snap.ro1042.is_rollable is False
    assert snap.ro1042.technician_signoff_recorded is False
    assert snap.h2_available_stalls == 2  # Spatial buffer exists
    assert snap.ro1042.promise_ticks == 66
    assert snap.ro1051.promise_ticks == 50
    assert snap.ro1051.priority_weight == 3.0


def test_fixtures_are_deterministic():
    """Verify loading fixtures repeatedly produces identical snapshot structures."""
    for sc_id, builder in SCENARIO_REGISTRY.items():
        snap1 = builder(version=14)
        snap2 = builder(version=14)
        assert snap1.model_dump() == snap2.model_dump()


def test_state_store_independent_instances_and_isolation():
    """Verify state store returns independent copies and mutating one does not mutate others."""
    store = StateStore()
    
    # Retrieve S-MATH-02 and mutate it
    snap_02 = store.get_scenario("S-MATH-02")
    snap_02.ro1042.customer_name = "MUTATED_CUSTOMER_NAME"
    snap_02.sources[0].cost = 9999.0
    
    # Check that store's internal S-MATH-02 was NOT mutated
    fresh_02 = store.get_scenario("S-MATH-02")
    assert fresh_02.ro1042.customer_name == "Sarah Jenkins"
    assert fresh_02.sources[0].cost == 55.00
    
    # Check that S-MATH-01 was NOT mutated
    snap_01 = store.get_scenario("S-MATH-01")
    assert snap_01.ro1042.customer_name == "Sarah Jenkins"
    assert snap_01.sources[0].cost == 55.00


def test_cross_scenario_mutation_isolation():
    """Mutating S-MATH-03 cannot alter S-MATH-02 or S-MATH-01 in the store."""
    store = StateStore()
    
    snap_03 = store.get_scenario("S-MATH-03")
    snap_03.h2_available_stalls = 99
    snap_03.ro1042.is_rollable = True
    
    # Verify S-MATH-03 in store remains intact
    assert store.get_scenario("S-MATH-03").h2_available_stalls == 2
    assert store.get_scenario("S-MATH-03").ro1042.is_rollable is False
    
    # Verify S-MATH-02 remains intact
    assert store.get_scenario("S-MATH-02").h2_available_stalls == 0


def test_unknown_scenario_id_raises_value_error():
    """Requesting an unknown scenario ID must raise a clear ValueError."""
    store = StateStore()
    with pytest.raises(ValueError, match="Unknown scenario ID: UNKNOWN-99"):
        store.get_scenario("UNKNOWN-99")
        
    with pytest.raises(ValueError, match="Unknown scenario ID: INVALID_ROOFTOP"):
        store.select_scenario("INVALID_ROOFTOP")


def test_repeated_get_does_not_mutate_version():
    """GET requests must remain strictly read-only and not mutate snapshot version."""
    store = StateStore()
    initial_version = store.version
    
    for _ in range(5):
        _ = store.get_scenario("S-MATH-01")
        _ = store.get_scenario("S-MATH-02")
        _ = store.get_scenario("S-MATH-03")
        _ = store.get_active_snapshot()
        
    assert store.version == initial_version
    assert store.active_snapshot.snapshot_version == initial_version


def test_reset_to_canonical_reloads_all_scenarios():
    """Store reset restores all scenarios to initial version v14."""
    store = StateStore()
    store.select_scenario("S-MATH-03")
    store.trigger_competing_reservation("S1")
    assert store.version == 15
    
    store.reset_to_canonical()
    assert store.version == 14
    assert store.current_scenario_id == "S-MATH-01"
    assert store.get_scenario("S-MATH-01").sources[0].atp == 1
    assert store.get_scenario("S-MATH-03").sources[0].atp == 1

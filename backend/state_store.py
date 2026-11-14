"""
In-Memory Versioned State Store for StallBreaker MVP.
Provides optimistic concurrency tracking, audit event logging, and state management.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from backend.models import (
    ScenarioSnapshot,
    Proposal,
    AuditEvent,
    ApprovalStatus
)
from backend.fixtures import (
    get_canonical_s_math_01_fixture,
    get_rollable_s_math_01_fixture
)


class StateStore:
    def __init__(self):
        self.version = 14  # Initial version e.g. v14 as specified in Act 3 narrative
        self.current_scenario_id = "S-MATH-01"
        self.snapshots: Dict[str, ScenarioSnapshot] = {
            "S-MATH-01": get_canonical_s_math_01_fixture(version=self.version),
            "S-MATH-01-ROLLABLE": get_rollable_s_math_01_fixture(version=self.version)
        }
        self.active_snapshot: ScenarioSnapshot = self.snapshots["S-MATH-01"]
        self.proposals: Dict[str, Proposal] = {}
        self.events: List[AuditEvent] = []
        
        self.log_event(
            event_type="SYSTEM_INITIALIZED",
            description=f"StallBreaker state store initialized at snapshot version v{self.version}. Scenario S-MATH-01 active.",
            version_before=self.version,
            version_after=self.version,
            details={"active_scenario": self.current_scenario_id}
        )

    def log_event(
        self,
        event_type: str,
        description: str,
        version_before: int,
        version_after: int,
        details: Optional[Dict] = None
    ) -> AuditEvent:
        evt = AuditEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:6].upper()}",
            timestamp=datetime.now().strftime("%H:%M:%S"),
            event_type=event_type,
            description=description,
            version_before=version_before,
            version_after=version_after,
            details=details or {}
        )
        self.events.append(evt)
        return evt

    def get_active_snapshot(self) -> ScenarioSnapshot:
        return self.active_snapshot

    def get_scenario(self, scenario_id: str) -> ScenarioSnapshot:
        """
        Strictly read-only retrieval of scenario snapshot.
        Must NOT change version, reset data, or emit side effects.
        """
        if scenario_id not in self.snapshots:
            raise ValueError(f"Unknown scenario ID: {scenario_id}")
        return self.snapshots[scenario_id]

    def select_scenario(self, scenario_id: str) -> ScenarioSnapshot:
        """
        Explicitly selects/switches the active scenario.
        """
        if scenario_id not in self.snapshots:
            raise ValueError(f"Unknown scenario ID: {scenario_id}")
        
        v_before = self.version
        self.current_scenario_id = scenario_id
        self.active_snapshot = self.snapshots[scenario_id]

        self.log_event(
            event_type="SCENARIO_SELECTED",
            description=f"Switched active scenario to {scenario_id} at snapshot version v{self.active_snapshot.snapshot_version}.",
            version_before=v_before,
            version_after=self.version,
            details={"scenario_id": scenario_id}
        )
        return self.active_snapshot

    def save_proposal(self, proposal: Proposal):
        self.proposals[proposal.proposal_id] = proposal
        self.log_event(
            event_type="PROPOSAL_GENERATED",
            description=(
                f"Generated {proposal.policy_id.value} recovery proposal ({proposal.proposal_id}) "
                f"under snapshot v{proposal.input_snapshot_version}. Selected: {proposal.selected_source_id} "
                f"(${proposal.parts_freight_cost:.2f}), Movement: {proposal.selected_movement}."
            ),
            version_before=self.version,
            version_after=self.version,
            details={
                "proposal_id": proposal.proposal_id,
                "policy": proposal.policy_id.value,
                "weighted_lateness": proposal.weighted_lateness_ticks
            }
        )

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        return self.proposals.get(proposal_id)

    def trigger_competing_reservation(self, source_id: str = "S1") -> ScenarioSnapshot:
        """
        Simulates Demo Act 3: A competing wholesale buyer reserves the last available unit of S1.
        Reduces S1 ATP to 0 and increments snapshot version (e.g. v14 -> v15).
        """
        v_before = self.version
        self.version += 1
        
        # Update source in active snapshot
        updated_sources = []
        target_name = source_id
        for s in self.active_snapshot.sources:
            if s.source_id == source_id:
                target_name = s.name
                updated_sources.append(s.model_copy(update={"atp": 0, "source_version": self.version}))
            else:
                updated_sources.append(s.model_copy(update={"source_version": self.version}))

        self.active_snapshot = self.active_snapshot.model_copy(
            update={"sources": updated_sources, "snapshot_version": self.version}
        )
        self.snapshots[self.current_scenario_id] = self.active_snapshot

        self.log_event(
            event_type="COMPETING_RESERVATION_LOGGED",
            description=(
                f"External vendor alert: Competing reservation claimed stock for {source_id} ({target_name}). "
                f"ATP decreased 1 -> 0. Inventory snapshot advanced from v{v_before} to v{self.version}."
            ),
            version_before=v_before,
            version_after=self.version,
            details={"source_id": source_id, "new_atp": 0}
        )
        return self.active_snapshot

    def reset_to_canonical(self) -> ScenarioSnapshot:
        """Resets store back to original canonical state."""
        v_before = self.version
        self.version = 14
        self.current_scenario_id = "S-MATH-01"
        self.snapshots = {
            "S-MATH-01": get_canonical_s_math_01_fixture(version=self.version),
            "S-MATH-01-ROLLABLE": get_rollable_s_math_01_fixture(version=self.version)
        }
        self.active_snapshot = self.snapshots["S-MATH-01"]
        self.proposals.clear()
        self.events.clear()
        self.log_event(
            event_type="STORE_RESET",
            description=f"Store reset to initial canonical fixture S-MATH-01 at version v{self.version}.",
            version_before=v_before,
            version_after=self.version
        )
        return self.active_snapshot


# Global singleton store instance for the backend session
store = StateStore()

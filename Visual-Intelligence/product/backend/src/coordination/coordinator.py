"""
Phase 12 Multi-Mission Coordinator.

The primary control-plane orchestrator for multi-mission coordination, logical resource
governance, deterministic arbitration, machine conflict detection, deadlock resolution,
safe preemption, global capacity tracking, and append-only coordination ledgers.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set
import uuid

from src.mission_control.coordinator import MissionCoordinator
from src.mission_control.mission_ledger import MissionLedger
from src.mission_control.mission_models import MissionAuthorizationContext
from src.execution_control.action_models import ExecutionAction
from src.execution_control.authorization_models import AuthorizationRecord
import os

from .models import (
    CoordinationMission,
    MissionPriority,
    ResourceDescriptor,
    ResourceRequest,
    ResourceLease,
    ConflictRecord,
    ArbitrationDecision,
    CoordinationBudget,
    CoordinationOutcome,
)
from .mission_registry import MissionRegistry
from .resource_registry import ResourceRegistry
from .resource_manager import ResourceManager
from .arbitration import ArbitrationEngine
from .conflict import ConflictEngine
from .fairness import FairnessEngine
from .leases import LeaseManager
from .capacity import CapacityTracker
from .preemption import PreemptionEngine
from .deadlock import DeadlockDetector
from .coordination_ledger import CoordinationLedger
from .exceptions import (
    CoordinationException,
    MissionAdmissionDenied,
    ResourceUnavailable,
    ResourceConflict,
    ReservationExpired,
    CoordinationDeadlock,
    CoordinationBudgetExceeded,
    CrossMissionAuthorizationError,
    CoordinationPolicyViolation,
)


class MultiMissionCoordinator:
    """Primary Multi-Mission Coordination & Resource Governance Engine."""

    def __init__(
        self,
        phase11_coordinator: Optional[MissionCoordinator] = None,
        max_concurrent_missions: int = 20,
        global_budget: Optional[CoordinationBudget] = None,
        ledger: Optional[CoordinationLedger] = None,
        ledger_dir: Optional[str] = None,
    ):
        if ledger_dir and not phase11_coordinator:
            p11_ledger_dir = os.path.join(ledger_dir, "phase11_ledger")
            p11_ledger = MissionLedger(base_dir=p11_ledger_dir)
            self.phase11_coordinator = MissionCoordinator(ledger=p11_ledger)
        else:
            self.phase11_coordinator = phase11_coordinator or MissionCoordinator()

        self.mission_registry = MissionRegistry(max_concurrent_missions=max_concurrent_missions)
        self.resource_registry = ResourceRegistry()
        self.resource_manager = ResourceManager(resource_registry=self.resource_registry)
        self.capacity_tracker = CapacityTracker(global_budget=global_budget)
        self.arbitration_engine = ArbitrationEngine(
            mission_registry=self.mission_registry,
            resource_manager=self.resource_manager,
            capacity_tracker=self.capacity_tracker,
        )
        self.conflict_engine = ConflictEngine()
        self.fairness_engine = FairnessEngine()
        self.preemption_engine = PreemptionEngine(resource_manager=self.resource_manager)
        self.deadlock_detector = DeadlockDetector()

        if ledger:
            self.ledger = ledger
        elif ledger_dir:
            p12_ledger_dir = os.path.join(ledger_dir, "phase12_ledger")
            self.ledger = CoordinationLedger(base_dir=p12_ledger_dir)
        else:
            self.ledger = CoordinationLedger()

        self._mission_authorizations: Dict[str, str] = {}  # mission_id -> authorization_id (for cross-mission check)
        self._wait_for_graph: Dict[str, Set[str]] = {}

    def admit_mission(
        self,
        mission_id: str,
        title: str,
        description: str,
        target_outcomes: List[str],
        priority: MissionPriority = MissionPriority.NORMAL,
        allowed_capabilities: Optional[Set[str]] = None,
        allowed_resources: Optional[Set[str]] = None,
    ) -> CoordinationMission:
        """Admits a mission into Phase 11 & Phase 12 registries."""
        # 1. Admit into Phase 12 Registry
        coord_mission = self.mission_registry.admit_mission(
            mission_id=mission_id,
            priority=priority,
        )

        # 2. Create Mission in Phase 11 Coordinator
        self.phase11_coordinator.create_mission(
            mission_id=mission_id,
            title=title,
            description=description,
            target_outcomes=target_outcomes,
            allowed_capabilities=allowed_capabilities,
            allowed_resources=allowed_resources,
        )

        self._emit_ledger_event(
            event_type="MISSION_ADMITTED",
            mission_id=mission_id,
            decision_id=f"adm_{mission_id}",
            reason_code="ADMISSION_SUCCESSFUL",
            new_state="ADMITTED",
        )

        return coord_mission

    def request_resources_and_arbitrate(
        self,
        requests: List[ResourceRequest]
    ) -> ArbitrationDecision:
        """Arbitrates resource requests across admitted missions."""
        decision = self.arbitration_engine.arbitrate_resource_requests(requests)

        for lease in decision.granted_leases:
            self._emit_ledger_event(
                event_type="RESOURCE_RESERVED",
                mission_id=lease.mission_id,
                resource_id=lease.resource_id,
                decision_id=decision.decision_id,
                reason_code="LEASE_GRANTED",
                new_state="RESERVED",
            )

        for conflict in decision.conflicts_detected:
            self._emit_ledger_event(
                event_type="CONFLICT_DETECTED",
                mission_id=conflict.mission_b_id,
                resource_id=conflict.resource_id,
                decision_id=decision.decision_id,
                reason_code=f"CONFLICT_{conflict.severity}",
                previous_state="RUNNING",
                new_state="PAUSED",
            )

        return decision

    def execute_mission_task(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Executes the next pending task for a mission after capacity checks."""
        mission = self.mission_registry.get_mission(mission_id)
        if mission.status not in ("ADMITTED", "RUNNING"):
            raise CoordinationPolicyViolation(f"Cannot execute task for mission in status '{mission.status}'.")

        # Capacity check & acquire staff slot
        self.capacity_tracker.acquire_staff_slot()
        try:
            res = self.phase11_coordinator.execute_next_task(mission_id)
            if res:
                self.capacity_tracker.record_token_consumption(1000)
            return res
        finally:
            self.capacity_tracker.release_staff_slot()

    def execute_controlled_action_for_mission(
        self,
        mission_id: str,
        action: ExecutionAction,
        authorization_record: AuthorizationRecord
    ) -> Dict[str, Any]:
        """Executes a side-effecting action after enforcing INV-12-005: No Cross-Mission Authorization Inheritance."""
        # 1. Enforce INV-12-005: Check authorization token isn't stolen from another mission
        for b_mission_id, b_auth_id in self._mission_authorizations.items():
            if b_auth_id == authorization_record.authorization_id and b_mission_id != mission_id:
                raise CrossMissionAuthorizationError(
                    f"Cross-Mission Authorization Reuse Violation: Token '{authorization_record.authorization_id}' bound to mission '{b_mission_id}' cannot be reused for '{mission_id}'."
                )

        if mission_id not in self._mission_authorizations:
            self._mission_authorizations[mission_id] = authorization_record.authorization_id

        # Sync authorization_context to Phase 11 mission
        p11_mission = self.phase11_coordinator._get_mission(mission_id)
        if authorization_record and not p11_mission.authorization_context.is_valid():
            caps = {c.value if hasattr(c, 'value') else str(c) for c in authorization_record.authorized_capabilities}
            exp_dt = (
                datetime.fromisoformat(authorization_record.expires_at)
                if isinstance(authorization_record.expires_at, str)
                else authorization_record.expires_at
            )
            p11_mission.authorization_context = MissionAuthorizationContext(
                authorization_token_id=authorization_record.authorization_id,
                authorized_by=authorization_record.authorizer_identity,
                expires_at=exp_dt,
                granted_capabilities=caps,
                granted_resources={authorization_record.resource_scope.scope_string},
            )

        # 2. Acquire global execution slot
        self.capacity_tracker.acquire_execution_slot()
        try:
            res = self.phase11_coordinator.execute_controlled_action(
                mission_id=mission_id,
                action=action,
                authorization_record=authorization_record,
            )

            self._emit_ledger_event(
                event_type="ACTION_EXECUTED",
                mission_id=mission_id,
                resource_id=action.resource_scope.scope_string,
                decision_id=action.action_id,
                reason_code="CONTROLLED_EXECUTION_SUCCESSFUL",
                previous_state="RUNNING",
                new_state="RUNNING",
            )

            return res
        finally:
            self.capacity_tracker.release_execution_slot()

    def resolve_deadlocks_and_preempt(self) -> Optional[CoordinationMission]:
        """Detects circular resource dependency deadlocks and preempts a deterministic victim."""
        cycle = self.deadlock_detector.detect_deadlock(self._wait_for_graph)
        if not cycle:
            return None

        active_missions = self.mission_registry.get_active_missions()
        victim = self.deadlock_detector.select_victim_mission(cycle, active_missions)

        # Preempt victim mission
        preempted = self.preemption_engine.preempt_mission(victim)
        self.mission_registry._missions[victim.mission_id] = preempted
        self.phase11_coordinator.pause_mission(victim.mission_id, reason="PREEMPTED_DEADLOCK_VICTIM")

        self._emit_ledger_event(
            event_type="MISSION_PREEMPTED",
            mission_id=victim.mission_id,
            decision_id=f"preempt_{victim.mission_id}",
            reason_code="DEADLOCK_VICTIM_PREEMPTED",
            previous_state=victim.status,
            new_state="PREEMPTED",
        )

        return preempted

    def cancel_mission(self, mission_id: str, reason: str = "USER_CANCEL") -> None:
        """Idempotently cancels a mission and releases all its active leases."""
        try:
            m = self.mission_registry.get_mission(mission_id)
            for lease in m.active_leases:
                self.resource_manager.release_lease(lease.lease_id)
            self.mission_registry.update_status(mission_id, "CANCELLED")
        except KeyError:
            pass

        self.phase11_coordinator.cancel_mission(mission_id, reason=reason)

        self._emit_ledger_event(
            event_type="MISSION_CANCELLED",
            mission_id=mission_id,
            decision_id=f"cnl_{mission_id}",
            reason_code=reason,
            previous_state="ACTIVE",
            new_state="CANCELLED",
        )

    def get_outcome(self) -> CoordinationOutcome:
        """Retrieves multi-mission coordination outcome summary."""
        active = self.mission_registry.get_active_missions()
        return CoordinationOutcome(
            admitted_missions=len(self.mission_registry._missions),
            completed_missions=sum(1 for m in self.mission_registry._missions.values() if m.status == "COMPLETED"),
            preempted_missions=sum(1 for m in self.mission_registry._missions.values() if m.status == "PREEMPTED"),
            resolved_conflicts=len(self.ledger.entries),
            total_granted_leases=len(self.resource_manager.lease_manager._issued_nonces),
            global_tokens_consumed=self.capacity_tracker.consumed_tokens,
        )

    def _emit_ledger_event(
        self,
        event_type: str,
        mission_id: str,
        decision_id: str,
        reason_code: str,
        previous_state: str = "N/A",
        new_state: str = "N/A",
        resource_id: Optional[str] = None
    ) -> None:
        """Records a event into the hash-linked coordination ledger."""
        self.ledger.record_coordination_event(
            event_type=event_type,
            mission_id=mission_id,
            resource_id=resource_id,
            decision_id=decision_id,
            reason_code=reason_code,
            previous_state=previous_state,
            new_state=new_state,
        )

"""
Phase 12 Deterministic Arbitration Engine.

Arbitrates competing resource requests across active concurrent missions using
priority weighting, fairness aging, conflict detection, and global capacity limits.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Set
import uuid

from .models import (
    CoordinationMission,
    ResourceRequest,
    ResourceLease,
    ArbitrationDecision,
    ConflictRecord,
)
from .mission_registry import MissionRegistry
from .resource_manager import ResourceManager
from .conflict import ConflictEngine
from .fairness import FairnessEngine
from .capacity import CapacityTracker
from .exceptions import ResourceUnavailable, ResourceConflict


class ArbitrationEngine:
    """Deterministic arbitration engine for multi-mission resource allocation."""

    def __init__(
        self,
        mission_registry: MissionRegistry,
        resource_manager: ResourceManager,
        capacity_tracker: Optional[CapacityTracker] = None
    ):
        self.registry = mission_registry
        self.resource_manager = resource_manager
        self.capacity_tracker = capacity_tracker or CapacityTracker()
        self.conflict_engine = ConflictEngine()
        self.fairness_engine = FairnessEngine()

    def arbitrate_resource_requests(
        self,
        requests: List[ResourceRequest],
        current_time: Optional[datetime] = None
    ) -> ArbitrationDecision:
        """Arbitrates resource requests across missions deterministically."""
        now = current_time or datetime.now(timezone.utc)
        decision_id = f"arb_{uuid.uuid4().hex[:8]}"

        active_missions = self.registry.get_active_missions()
        # Apply fairness aging to waiting missions
        active_missions = self.fairness_engine.check_and_apply_aging(active_missions, now)

        # Sort requests by mission effective priority rank ascending (lower = higher priority)
        def get_req_priority(req: ResourceRequest) -> float:
            try:
                m = self.registry.get_mission(req.mission_id)
                return self.fairness_engine.calculate_effective_priority(m, now)
            except KeyError:
                return 999.0

        sorted_requests = sorted(requests, key=get_req_priority)

        granted_leases: List[ResourceLease] = []
        conflicts_detected: List[ConflictRecord] = []
        granted_mission_id: Optional[str] = None
        deferred_mission_ids: List[str] = []

        for req in sorted_requests:
            # 1. Conflict Check
            conflicts = self.conflict_engine.detect_conflicts(req, active_missions)
            blocking = [c for c in conflicts if c.severity == "BLOCKING"]
            if blocking:
                conflicts_detected.extend(conflicts)
                deferred_mission_ids.append(req.mission_id)

                # Fail-closed: pause conflicting lower-priority mission status
                self.registry.update_status(req.mission_id, "PAUSED")
                continue

            # 2. Allocate via ResourceManager
            try:
                lease = self.resource_manager.allocate(req, current_time=now)
                granted_leases.append(lease)
                granted_mission_id = req.mission_id

                # Update active mission leases in registry
                m = self.registry.get_mission(req.mission_id)
                updated_leases = list(m.active_leases) + [lease]
                self.registry._missions[req.mission_id] = CoordinationMission(
                    mission_id=m.mission_id,
                    priority=m.priority,
                    admission_timestamp=m.admission_timestamp,
                    requested_resources=m.requested_resources,
                    active_leases=updated_leases,
                    status="RUNNING",
                    aging_boost=m.aging_boost,
                )
            except ResourceUnavailable:
                deferred_mission_ids.append(req.mission_id)

        return ArbitrationDecision(
            decision_id=decision_id,
            granted_mission_id=granted_mission_id,
            deferred_mission_ids=deferred_mission_ids,
            reason_code="ARBITRATION_SUCCESSFUL" if granted_leases else "ARBITRATION_DEFERRED",
            granted_leases=granted_leases,
            conflicts_detected=conflicts_detected,
            timestamp=now,
        )

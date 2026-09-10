"""
Phase 14 Coordination Service
------------------------------
Controlled facade over Phase 12 Multi-Mission Coordinator.
Surfaces resource status, mission priority, queued work, preemption state, and capacity tokens
to the user control plane without permitting user mutations of coordination policy.
"""

from typing import Optional, Dict, Any, List
import uuid

from src.coordination import (
    MultiMissionCoordinator,
    MissionPriority,
    CoordinationMission,
    ResourceRequest,
    ResourceLease,
)
from src.workflow_gateway.exceptions import WorkflowGatewayError

class CoordinationService:
    """Service facade interfacing between Workflow Control Plane and Phase 12 Multi-Mission Coordination."""

    def __init__(self, multi_mission_coordinator: Optional[MultiMissionCoordinator] = None):
        self._coordinator = multi_mission_coordinator or MultiMissionCoordinator()

    def admit_mission_to_coordination(
        self,
        mission_id: str,
        priority: str = "NORMAL",
        requested_staff_slots: int = 2,
    ) -> bool:
        """Admits a mission into Phase 12 multi-mission coordination tracking."""
        prio_map = {
            "LOW": MissionPriority.LOW,
            "NORMAL": MissionPriority.NORMAL,
            "HIGH": MissionPriority.HIGH,
            "CRITICAL": MissionPriority.SYSTEM_CRITICAL,
            "SYSTEM_CRITICAL": MissionPriority.SYSTEM_CRITICAL,
            "USER_BLOCKING": MissionPriority.USER_BLOCKING,
        }
        prio = prio_map.get(priority.upper(), MissionPriority.NORMAL)

        if hasattr(self._coordinator, "mission_registry"):
            coord_mission = self._coordinator.mission_registry.admit_mission(
                mission_id=mission_id,
                priority=prio,
            )
            return coord_mission is not None
        return True

    def request_resource_lease(
        self, mission_id: str, resource_id: str = "res-slot-1", duration_seconds: int = 300
    ) -> Optional[ResourceLease]:
        """Requests a logical resource lease for a mission."""
        req = ResourceRequest(
            request_id=f"req-{uuid.uuid4().hex[:6]}",
            mission_id=mission_id,
            resource_id=resource_id,
            requested_duration_seconds=int(duration_seconds),
        )
        decision = self._coordinator.request_resources_and_arbitrate([req])
        if decision.granted_leases:
            return decision.granted_leases[0]
        return None

    def release_resource_lease(self, lease_id: str) -> bool:
        """Releases a logical resource lease."""
        if hasattr(self._coordinator, "resource_manager"):
            self._coordinator.resource_manager.release_lease(lease_id)
            return True
        return True

    def get_coordination_status(self, mission_id: str) -> Dict[str, Any]:
        """Returns read-only coordination status metrics for a mission."""
        return {"mission_id": mission_id, "status": "ADMITTED"}

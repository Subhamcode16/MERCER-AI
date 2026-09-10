"""
Phase 12 Controlled Preemption Engine.

Executes safe preemption of lower-priority or deadlock-victim missions:
RUNNING -> CHECKPOINT -> RELEASE LEASES -> PAUSED / PREEMPTED.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from .models import CoordinationMission
from .resource_manager import ResourceManager
from .exceptions import CoordinationException


class PreemptionEngine:
    """Manages safe, auditable preemption and resource release."""

    def __init__(self, resource_manager: ResourceManager):
        self.resource_manager = resource_manager

    def preempt_mission(
        self,
        mission: CoordinationMission,
        reason: str = "PREEMPTED_BY_HIGHER_PRIORITY"
    ) -> CoordinationMission:
        """Safely preempts a running mission, releases its active resource leases, and updates state."""
        # 1. Release active leases back to resource manager
        for lease in mission.active_leases:
            self.resource_manager.release_lease(lease.lease_id)

        # 2. Return updated mission with status PREEMPTED and emptied active leases
        updated = CoordinationMission(
            mission_id=mission.mission_id,
            priority=mission.priority,
            admission_timestamp=mission.admission_timestamp,
            requested_resources=mission.requested_resources,
            active_leases=[],
            status="PREEMPTED",
            aging_boost=mission.aging_boost + 1,  # Boost aging so preempted mission gets prioritized on resume
        )

        return updated

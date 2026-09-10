"""
Phase 12 Multi-Mission Registry & Admission Controller.

Thread-safe registry managing active concurrent missions, admission bounds,
concurrency limits, lifecycle status indexing, and mission ownership tracking.
"""

import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .models import CoordinationMission, MissionPriority
from .exceptions import MissionAdmissionDenied, CoordinationPolicyViolation


class MissionRegistry:
    """Thread-safe registry for concurrent admitted missions."""

    def __init__(self, max_concurrent_missions: int = 20):
        self.max_concurrent_missions = max_concurrent_missions
        self._missions: Dict[str, CoordinationMission] = {}
        self._lock = threading.RLock()

    def admit_mission(
        self,
        mission_id: str,
        priority: MissionPriority = MissionPriority.NORMAL,
        admission_time: Optional[datetime] = None
    ) -> CoordinationMission:
        """Admits a mission into the registry if bounds permit."""
        with self._lock:
            if mission_id in self._missions:
                raise MissionAdmissionDenied(f"Mission '{mission_id}' is already registered.")

            active_count = sum(
                1 for m in self._missions.values()
                if m.status in ("ADMITTED", "RUNNING", "PREEMPTED", "PAUSED")
            )
            if active_count >= self.max_concurrent_missions:
                raise MissionAdmissionDenied(
                    f"Admission limit reached ({active_count} >= {self.max_concurrent_missions})."
                )

            now = admission_time or datetime.now(timezone.utc)
            mission = CoordinationMission(
                mission_id=mission_id,
                priority=priority,
                admission_timestamp=now,
                status="ADMITTED",
            )

            self._missions[mission_id] = mission
            return mission

    def get_mission(self, mission_id: str) -> CoordinationMission:
        """Retrieves a mission from the registry."""
        with self._lock:
            if mission_id not in self._missions:
                raise KeyError(f"Mission '{mission_id}' not found in registry.")
            return self._missions[mission_id]

    def update_status(self, mission_id: str, new_status: str) -> CoordinationMission:
        """Thread-safely updates a mission's status."""
        with self._lock:
            mission = self.get_mission(mission_id)
            updated = CoordinationMission(
                mission_id=mission.mission_id,
                priority=mission.priority,
                admission_timestamp=mission.admission_timestamp,
                requested_resources=mission.requested_resources,
                active_leases=mission.active_leases,
                status=new_status,
                aging_boost=mission.aging_boost,
            )
            self._missions[mission_id] = updated
            return updated

    def update_aging_boost(self, mission_id: str, boost: int) -> CoordinationMission:
        """Updates dynamic priority aging boost counter for fairness."""
        with self._lock:
            mission = self.get_mission(mission_id)
            updated = CoordinationMission(
                mission_id=mission.mission_id,
                priority=mission.priority,
                admission_timestamp=mission.admission_timestamp,
                requested_resources=mission.requested_resources,
                active_leases=mission.active_leases,
                status=mission.status,
                aging_boost=boost,
            )
            self._missions[mission_id] = updated
            return updated

    def get_active_missions(self) -> List[CoordinationMission]:
        """Returns list of all active (non-completed, non-cancelled) missions."""
        with self._lock:
            return [
                m for m in self._missions.values()
                if m.status in ("ADMITTED", "RUNNING", "PAUSED", "PREEMPTED")
            ]

    def remove_mission(self, mission_id: str) -> None:
        """Removes a mission from registry (upon terminal completion or cancellation)."""
        with self._lock:
            if mission_id in self._missions:
                del self._missions[mission_id]

    @property
    def active_count(self) -> int:
        """Returns count of active registered missions."""
        with self._lock:
            return len(self.get_active_missions())

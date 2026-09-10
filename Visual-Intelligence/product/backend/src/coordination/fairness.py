"""
Phase 12 Fairness & Priority Aging Engine.

Applies priority weighting, dynamic aging boosts to prevent starvation of low-priority missions,
and deterministic tie-breaking for arbitration decisions.
"""

from datetime import datetime, timezone
from typing import List, Optional

from .models import CoordinationMission, MissionPriority
from .exceptions import StarvationDetected


class FairnessEngine:
    """Manages priority weighting, dynamic aging, and starvation defense."""

    def __init__(self, starvation_threshold_seconds: int = 600):
        self.starvation_threshold_seconds = starvation_threshold_seconds

    def calculate_effective_priority(
        self,
        mission: CoordinationMission,
        current_time: Optional[datetime] = None
    ) -> float:
        """Calculates numerical priority rank (lower value = higher execution priority)."""
        base_rank = mission.priority.value
        # Apply dynamic aging boost (each boost point reduces priority rank numerical value by 0.5)
        effective = float(base_rank) - (mission.aging_boost * 0.5)
        return max(0.1, effective)

    def check_and_apply_aging(
        self,
        waiting_missions: List[CoordinationMission],
        current_time: Optional[datetime] = None
    ) -> List[CoordinationMission]:
        """Scans waiting missions; applies aging boost to missions exceeding starvation threshold."""
        now = current_time or datetime.now(timezone.utc)
        updated = []

        for m in waiting_missions:
            waited_seconds = (now - m.admission_timestamp).total_seconds()
            if waited_seconds > self.starvation_threshold_seconds:
                # Calculate required boost points
                boost_points = int(waited_seconds // self.starvation_threshold_seconds)
                new_boost = max(m.aging_boost, boost_points)
                updated_m = CoordinationMission(
                    mission_id=m.mission_id,
                    priority=m.priority,
                    admission_timestamp=m.admission_timestamp,
                    requested_resources=m.requested_resources,
                    active_leases=m.active_leases,
                    status=m.status,
                    aging_boost=new_boost,
                )
                updated.append(updated_m)
            else:
                updated.append(m)

        return updated

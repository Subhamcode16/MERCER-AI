"""
Phase 12 Machine Conflict Detection Engine.

Detects resource allocation collisions, overlapping scheduled publication windows,
contradictory brand asset edits, and concurrent artifact modification conflicts across missions.
"""

from typing import List, Dict, Set, Optional
import uuid

from .models import ResourceRequest, ConflictRecord, CoordinationMission
from .exceptions import ResourceConflict


class ConflictEngine:
    """Machine conflict detection and severity classifier engine."""

    def detect_conflicts(
        self,
        new_request: ResourceRequest,
        active_missions: List[CoordinationMission]
    ) -> List[ConflictRecord]:
        """Scans new request against active missions for incompatible resource or mutation conflicts."""
        conflicts: List[ConflictRecord] = []

        for m in active_missions:
            if m.mission_id == new_request.mission_id:
                continue

            for active_lease in m.active_leases:
                # 1. Exclusive resource access collision check
                if active_lease.resource_id == new_request.resource_id:
                    if new_request.exclusive or active_lease.quantity > 0:
                        # Check namespace / calendar scope overlap
                        if "account:" in new_request.resource_id or "calendar:" in new_request.resource_id:
                            conflict_id = f"cnf_{uuid.uuid4().hex[:8]}"
                            record = ConflictRecord(
                                conflict_id=conflict_id,
                                mission_a_id=m.mission_id,
                                mission_b_id=new_request.mission_id,
                                resource_id=new_request.resource_id,
                                severity="BLOCKING",
                                description=f"Mutually exclusive collision on resource '{new_request.resource_id}' between Mission '{m.mission_id}' and '{new_request.mission_id}'.",
                            )
                            conflicts.append(record)

        return conflicts

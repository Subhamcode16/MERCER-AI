"""
Unit tests for Phase 12 Machine Conflict Engine.
"""

import pytest
from datetime import datetime, timezone

from src.coordination.conflict import ConflictEngine
from src.coordination.models import ResourceRequest, CoordinationMission, MissionPriority, ResourceLease


def test_conflict_detection_on_exclusive_resources():
    engine = ConflictEngine()

    lease = ResourceLease(
        lease_id="l1",
        mission_id="m1",
        resource_id="account:nocap_social",
        quantity=1,
        issued_at=datetime.now(timezone.utc).isoformat(),
        expires_at=datetime.now(timezone.utc).isoformat(),
        nonce="n1",
    )

    m1 = CoordinationMission(
        mission_id="m1",
        priority=MissionPriority.HIGH,
        admission_timestamp=datetime.now(timezone.utc),
        active_leases=[lease],
    )

    req = ResourceRequest("req2", "m2", "account:nocap_social", quantity=1, exclusive=True)
    conflicts = engine.detect_conflicts(req, [m1])

    assert len(conflicts) == 1
    assert conflicts[0].severity == "BLOCKING"
    assert conflicts[0].mission_a_id == "m1"
    assert conflicts[0].mission_b_id == "m2"

"""
Unit tests for Phase 12 Preemption Engine.
"""

import pytest
from datetime import datetime, timezone

from src.coordination.preemption import PreemptionEngine
from src.coordination.resource_manager import ResourceManager
from src.coordination.models import CoordinationMission, MissionPriority, ResourceRequest


def test_safe_preemption_and_lease_release():
    mgr = ResourceManager()
    engine = PreemptionEngine(mgr)

    req = ResourceRequest("req1", "m_low", "staff:designer", quantity=1)
    lease = mgr.allocate(req)

    m = CoordinationMission(
        mission_id="m_low",
        priority=MissionPriority.LOW,
        admission_timestamp=datetime.now(timezone.utc),
        active_leases=[lease],
        status="RUNNING",
    )

    preempted = engine.preempt_mission(m)
    assert preempted.status == "PREEMPTED"
    assert preempted.active_leases == []
    assert mgr.get_allocated_quantity("staff:designer") == 0

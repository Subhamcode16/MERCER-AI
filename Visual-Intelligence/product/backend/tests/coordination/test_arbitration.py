"""
Unit tests for Phase 12 Arbitration Engine.
"""

import pytest

from src.coordination.arbitration import ArbitrationEngine
from src.coordination.mission_registry import MissionRegistry
from src.coordination.resource_manager import ResourceManager
from src.coordination.models import ResourceRequest, MissionPriority


def test_arbitration_priority_ordering():
    reg = MissionRegistry()
    reg.admit_mission("m_low", priority=MissionPriority.LOW)
    reg.admit_mission("m_high", priority=MissionPriority.HIGH)

    mgr = ResourceManager()
    arb = ArbitrationEngine(reg, mgr)

    # Competes for 1 capacity account resource
    req1 = ResourceRequest("r1", "m_low", "account:nocap_social", quantity=1)
    req2 = ResourceRequest("r2", "m_high", "account:nocap_social", quantity=1)

    decision = arb.arbitrate_resource_requests([req1, req2])
    assert decision.granted_mission_id == "m_high"
    assert decision.deferred_mission_ids == ["m_low"]

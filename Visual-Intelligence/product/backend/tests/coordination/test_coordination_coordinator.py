"""
Unit tests for Phase 12 MultiMissionCoordinator.
"""

import pytest

from src.coordination.coordinator import MultiMissionCoordinator
from src.coordination.models import MissionPriority, ResourceRequest


def test_multi_mission_coordinator_admit_and_arbitrate(tmp_path):
    coord = MultiMissionCoordinator(ledger_dir=str(tmp_path))

    m1 = coord.admit_mission(
        mission_id="m_coord_1",
        title="Mission 1",
        description="Desc 1",
        target_outcomes=["Complete"],
        priority=MissionPriority.HIGH,
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )
    assert m1.mission_id == "m_coord_1"

    req = ResourceRequest("req1", "m_coord_1", "staff:designer", quantity=1)
    decision = coord.request_resources_and_arbitrate([req])

    assert decision.granted_mission_id == "m_coord_1"
    assert len(decision.granted_leases) == 1
    assert coord.ledger.verify_ledger_integrity() is True

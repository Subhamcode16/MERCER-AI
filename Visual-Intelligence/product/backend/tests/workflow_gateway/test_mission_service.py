"""
Phase 14 Test Mission Service
-----------------------------
Tests Phase 11 mission control facade, pause, resume, and cancellation terminal lock.
"""

import pytest
from src.workflow_gateway.mission_service import MissionService
from src.mission_control import MissionState

def test_mission_lifecycle_facade():
    service = MissionService()
    m_id = service.create_mission_for_workflow(
        workflow_id="wf-m-1",
        title="Test Campaign",
        description="Campaign objective",
        max_budget=100.0,
    )

    tasks = [{"task_type": "DRAFT", "capability": "CREATE_DRAFT"}]
    service.build_mission_graph(m_id, tasks)

    state = service.start_mission(m_id)
    assert state == MissionState.RUNNING

    state = service.pause_mission(m_id, reason="User pause")
    assert state == MissionState.PAUSED

    state = service.resume_mission(m_id)
    assert state == MissionState.RUNNING

    state = service.cancel_mission(m_id, reason="User cancel")
    assert state == MissionState.CANCELLED

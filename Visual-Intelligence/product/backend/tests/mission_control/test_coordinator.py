"""
Unit tests for Phase 11 Mission Coordinator.
"""

import pytest

from src.mission_control.coordinator import MissionCoordinator
from src.mission_control.mission_models import MissionBudget
from src.mission_control.exceptions import SecurityBoundaryViolation, InvalidMissionStateError


def test_coordinator_create_and_run_mission(tmp_path):
    coord = MissionCoordinator()

    mission = coord.create_mission(
        mission_id="m_coord_1",
        title="Coordination Test",
        description="Test description",
        target_outcomes=["Complete"],
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )

    assert mission.state == "PLANNED"

    coord.prepare_mission("m_coord_1")
    assert mission.state == "READY"

    coord.add_task(
        mission_id="m_coord_1",
        task_id="t1",
        workflow_id="wf_01",
        assigned_role="RESEARCHER",
        description="Research streetwear trends",
    )

    coord.start_mission("m_coord_1")
    assert mission.state == "RUNNING"

    res = coord.execute_next_task("m_coord_1")
    assert res is not None
    assert res["task_id"] == "t1"
    assert mission.state == "COMPLETED"


def test_coordinator_boundary_violation_on_task_addition():
    coord = MissionCoordinator()

    coord.create_mission(
        mission_id="m_coord_2",
        title="Boundary Test",
        description="Test",
        target_outcomes=[],
        allowed_capabilities={"CREATE_DRAFT"},
    )

    # Task requesting capability outside allowed_capabilities raises SecurityBoundaryViolation
    with pytest.raises(SecurityBoundaryViolation):
        coord.add_task(
            mission_id="m_coord_2",
            task_id="t_unauth",
            workflow_id="wf_02",
            assigned_role="STRATEGIST",
            description="Unauthorized task",
            required_capabilities={"ADMIN_EXECUTE"},
        )

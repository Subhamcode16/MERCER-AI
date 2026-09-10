"""
Failure & Recovery tests for Phase 11.
"""

import pytest

from src.mission_control.coordinator import MissionCoordinator


def test_partial_task_failure_recovery():
    coord = MissionCoordinator()
    coord.create_mission(mission_id="m_fail_1", title="Fail Test", description="D", target_outcomes=[])
    coord.prepare_mission("m_fail_1")

    coord.add_task(mission_id="m_fail_1", task_id="t1", workflow_id="wf_1", assigned_role="RESEARCHER", description="R")
    coord.add_task(mission_id="m_fail_1", task_id="t2", workflow_id="wf_1", assigned_role="DESIGNER", description="D", dependencies=["t1"])

    graph = coord.graphs["m_fail_1"]
    blocked = graph.mark_task_failed("t1")

    assert blocked == ["t2"]
    assert graph.nodes["t2"].status == "BLOCKED"

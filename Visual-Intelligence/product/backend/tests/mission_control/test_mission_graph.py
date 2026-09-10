"""
Unit tests for Phase 11 Mission Graph (Bounded DAG).
"""

import pytest

from src.mission_control.mission_graph import MissionGraph, MissionTaskNode
from src.mission_control.exceptions import InvalidMissionGraphError


def test_mission_graph_topological_sort():
    graph = MissionGraph(max_depth=5, max_tasks=10)

    node1 = MissionTaskNode(task_id="t1", workflow_id="wf_1", assigned_role="RESEARCHER", description="Research")
    node2 = MissionTaskNode(task_id="t2", workflow_id="wf_1", assigned_role="DESIGNER", description="Design", dependencies=["t1"])
    node3 = MissionTaskNode(task_id="t3", workflow_id="wf_1", assigned_role="REVIEWER", description="Review", dependencies=["t2"])

    graph.add_task(node1)
    graph.add_task(node2)
    graph.add_task(node3)

    order = graph.get_execution_order()
    assert order == ["t1", "t2", "t3"]


def test_mission_graph_cycle_detection():
    graph = MissionGraph(max_depth=5, max_tasks=10)

    n1 = MissionTaskNode(task_id="t1", workflow_id="wf_1", assigned_role="RESEARCHER", description="R", dependencies=[])
    graph.add_task(n1)

    n2 = MissionTaskNode(task_id="t2", workflow_id="wf_1", assigned_role="DESIGNER", description="D", dependencies=["t1"])
    graph.add_task(n2)

    with pytest.raises(InvalidMissionGraphError):
        # Manually introduce cycle t2 -> t1
        graph.adj_list["t2"].append("t1")
        graph.in_degree["t1"] += 1
        graph.validate_graph()


def test_mission_graph_task_count_limit():
    graph = MissionGraph(max_depth=5, max_tasks=2)
    graph.add_task(MissionTaskNode(task_id="t1", workflow_id="wf_1", assigned_role="RESEARCHER", description="R"))
    graph.add_task(MissionTaskNode(task_id="t2", workflow_id="wf_1", assigned_role="DESIGNER", description="D"))

    with pytest.raises(InvalidMissionGraphError):
        graph.add_task(MissionTaskNode(task_id="t3", workflow_id="wf_1", assigned_role="REVIEWER", description="Rev"))


def test_task_failure_propagation():
    graph = MissionGraph()
    n1 = MissionTaskNode(task_id="t1", workflow_id="wf_1", assigned_role="RESEARCHER", description="R")
    n2 = MissionTaskNode(task_id="t2", workflow_id="wf_1", assigned_role="DESIGNER", description="D", dependencies=["t1"])
    graph.add_task(n1)
    graph.add_task(n2)

    blocked = graph.mark_task_failed("t1")
    assert blocked == ["t2"]
    assert graph.nodes["t1"].status == "FAILED"
    assert graph.nodes["t2"].status == "BLOCKED"

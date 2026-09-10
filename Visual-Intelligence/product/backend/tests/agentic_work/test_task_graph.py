"""
Tests for TaskGraph: dependency resolution, parallel execution, max 3 revision bounds.
"""

from src.agentic_work import TaskGraph, StaffTask, StaffRole, TaskStatus


def test_task_graph_dependency_resolution():
    graph = TaskGraph("wf-test-01")

    t1 = StaffTask("t1", "wf-test-01", StaffRole.RESEARCHER, "Research")
    t2 = StaffTask("t2", "wf-test-01", StaffRole.STRATEGIST, "Strategy", dependencies=["t1"])

    graph.add_task(t1)
    graph.add_task(t2)

    ready = graph.get_ready_tasks()
    assert len(ready) == 1
    assert ready[0].task_id == "t1"

    graph.mark_completed("t1", {"out": "ok"})

    ready2 = graph.get_ready_tasks()
    assert len(ready2) == 1
    assert ready2[0].task_id == "t2"


def test_task_graph_revision_limit():
    graph = TaskGraph("wf-test-02", max_revisions=3)
    t1 = StaffTask("t1", "wf-test-02", StaffRole.DESIGNER, "Design")
    graph.add_task(t1)

    assert graph.request_revision("t1", ["Fix 1"]) is True
    assert graph.request_revision("t1", ["Fix 2"]) is True
    assert graph.request_revision("t1", ["Fix 3"]) is True
    assert graph.request_revision("t1", ["Fix 4"]) is False  # Limit exceeded!

    assert graph.get_task("t1").status == TaskStatus.BLOCKED

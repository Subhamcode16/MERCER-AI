"""
Tests for Context Scoping: TaskContext and StaffContext isolation.
"""

from src.agentic_work import TaskContext, StaffContext, StaffRole


def test_context_scoping_isolation():
    t_ctx = TaskContext(
        task_id="t1",
        workflow_id="wf1",
        role=StaffRole.DESIGNER,
        objective="Design lookbook",
        inputs={"palette": "ivory"},
    )
    s_ctx = StaffContext(
        staff_id="s1",
        role=StaffRole.DESIGNER,
        task_context=t_ctx,
        allowed_tools=["color_picker"],
    )

    assert s_ctx.task_context.task_id == "t1"
    assert s_ctx.allowed_tools == ["color_picker"]

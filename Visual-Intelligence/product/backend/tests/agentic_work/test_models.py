"""
Tests for Agentic Work Models: schema validation, type safety, boolean confusion rejection.
"""

import pytest
from src.agentic_work import (
    StaffRole,
    TaskStatus,
    StaffCapability,
    StaffTask,
    StaffResult,
    LearningSignal,
    AdaptiveChange,
)


def test_staff_task_valid():
    task = StaffTask(
        task_id="t-001",
        workflow_id="wf-001",
        role=StaffRole.RESEARCHER,
        objective="Collect lookbook research.",
    )
    assert task.task_id == "t-001"
    assert task.role == StaffRole.RESEARCHER
    assert task.status == TaskStatus.PENDING


def test_staff_task_invalid_role():
    with pytest.raises(ValueError):
        StaffTask(
            task_id="t-002",
            workflow_id="wf-001",
            role="INVALID_ROLE",
            objective="Test",
        )


def test_staff_result_is_authoritative_rejection():
    with pytest.raises(ValueError):
        StaffResult(
            task_id="t-001",
            staff_id="s-001",
            role=StaffRole.DESIGNER,
            status=TaskStatus.COMPLETED,
            output_data={},
            execution_time_seconds=1.0,
            is_authoritative=True,  # MUST raise ValueError!
        )


def test_learning_signal_security_policy_rejection():
    with pytest.raises(ValueError):
        LearningSignal(
            signal_id="sig-001",
            workflow_id="wf-001",
            task_id=None,
            source="USER_FEEDBACK",
            category="SECURITY_POLICY",  # MUST raise ValueError!
            observed_failure="test",
            expected_behavior="test",
            correction="test",
        )


def test_adaptive_change_forbidden_target_rejection():
    with pytest.raises(ValueError):
        AdaptiveChange(
            change_id="chg-001",
            target_component="EXECUTION_GATE",  # MUST raise ValueError!
            previous_version="v1",
            proposed_version="v2",
            reason="test",
            supporting_signals=[],
        )

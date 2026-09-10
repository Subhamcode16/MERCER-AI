"""
Phase 10 — Action Models Unit Tests
"""

import pytest
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import ExecutionControlException, CapabilityViolationError
from src.execution_control.resource_scope import ResourceScope


def test_planned_effect_to_dict():
    effect = PlannedEffect(
        effect_type="CREATE_DRAFT",
        target_system="SANDBOX_CMS",
        description="Create campaign draft",
        reversible=True,
    )
    d = effect.to_dict()
    assert d["effect_type"] == "CREATE_DRAFT"
    assert d["reversible"] is True


def test_execution_action_creation():
    effect = PlannedEffect(
        effect_type="PUBLISH",
        target_system="SANDBOX_SOCIAL",
        description="Publish social post",
        reversible=False,
    )
    scope = ResourceScope("brand:aura/campaign:fall2026")

    action = ExecutionAction(
        action_id="act_001",
        workflow_id="wf_100",
        task_id="t4_content",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=scope,
        input_payload={"text": "Fall Collection Launch"},
        planned_effect=effect,
    )

    assert action.action_id == "act_001"
    assert action.capability == ExecutionCapability.PUBLISH_CONTENT
    assert len(action.input_commitment_hash) == 64  # SHA-256 string length


def test_execution_action_rejects_empty_ids():
    effect = PlannedEffect("PUBLISH", "SYS", "Desc")
    scope = ResourceScope("brand:aura")

    with pytest.raises(ExecutionControlException):
        ExecutionAction(
            action_id="",
            workflow_id="wf_100",
            task_id="t1",
            capability=ExecutionCapability.PUBLISH_CONTENT,
            resource_scope=scope,
            input_payload={},
            planned_effect=effect,
        )


def test_execution_action_rejects_forbidden_capability():
    effect = PlannedEffect("PUBLISH", "SYS", "Desc")
    scope = ResourceScope("brand:aura")

    with pytest.raises(CapabilityViolationError):
        ExecutionAction(
            action_id="act_bad",
            workflow_id="wf_100",
            task_id="t1",
            capability="ALLOW_ALL",  # Forbidden capability string
            resource_scope=scope,
            input_payload={},
            planned_effect=effect,
        )

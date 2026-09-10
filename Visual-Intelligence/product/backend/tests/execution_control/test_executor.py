"""
Phase 10 — Execution Controller Pipeline Unit Tests
"""

import shutil
import tempfile
import pytest

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.adapters import SocialPlatformAdapter
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import (
    AdapterNotFoundError,
    CapabilityViolationError,
    ResourceScopeViolationError,
)
from src.execution_control.execution_ledger import ExecutionLedger
from src.execution_control.executor import ExecutionController
from src.execution_control.idempotency import IdempotencyGuard
from src.execution_control.resource_scope import ResourceScope


@pytest.fixture
def temp_exec_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_executor_pipeline_success(temp_exec_dir):
    ledger = ExecutionLedger(base_dir=temp_exec_dir)
    controller = ExecutionController(ledger=ledger)
    adapter = SocialPlatformAdapter()
    controller.register_adapter(adapter)

    human_boundary = HumanAuthorizationBoundary()
    auth = human_boundary.issue_human_authorization(
        request_id="req_pub",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        human_operator_id="HUMAN_OPERATOR_ALICE",
        decision_reference="DEC_100",
    )

    act = ExecutionAction(
        action_id="act_pub_100",
        workflow_id="wf_100",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={"text": "Publish post"},
        planned_effect=PlannedEffect("PUB", "SANDBOX_SOCIAL", "Publish post"),
    )

    res = controller.execute_action(act, auth)
    assert res.success is True
    assert res.output_data["status"] == "PUBLISHED"


def test_executor_rejects_missing_human_authorization():
    controller = ExecutionController()
    adapter = SocialPlatformAdapter()
    controller.register_adapter(adapter)

    act = ExecutionAction(
        action_id="act_no_auth",
        workflow_id="wf_100",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,  # Requires human authorization!
        resource_scope=ResourceScope("brand:aura"),
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SANDBOX_SOCIAL", "Publish post"),
    )

    with pytest.raises(PermissionError):
        controller.execute_action(act, authorization_record=None)


def test_executor_rejects_resource_boundary_breach():
    controller = ExecutionController()
    adapter = SocialPlatformAdapter()
    controller.register_adapter(adapter)

    human_boundary = HumanAuthorizationBoundary()
    auth_restricted = human_boundary.issue_human_authorization(
        request_id="req_scope",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),  # Authorized for brand:aura only
        human_operator_id="HUMAN_OPERATOR_BOB",
        decision_reference="DEC_101",
    )

    act_breach = ExecutionAction(
        action_id="act_breach",
        workflow_id="wf_100",
        task_id="t1",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=ResourceScope("brand:other_brand"),  # Breach attempt!
        input_payload={},
        planned_effect=PlannedEffect("PUB", "SANDBOX_SOCIAL", "Publish post"),
    )

    with pytest.raises(ResourceScopeViolationError):
        controller.execute_action(act_breach, auth_restricted)

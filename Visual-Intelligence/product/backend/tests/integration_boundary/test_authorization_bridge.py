"""
Unit tests for Phase 13 Authorization Bridge (INV-13-001 & INV-13-006).
"""

from datetime import datetime, timezone, timedelta
import pytest

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.integration_boundary.authorization_bridge import AuthorizationBridge
from src.integration_boundary.exceptions import AuthorizationScopeMismatchError


def test_authorization_bridge_validation():
    bridge = AuthorizationBridge()
    human_boundary = HumanAuthorizationBoundary()
    now = datetime.now(timezone.utc)

    auth = human_boundary.issue_human_authorization(
        request_id="req_bridge_01",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_01",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    action = ExecutionAction(
        action_id="act_01",
        workflow_id="wf_01",
        task_id="t_01",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={"text": "Hello"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Draft"),
    )

    # 1. Valid authorization passes
    bridge.validate_authorization_for_external_call(
        authorization_record=auth,
        action=action,
        mission_id="m_01",
    )

    # 2. Missing authorization token raises AuthorizationScopeMismatchError (INV-13-001)
    with pytest.raises(AuthorizationScopeMismatchError):
        bridge.validate_authorization_for_external_call(
            authorization_record=None,
            action=action,
            mission_id="m_01",
        )

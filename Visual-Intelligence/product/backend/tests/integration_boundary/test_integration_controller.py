"""
Unit tests for Phase 13 Integration Controller end-to-end pipeline.
"""

from datetime import datetime, timezone, timedelta
import pytest

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.integration_boundary.integration_controller import IntegrationController
from src.integration_boundary.mock_social_provider import MockSocialProvider
from src.integration_boundary.models import ProviderEnvironment, IntegrationOutcomeClass


def test_integration_controller_full_pipeline(tmp_path):
    ctrl = IntegrationController(ledger_dir=str(tmp_path))
    provider = MockSocialProvider()
    ctrl.register_provider(provider)

    ctrl.credential_gateway.register_credential_handle(
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        reference_id="ref_social_sandbox",
        secret_handle="SECRET_OPAQUE_SANDBOX_KEY",
    )

    human_boundary = HumanAuthorizationBoundary()
    now = datetime.now(timezone.utc)
    auth = human_boundary.issue_human_authorization(
        request_id="req_ctrl_01",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_01",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    action = ExecutionAction(
        action_id="act_ctrl_01",
        workflow_id="wf_01",
        task_id="t_01",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={"text": "Autumn drop post draft"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Post draft"),
    )

    outcome = ctrl.execute_external_tool(
        mission_id="m_nocap_01",
        provider_id="mock_social",
        operation_name="create_draft",
        target_environment=ProviderEnvironment.SANDBOX,
        action=action,
        authorization_record=auth,
        user_idempotency_key="key_01",
    )

    assert outcome.outcome_class == IntegrationOutcomeClass.SUCCESS
    assert outcome.reconciled is True
    assert ctrl.ledger.verify_ledger_integrity() is True

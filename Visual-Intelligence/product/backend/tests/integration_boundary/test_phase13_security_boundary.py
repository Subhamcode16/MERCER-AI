"""
Phase 13 Threat Matrix & Security Boundary Tests (T13-1 through T13-16).
"""

from datetime import datetime, timezone, timedelta
import pytest

from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.integration_boundary.integration_controller import IntegrationController
from src.integration_boundary.mock_social_provider import MockSocialProvider
from src.integration_boundary.models import ProviderEnvironment
from src.integration_boundary.exceptions import (
    AuthorizationScopeMismatchError,
    CredentialAccessViolationError,
    EnvironmentMismatchError,
    ExternalReplayError,
    CapabilityMappingError,
    IntegrationCircuitOpenError,
)


def test_t13_1_unauthorized_provider_invocation_rejection(tmp_path):
    """T13-1: Calling integration controller without valid authorization fails closed."""
    ctrl = IntegrationController(ledger_dir=str(tmp_path))
    provider = MockSocialProvider()
    ctrl.register_provider(provider)

    action = ExecutionAction(
        action_id="act_unauth",
        workflow_id="wf_1",
        task_id="t_1",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Draft"),
    )

    with pytest.raises(AuthorizationScopeMismatchError):
        ctrl.execute_external_tool(
            mission_id="m_sec",
            provider_id="mock_social",
            operation_name="create_draft",
            target_environment=ProviderEnvironment.SANDBOX,
            action=action,
            authorization_record=None,  # Missing authorization
        )


def test_t13_3_scope_confusion_capability_mismatch(tmp_path):
    """T13-3: Authorization for CREATE_DRAFT cannot be used for PUBLISH_CONTENT."""
    ctrl = IntegrationController(ledger_dir=str(tmp_path))
    provider = MockSocialProvider()
    ctrl.register_provider(provider)

    ctrl.credential_gateway.register_credential_handle(
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        reference_id="ref_social",
        secret_handle="SECRET_OPAQUE",
    )

    human_boundary = HumanAuthorizationBoundary()
    now = datetime.now(timezone.utc)
    auth = human_boundary.issue_human_authorization(
        request_id="req_scope_01",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_01",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    action_publish = ExecutionAction(
        action_id="act_pub",
        workflow_id="wf_1",
        task_id="t_1",
        capability=ExecutionCapability.PUBLISH_CONTENT,  # Mismatched capability
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={},
        planned_effect=PlannedEffect("PUBLISH_CONTENT", "SANDBOX_SOCIAL", "Publish"),
    )

    # Capability mapping mismatch throws CapabilityMappingError or AuthorizationScopeMismatchError
    with pytest.raises((CapabilityMappingError, AuthorizationScopeMismatchError)):
        ctrl.execute_external_tool(
            mission_id="m_sec",
            provider_id="mock_social",
            operation_name="publish_content",
            target_environment=ProviderEnvironment.SANDBOX,
            action=action_publish,
            authorization_record=auth,
        )


def test_t13_5_sandbox_to_live_mismatch_rejection(tmp_path):
    """T13-5: Test credentials cannot be executed on LIVE provider operation."""
    ctrl = IntegrationController(ledger_dir=str(tmp_path))
    provider = MockSocialProvider()
    ctrl.register_provider(provider)

    # Register SANDBOX credential
    ctrl.credential_gateway.register_credential_handle(
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        reference_id="ref_sandbox",
        secret_handle="SECRET_SANDBOX",
    )

    human_boundary = HumanAuthorizationBoundary()
    now = datetime.now(timezone.utc)
    auth = human_boundary.issue_human_authorization(
        request_id="req_env_01",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_01",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    action = ExecutionAction(
        action_id="act_env",
        workflow_id="wf_1",
        task_id="t_1",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Draft"),
    )

    # Requesting LIVE environment with SANDBOX credentials throws EnvironmentMismatchError or CredentialAccessViolationError
    with pytest.raises((EnvironmentMismatchError, CredentialAccessViolationError)):
        ctrl.execute_external_tool(
            mission_id="m_sec",
            provider_id="mock_social",
            operation_name="create_draft",
            target_environment=ProviderEnvironment.LIVE,
            action=action,
            authorization_record=auth,
        )


def test_t13_6_replay_mutation_rejection(tmp_path):
    """T13-6: Submitting duplicate mutation triggers ExternalReplayError."""
    ctrl = IntegrationController(ledger_dir=str(tmp_path))
    provider = MockSocialProvider()
    ctrl.register_provider(provider)

    ctrl.credential_gateway.register_credential_handle(
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        reference_id="ref_social",
        secret_handle="SECRET_OPAQUE",
    )

    human_boundary = HumanAuthorizationBoundary()
    now = datetime.now(timezone.utc)
    auth = human_boundary.issue_human_authorization(
        request_id="req_replay_01",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_01",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    action = ExecutionAction(
        action_id="act_replay",
        workflow_id="wf_1",
        task_id="t_1",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={"text": "Replay test"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Draft"),
    )

    # 1. First execution succeeds
    ctrl.execute_external_tool(
        mission_id="m_sec",
        provider_id="mock_social",
        operation_name="create_draft",
        target_environment=ProviderEnvironment.SANDBOX,
        action=action,
        authorization_record=auth,
        user_idempotency_key="key_same",
    )

    auth2 = human_boundary.issue_human_authorization(
        request_id="req_replay_02",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_02",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    # 2. Replayed execution with duplicate idempotency key throws ExternalReplayError
    with pytest.raises(ExternalReplayError):
        ctrl.execute_external_tool(
            mission_id="m_sec",
            provider_id="mock_social",
            operation_name="create_draft",
            target_environment=ProviderEnvironment.SANDBOX,
            action=action,
            authorization_record=auth2,
            user_idempotency_key="key_same",
        )

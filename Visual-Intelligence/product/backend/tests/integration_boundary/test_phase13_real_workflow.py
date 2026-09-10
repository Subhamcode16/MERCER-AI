"""
Mandatory Real-World Benchmark for Phase 13 Integration Boundary.

Executes end-to-end NOCAP campaign workflow through Phase 8-12 control planes down into Phase 13
controlled external tool execution. Verifies outcome reconciliation and ledger integrity.
"""

from datetime import datetime, timezone, timedelta
import pytest

from src.coordination.coordinator import MultiMissionCoordinator
from src.coordination.models import MissionPriority, ResourceRequest
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.integration_boundary.integration_controller import IntegrationController
from src.integration_boundary.mock_social_provider import MockSocialProvider
from src.integration_boundary.models import ProviderEnvironment, IntegrationOutcomeClass
from src.integration_boundary.exceptions import (
    AuthorizationScopeMismatchError,
    ExternalReplayError,
    CapabilityMappingError,
    EnvironmentMismatchError,
)


def test_nocap_end_to_end_phase13_benchmark(tmp_path):
    # 1. Initialize MultiMissionCoordinator & IntegrationController
    coord = MultiMissionCoordinator(ledger_dir=str(tmp_path))
    ctrl = IntegrationController(ledger_dir=str(tmp_path))

    provider = MockSocialProvider(provider_id="mock_social", environment=ProviderEnvironment.SANDBOX)
    ctrl.register_provider(provider)

    ctrl.credential_gateway.register_credential_handle(
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        reference_id="ref_nocap_social_sandbox",
        secret_handle="SECRET_OPAQUE_SANDBOX_KEY_NOCAP",
    )

    now = datetime.now(timezone.utc)

    # 2. Admit & Prepare Mission in Phase 11/12
    coord.admit_mission(
        mission_id="mission_nocap_autumn_drop",
        title="NOCAP September Autumn Drop",
        description="Launch NOCAP Autumn Social Drop",
        target_outcomes=["Complete Draft"],
        priority=MissionPriority.HIGH,
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap:autumn"},
    )
    coord.phase11_coordinator.prepare_mission("mission_nocap_autumn_drop")
    coord.phase11_coordinator.start_mission("mission_nocap_autumn_drop")

    # 3. Add AI Staff Task
    coord.phase11_coordinator.add_task(
        mission_id="mission_nocap_autumn_drop",
        task_id="task_copy",
        workflow_id="wf_nocap_01",
        assigned_role="CONTENT_SPECIALIST",
        description="Write Instagram Autumn Drop Copy",
    )

    # 4. Request Resource Allocation
    req = ResourceRequest("req_nocap_01", "mission_nocap_autumn_drop", "staff:designer", quantity=1)
    coord.request_resources_and_arbitrate([req])

    # 5. Issue Phase 10 Human Authorization
    scope = ResourceScope("campaign:nocap:autumn")
    auth = coord.phase11_coordinator.human_auth_boundary.issue_human_authorization(
        request_id="req_auth_autumn_drop",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=scope,
        human_operator_id="brand_director_human_01",
        decision_reference="DEC_APPROVE_AUTUMN_DROP",
        expires_at=(now + timedelta(hours=6)).isoformat(),
    )

    action = ExecutionAction(
        action_id="act_autumn_draft_01",
        workflow_id="wf_nocap_01",
        task_id="task_copy",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=scope,
        input_payload={"title": "NOCAP Autumn Teaser", "text": "Autumn collection drops Friday."},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Post draft"),
    )

    # 6. Execute Phase 13 Controlled External Operation
    outcome = ctrl.execute_external_tool(
        mission_id="mission_nocap_autumn_drop",
        provider_id="mock_social",
        operation_name="create_draft",
        target_environment=ProviderEnvironment.SANDBOX,
        action=action,
        authorization_record=auth,
        user_idempotency_key="key_nocap_drop_01",
    )

    # 7. Assertions on Success
    assert outcome.outcome_class == IntegrationOutcomeClass.SUCCESS
    assert outcome.reconciled is True
    assert outcome.provider_transaction_id.startswith("tx_mock_social_")

    # 8. Test Prohibited Operations (Fail-Closed Validations)
    # A. Unauthorized publish attempt -> BLOCKED
    action_pub = ExecutionAction(
        action_id="act_pub_fail",
        workflow_id="wf_nocap_01",
        task_id="task_copy",
        capability=ExecutionCapability.PUBLISH_CONTENT,
        resource_scope=scope,
        input_payload={},
        planned_effect=PlannedEffect("PUBLISH_CONTENT", "SANDBOX_SOCIAL", "Publish"),
    )
    with pytest.raises((CapabilityMappingError, AuthorizationScopeMismatchError)):
        ctrl.execute_external_tool(
            mission_id="mission_nocap_autumn_drop",
            provider_id="mock_social",
            operation_name="publish_content",
            target_environment=ProviderEnvironment.SANDBOX,
            action=action_pub,
            authorization_record=auth,
        )

    # B. Duplicate mutation attempt -> BLOCKED
    auth_dup = coord.phase11_coordinator.human_auth_boundary.issue_human_authorization(
        request_id="req_auth_autumn_dup",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=scope,
        human_operator_id="brand_director_human_01",
        decision_reference="DEC_APPROVE_AUTUMN_DROP_DUP",
        expires_at=(now + timedelta(hours=6)).isoformat(),
    )
    with pytest.raises(ExternalReplayError):
        ctrl.execute_external_tool(
            mission_id="mission_nocap_autumn_drop",
            provider_id="mock_social",
            operation_name="create_draft",
            target_environment=ProviderEnvironment.SANDBOX,
            action=action,
            authorization_record=auth_dup,
            user_idempotency_key="key_nocap_drop_01",
        )

    # C. Audit Integrity Pass
    assert ctrl.ledger.verify_ledger_integrity() is True

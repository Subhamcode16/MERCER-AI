"""
Phase 18 Studio Provider Runtime.

Subordinates all external provider interactions to Phase 13 IntegrationController controls,
enforcing exact capability checks, authorization verification, idempotency barriers,
rate limiting, circuit breakers, and hash-linked audit logging.
"""

from typing import Dict, Any, Optional
import os

from src.integration_boundary.integration_controller import IntegrationController
from src.integration_boundary.mock_social_provider import MockSocialProvider
from src.integration_boundary.models import (
    ProviderEnvironment,
    ExternalResponse,
)
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.studio_intelligence.exceptions import ProviderRuntimeError


class StudioProviderRuntime:
    """Delegates all external provider actions through Phase 13 IntegrationController."""

    def __init__(self, integration_controller: Optional[IntegrationController] = None):
        self.integration_controller = integration_controller or IntegrationController()
        if "mock_social" not in self.integration_controller._providers:
            self.integration_controller.register_provider(MockSocialProvider(provider_id="mock_social"))

        self.integration_controller.credential_gateway.register_credential_handle(
            provider_id="mock_social",
            environment=ProviderEnvironment.SANDBOX,
            reference_id="ref_social_sandbox",
            secret_handle="SECRET_OPAQUE_SANDBOX_KEY",
        )

    def execute_provider_action(
        self,
        client_id: str,
        action_name: str,
        capability: ExecutionCapability,
        auth_record: AuthorizationRecord,
        payload: Dict[str, Any],
        idempotency_key: str,
    ) -> Any:
        """Executes a provider action strictly subordinate to Phase 13 controls."""
        if not auth_record or getattr(auth_record, "revoked", False):
            raise ProviderRuntimeError("Provider operation rejected: Phase 10 Human Authorization missing or invalid.")

        action = ExecutionAction(
            action_id=f"act_{idempotency_key}",
            workflow_id=f"wf_{client_id}",
            task_id=f"task_{idempotency_key}",
            capability=capability,
            resource_scope=auth_record.resource_scope,
            input_payload=payload,
            planned_effect=PlannedEffect(action_name, "SANDBOX_SOCIAL", f"Execute {action_name}"),
        )

        # Route through Phase 13 10-step validation pipeline
        try:
            return self.integration_controller.execute_external_tool(
                mission_id=f"mission_{client_id}",
                provider_id="mock_social",
                operation_name=action_name,
                target_environment=ProviderEnvironment.SANDBOX,
                action=action,
                authorization_record=auth_record,
                user_idempotency_key=idempotency_key,
            )
        except Exception as exc:
            raise ProviderRuntimeError(f"Phase 13 Provider Execution failed: {str(exc)}") from exc

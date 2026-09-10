"""
Phase 13 Integration Controller.

Primary entry point for controlled external tool & platform execution.
Orchestrates the 10-step validation pipeline: capability mapping, authorization bridge,
environment guard, rate limits, circuit breaker, idempotency reservation, credential gateway,
provider adapter invocation, outcome reconciliation, and hash-linked audit logging.
"""

from typing import Dict, Any, Optional
import uuid
import os

from src.execution_control.action_models import ExecutionAction
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.models import (
    ProviderEnvironment,
    ExternalRequest,
    ExternalResponse,
    IntegrationOutcome,
    IntegrationOutcomeClass,
    CredentialReference,
)
from src.integration_boundary.provider import BaseProviderAdapter
from src.integration_boundary.capability_mapping import CapabilityMappingRegistry
from src.integration_boundary.credential_gateway import CredentialGateway
from src.integration_boundary.environment_guard import EnvironmentGuard
from src.integration_boundary.authorization_bridge import AuthorizationBridge
from src.integration_boundary.idempotency import ExternalIdempotencyBarrier
from src.integration_boundary.rate_limiter import ProviderRateLimiter
from src.integration_boundary.circuit_breaker import IntegrationCircuitBreaker
from src.integration_boundary.integration_ledger import IntegrationLedger
from src.integration_boundary.reconciliation import ReconciliationEngine
from src.integration_boundary.exceptions import (
    ProviderNotRegisteredError,
    CapabilityMappingError,
    AuthorizationScopeMismatchError,
    ExternalTimeoutError,
    ExternalOperationRejectedError,
    IntegrationBoundaryError,
)


class IntegrationController:
    """Primary control-plane orchestrator for external tool and platform integrations."""

    def __init__(self, ledger: Optional[IntegrationLedger] = None, ledger_dir: Optional[str] = None):
        self.capability_mapping = CapabilityMappingRegistry()
        self.credential_gateway = CredentialGateway()
        self.environment_guard = EnvironmentGuard()
        self.authorization_bridge = AuthorizationBridge()
        self.idempotency_barrier = ExternalIdempotencyBarrier()
        self.rate_limiter = ProviderRateLimiter()
        self.circuit_breaker = IntegrationCircuitBreaker()
        self.reconciliation_engine = ReconciliationEngine()

        if ledger:
            self.ledger = ledger
        elif ledger_dir:
            p13_ledger_dir = os.path.join(ledger_dir, "phase13_ledger")
            self.ledger = IntegrationLedger(base_dir=p13_ledger_dir)
        else:
            self.ledger = IntegrationLedger()

        # provider_id -> BaseProviderAdapter
        self._providers: Dict[str, BaseProviderAdapter] = {}

    def register_provider(self, provider: BaseProviderAdapter) -> None:
        """Registers a provider adapter and records its supported operation mappings."""
        self._providers[provider.provider_id] = provider
        for op in provider.supported_operations():
            self.capability_mapping.register_mapping(
                provider_id=provider.provider_id,
                operation_name=op.operation_name,
                capability=op.mapped_capability,
            )

    def execute_external_tool(
        self,
        mission_id: str,
        provider_id: str,
        operation_name: str,
        target_environment: ProviderEnvironment,
        action: ExecutionAction,
        authorization_record: AuthorizationRecord,
        user_idempotency_key: str = "default_key",
        explicit_live_allowed: bool = False
    ) -> IntegrationOutcome:
        """
        Orchestrates controlled external tool execution through the 10-step validation pipeline.
        Fails closed on any security boundary or validation error.
        """
        request_id = f"req_ext_{uuid.uuid4().hex[:8]}"

        # 1. Provider registration check
        provider = self._providers.get(provider_id)
        if not provider:
            raise ProviderNotRegisteredError(f"External provider '{provider_id}' is not registered.")

        # 2. Capability mapping check (INV-13-002)
        mapped_cap = self.capability_mapping.resolve_capability(provider_id, operation_name)
        if mapped_cap != action.capability:
            raise CapabilityMappingError(
                f"Capability Mismatch: Operation '{operation_name}' maps to '{mapped_cap.value}', but action specifies '{action.capability.value}'."
            )

        # 3. Authorization bridge validation (INV-13-001 & INV-13-006)
        self.authorization_bridge.validate_authorization_for_external_call(
            authorization_record=authorization_record,
            action=action,
            mission_id=mission_id,
        )
        auth_verified = True

        # 4. Environment boundary validation (INV-13-005)
        cred_ref = self.credential_gateway.get_credential_reference(
            provider_id=provider_id,
            environment=target_environment,
            authorization_verified=auth_verified,
        )
        self.environment_guard.validate_environment_boundary(
            target_environment=target_environment,
            credential_reference=cred_ref,
            explicit_live_allowed=explicit_live_allowed,
        )

        # 5. Rate limit check
        cap_name = action.capability.value if hasattr(action.capability, "value") else str(action.capability)
        self.rate_limiter.check_and_acquire(provider_id, cap_name)

        # 6. Circuit breaker check (INV-13-009)
        self.circuit_breaker.check_state(provider_id)

        # 7. Idempotency reservation (INV-13-008)
        idempotency_key = self.idempotency_barrier.compute_idempotency_key(
            mission_id=mission_id,
            authorization_id=authorization_record.authorization_id,
            action_hash=action.input_commitment_hash,
            operation_name=operation_name,
            user_idempotency_key=user_idempotency_key,
        )
        self.idempotency_barrier.reserve_key(idempotency_key)

        # 8. Retrieve opaque secret (INV-13-003 & INV-13-004)
        opaque_secret = self.credential_gateway.get_opaque_secret(cred_ref, authorization_verified=auth_verified)

        # Build external request contract
        ext_request = ExternalRequest(
            request_id=request_id,
            operation_name=operation_name,
            provider_id=provider_id,
            environment=target_environment,
            capability=action.capability,
            resource_scope_string=action.resource_scope.scope_string,
            payload=action.input_payload,
            idempotency_key=idempotency_key,
            action_hash=action.input_commitment_hash,
            mission_id=mission_id,
            authorization_id=authorization_record.authorization_id,
        )

        # 9. Provider invocation & exception handling
        try:
            response = provider.execute(
                request=ext_request,
                credential_reference=cred_ref,
                opaque_secret=opaque_secret,
            )
            self.circuit_breaker.record_success(provider_id)
        except (ExternalTimeoutError, ExternalOperationRejectedError) as e:
            self.circuit_breaker.record_failure(provider_id)
            response = ExternalResponse(
                request_id=request_id,
                provider_transaction_id=f"tx_failed_{uuid.uuid4().hex[:6]}",
                outcome_class=IntegrationOutcomeClass.FAILED,
                output_data={},
                error_message=str(e),
            )

        # 10. Reconcile & Audit Logging (INV-13-012)
        outcome = self.reconciliation_engine.reconcile_execution(ext_request, response)

        self.ledger.record_integration_event(
            event_type="EXTERNAL_TOOL_EXECUTED",
            request_id=request_id,
            mission_id=mission_id,
            provider_id=provider_id,
            environment=target_environment.value,
            capability=cap_name,
            resource_scope=action.resource_scope.scope_string,
            idempotency_key=idempotency_key,
            outcome_class=outcome.outcome_class.value,
            transaction_id=outcome.provider_transaction_id,
        )

        return outcome

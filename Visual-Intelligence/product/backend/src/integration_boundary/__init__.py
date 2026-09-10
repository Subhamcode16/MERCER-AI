"""
Phase 13 External Tool & Platform Integration Boundary Package.

Provides controlled external-world transport, capability mapping, opaque credential handles,
environment separation, rate limiting, circuit breaker, idempotency barriers, outcome reconciliation,
and append-only hash-linked audit logging.
"""

from .exceptions import (
    IntegrationBoundaryError,
    ProviderNotRegisteredError,
    CapabilityMappingError,
    AuthorizationScopeMismatchError,
    CredentialAccessViolationError,
    EnvironmentMismatchError,
    ProviderResponseValidationError,
    ExternalReplayError,
    ExternalRateLimitError,
    ExternalOperationRejectedError,
    ExternalTimeoutError,
    IntegrationCircuitOpenError,
    ReconciliationTamperError,
)

from .models import (
    ProviderEnvironment,
    IntegrationOutcomeClass,
    CredentialReference,
    ExternalOperation,
    ExternalRequest,
    ExternalResponse,
    IntegrationOutcome,
)

from .capability_mapping import CapabilityMappingRegistry
from .credential_gateway import CredentialGateway
from .environment_guard import EnvironmentGuard
from .authorization_bridge import AuthorizationBridge
from .idempotency import ExternalIdempotencyBarrier
from .rate_limiter import ProviderRateLimiter
from .circuit_breaker import IntegrationCircuitBreaker, CircuitState
from .provider import BaseProviderAdapter
from .mock_social_provider import MockSocialProvider
from .integration_ledger import IntegrationLedger, IntegrationLedgerEntry
from .reconciliation import ReconciliationEngine
from .integration_controller import IntegrationController

__all__ = [
    "IntegrationBoundaryError",
    "ProviderNotRegisteredError",
    "CapabilityMappingError",
    "AuthorizationScopeMismatchError",
    "CredentialAccessViolationError",
    "EnvironmentMismatchError",
    "ProviderResponseValidationError",
    "ExternalReplayError",
    "ExternalRateLimitError",
    "ExternalOperationRejectedError",
    "ExternalTimeoutError",
    "IntegrationCircuitOpenError",
    "ReconciliationTamperError",
    "ProviderEnvironment",
    "IntegrationOutcomeClass",
    "CredentialReference",
    "ExternalOperation",
    "ExternalRequest",
    "ExternalResponse",
    "IntegrationOutcome",
    "CapabilityMappingRegistry",
    "CredentialGateway",
    "EnvironmentGuard",
    "AuthorizationBridge",
    "ExternalIdempotencyBarrier",
    "ProviderRateLimiter",
    "IntegrationCircuitBreaker",
    "CircuitState",
    "BaseProviderAdapter",
    "MockSocialProvider",
    "IntegrationLedger",
    "IntegrationLedgerEntry",
    "ReconciliationEngine",
    "IntegrationController",
]

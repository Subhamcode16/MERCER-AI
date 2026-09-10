"""
Phase 13 Integration Boundary Exceptions.

Defines fail-closed domain exceptions for external tool & platform integration boundaries.
"""


class IntegrationBoundaryError(Exception):
    """Base exception for all Phase 13 integration boundary errors."""
    pass


class ProviderNotRegisteredError(IntegrationBoundaryError):
    """Raised when an requested provider ID is not registered in the integration boundary."""
    pass


class CapabilityMappingError(IntegrationBoundaryError):
    """Raised when an external operation cannot be mapped to an explicit Phase 10 capability."""
    pass


class AuthorizationScopeMismatchError(IntegrationBoundaryError, PermissionError):
    """Raised when an authorization record scope, capability, or mission does not match the external request."""
    pass


class CredentialAccessViolationError(IntegrationBoundaryError, PermissionError):
    """Raised when credential access is attempted without prior valid human authorization."""
    pass


class EnvironmentMismatchError(IntegrationBoundaryError):
    """Raised when sandbox/live credential or operation environment parameters mismatch."""
    pass


class ProviderResponseValidationError(IntegrationBoundaryError):
    """Raised when a provider response fails structural validation or reconciliation checks."""
    pass


class ExternalReplayError(IntegrationBoundaryError):
    """Raised when a duplicate external mutation is submitted across the idempotency barrier."""
    pass


class ExternalRateLimitError(IntegrationBoundaryError):
    """Raised when provider or capability rate limits are exceeded."""
    pass


class ExternalOperationRejectedError(IntegrationBoundaryError):
    """Raised when an external provider rejects an operation payload."""
    pass


class ExternalTimeoutError(IntegrationBoundaryError):
    """Raised when an external provider call times out."""
    pass


class IntegrationCircuitOpenError(IntegrationBoundaryError):
    """Raised when an external execution is attempted while the provider circuit breaker is OPEN."""
    pass


class ReconciliationTamperError(IntegrationBoundaryError):
    """Raised when external outcome reconciliation detects response tampering or discrepancy."""
    pass

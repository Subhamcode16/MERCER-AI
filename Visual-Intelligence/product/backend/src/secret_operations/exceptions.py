"""
Phase 23 Secret & Credential Operations Exceptions.
"""

class SecretOperationError(Exception):
    """Base exception for secret operations."""
    pass

class SecretNotFoundError(SecretOperationError):
    """Raised when requested secret is missing from provider."""
    pass

class SecretRotationError(SecretOperationError):
    """Raised when in-flight credential rotation fails."""
    pass

class LeaseExpiredError(SecretOperationError):
    """Raised when a time-bounded credential lease has expired."""
    pass

class UnauthorizedScopeError(SecretOperationError):
    """Raised when credential is requested for an unpermitted domain scope."""
    pass

class SecretLeakageDetected(SecretOperationError):
    """Raised when unredacted credential material is detected in telemetry or output."""
    pass

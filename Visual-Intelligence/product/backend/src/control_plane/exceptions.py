"""
Phase 25 Control Plane Exceptions Hierarchy.
"""

class ControlPlaneError(Exception):
    """Base exception for all control plane operations."""
    pass

class TenantContextMissingError(ControlPlaneError):
    """Raised when an operator request lacks valid tenant or client context."""
    pass

class UnauthorizedOperatorActionError(ControlPlaneError):
    """Raised when an operator lacks the specific capability for a requested action."""
    pass

class StaleActionConflictError(ControlPlaneError):
    """Raised when an action is attempted against a stale entity version (409 Conflict)."""
    pass

class DTOSerializationError(ControlPlaneError):
    """Raised when serialization detects prohibited fields (secrets, credentials, CoT)."""
    pass

class OperatorSessionExpiredError(ControlPlaneError):
    """Raised when operator authentication token or session has expired."""
    pass

class TenantAccessDeniedError(ControlPlaneError):
    """Raised when an operator attempts cross-tenant data access."""
    pass

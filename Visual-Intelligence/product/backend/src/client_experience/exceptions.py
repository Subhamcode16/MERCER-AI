"""
Phase 16 Client Experience Exception Hierarchy.
All exceptions are fail-closed and non-swallowable security/interaction errors.
"""

class ClientExperienceError(Exception):
    """Base exception for all Phase 16 Client Experience errors."""
    pass

class ClientAccessDeniedError(ClientExperienceError):
    """Raised when access to a client workspace, campaign, or deliverable is denied."""
    pass

class InvalidRoleCapabilityError(ClientExperienceError):
    """Raised when a human role attempts an action not permitted by its explicit capability allowlist."""
    pass

class ContextGuardViolationError(ClientExperienceError):
    """Raised when server-side client context validation fails closed."""
    pass

class UIAuthorizationForgeryError(ClientExperienceError):
    """Raised when UI or API layers attempt to manufacture authorization records directly."""
    pass

class FeedbackPolicyMutationError(ClientExperienceError):
    """Raised when client feedback attempts to mutate security policy or elevate capabilities."""
    pass

class ReasoningLeakageError(ClientExperienceError):
    """Raised when an operation would expose protected internal chain-of-thought or credentials."""
    pass

class StaleApprovalError(ClientExperienceError):
    """Raised when an action is attempted on an expired or invalid approval item."""
    pass

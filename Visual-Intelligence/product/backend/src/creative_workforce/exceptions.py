"""
Phase 14 Creative Workforce Exception Hierarchy
------------------------------------------------
Fail-closed exceptions for ILYREN Creative Workforce operations.
Prohibits privilege escalation, authorization forgery, cross-client context leakage,
and unauthorized security policy mutations.
"""

class CreativeWorkforceError(Exception):
    """Base exception for all Phase 14 Creative Workforce errors."""
    pass

class StaffNotFoundError(CreativeWorkforceError):
    """Raised when a requested staff member or role identity does not exist."""
    pass

class ContextScopeViolationError(CreativeWorkforceError):
    """Raised when context scoping rules or identity bindings are violated."""
    pass

class CrossClientLeakageError(CreativeWorkforceError):
    """Raised when a staff member attempts to access context or artifacts from another client."""
    pass

class RevisionLimitExceededError(CreativeWorkforceError):
    """Raised when an artifact exceeds the maximum permitted revision ceiling (MAX_REVISIONS = 3)."""
    pass

class SelfAuthorizationAttemptError(CreativeWorkforceError):
    """Raised when a staff member or reviewer attempts to authorize its own execution or issue tokens."""
    pass

class ReviewerBypassError(CreativeWorkforceError):
    """Raised when a producing staff attempts to bypass independent review."""
    pass

class StrategyDegradationError(CreativeWorkforceError):
    """Raised when a candidate workflow strategy fails benchmark evaluation against baseline."""
    pass

class UntrustedObservationInjectionError(CreativeWorkforceError):
    """Raised when an external observation contains prompt injection or security policy mutation attempts."""
    pass

class InvalidWorkforceRequestError(CreativeWorkforceError):
    """Raised when a workforce request or objective is malformed or invalid."""
    pass

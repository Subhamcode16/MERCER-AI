"""
Phase 15 Studio Operations Exception Hierarchy.
All exceptions are fail-closed and non-swallowable security/operational errors.
"""

class StudioOperationError(Exception):
    """Base exception for all Phase 15 Studio Operations errors."""
    pass

class ClientContextViolation(StudioOperationError):
    """Raised when client context is missing, invalid, or violates cross-client isolation."""
    pass

class CampaignStateViolation(StudioOperationError):
    """Raised when an invalid state transition is attempted on a campaign."""
    pass

class DeliverableStateViolation(StudioOperationError):
    """Raised when an invalid lifecycle state transition is attempted on a deliverable."""
    pass

class ApprovalRequiredError(StudioOperationError):
    """Raised when an operation requires explicit human authorization."""
    pass

class ApprovalExpiredError(StudioOperationError):
    """Raised when a human approval request has expired and can no longer be acted upon."""
    pass

class OperationalPolicyViolation(StudioOperationError):
    """Raised when an action violates a client's operational policy."""
    pass

class ContinuityViolation(StudioOperationError):
    """Raised when operational continuity is interrupted, inconsistent, or invalid."""
    pass

class ScheduleConflictError(StudioOperationError):
    """Raised when a operational schedule conflict or invalid window is encountered."""
    pass

class ProductionReadinessError(StudioOperationError):
    """Raised when production readiness checks fail."""
    pass

class ExternalOutcomeValidationError(StudioOperationError):
    """Raised when external platform observations fail validation or contain untrusted structures."""
    pass

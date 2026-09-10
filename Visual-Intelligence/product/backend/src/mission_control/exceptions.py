"""
Phase 11 Mission Control Exception Hierarchy.

Establishes domain-specific, non-swallowable exceptions for operational autonomy,
mission orchestration, state transition failures, boundary violations, and checkpoint tampering.
"""


class MissionControlError(Exception):
    """Base exception for all Phase 11 mission control errors."""
    pass


class InvalidMissionStateError(MissionControlError):
    """Raised when an invalid or forbidden mission state transition is attempted."""
    pass


class InvalidMissionGraphError(MissionControlError):
    """Raised when a mission DAG is cyclic, exceeds depth, or has invalid task dependencies."""
    pass


class MissionPolicyViolationError(MissionControlError):
    """Raised when a mission violates autonomy policies, constraints, or security boundaries."""
    pass


class MissionBudgetExceededError(MissionControlError):
    """Raised when a task or mission exceeds token, execution, or runtime budgets."""
    pass


class AuthorizationRequiredError(MissionControlError):
    """Raised when an operation requires external human authorization token."""
    pass


class CheckpointError(MissionControlError):
    """Base exception for mission checkpoint failures."""
    pass


class CheckpointTamperedError(CheckpointError):
    """Raised when a checkpoint's SHA-256 digest verification fails."""
    pass


class ResumptionFailedError(MissionControlError):
    """Raised when 8-point resumption revalidation fails."""
    pass


class RetryExhaustedError(MissionControlError):
    """Raised when a task fails and exceeds maximum retry attempts."""
    pass


class MissionCancelledError(MissionControlError):
    """Raised when attempting execution or modification on a cancelled mission."""
    pass


class SecurityBoundaryViolation(MissionControlError, PermissionError):
    """Raised when autonomous execution attempts privilege elevation or policy mutation."""
    pass

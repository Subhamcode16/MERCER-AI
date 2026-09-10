"""
Phase 12 Coordination Exception Hierarchy.

Defines domain-specific exceptions for multi-mission coordination, shared resource allocations,
leases, deadlocks, capacity exhaustion, conflict detection, and security boundaries.
"""


class CoordinationException(Exception):
    """Base exception for all Phase 12 coordination errors."""
    pass


class MissionAdmissionDenied(CoordinationException):
    """Raised when a mission is denied admission into the coordination registry."""
    pass


class ResourceUnavailable(CoordinationException):
    """Raised when a requested logical resource is currently unavailable or depleted."""
    pass


class ResourceConflict(CoordinationException):
    """Raised when mutually incompatible resource allocations or side-effects are detected."""
    pass


class ReservationExpired(CoordinationException):
    """Raised when attempting to use or commit an expired resource lease."""
    pass


class CoordinationDeadlock(CoordinationException):
    """Raised when a cyclic resource dependency deadlock is detected across missions."""
    pass


class StarvationDetected(CoordinationException):
    """Raised when a low-priority mission exceeds maximum waiting duration threshold."""
    pass


class CoordinationBudgetExceeded(CoordinationException):
    """Raised when global or multi-mission resource budgets are exhausted."""
    pass


class CrossMissionAuthorizationError(CoordinationException, PermissionError):
    """Raised when an authorization token from Mission A is attempted to be used by Mission B."""
    pass


class CoordinationPolicyViolation(CoordinationException):
    """Raised when a coordination decision violates security boundaries or policy invariants."""
    pass


class CoordinationReplayError(CoordinationException):
    """Raised when a replayed lease, nonce, or coordination record is detected."""
    pass


class CheckpointTamperedError(CoordinationException):
    """Raised when a lease, audit ledger checkpoint, or hash signature is tampered with."""
    pass


class LeaseValidationError(CoordinationException):
    """Raised when a resource lease fails validation due to expiration, revocation, or invalid signature."""
    pass


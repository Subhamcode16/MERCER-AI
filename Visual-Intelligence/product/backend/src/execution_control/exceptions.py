"""
Phase 10 — Controlled Operational Execution & Authorization Exceptions

Defines fail-closed exceptions for capability violations, unauthorized self-execution,
expired or revoked tokens, replay attempts, dry-run side-effect escapes, and resource boundary breaches.
"""


class ExecutionControlException(Exception):
    """Base exception for all Phase 10 execution control failures."""

    pass


class SelfAuthorizationAttemptError(ExecutionControlException, PermissionError):
    """Raised when an AI staff member, reviewer, or orchestrator attempts to authorize its own execution."""

    pass


class CapabilityViolationError(ExecutionControlException, PermissionError):
    """Raised when an action requests an un-allowed, non-existent, or forbidden capability."""

    pass


class ResourceScopeViolationError(ExecutionControlException, PermissionError):
    """Raised when an authorization token is used outside its explicit resource scope."""

    pass


class AuthorizationExpiredError(ExecutionControlException, PermissionError):
    """Raised when an authorization record has exceeded its expiration timestamp."""

    pass


class AuthorizationRevokedError(ExecutionControlException, PermissionError):
    """Raised when an authorization record has been revoked."""

    pass


class ReplayExecutionError(ExecutionControlException, ValueError):
    """Raised when an action or authorization token is re-submitted (replay attack defense)."""

    pass


class DryRunSideEffectError(ExecutionControlException, RuntimeError):
    """Raised if dry-run simulation attempts to invoke real side-effect adapters."""

    pass


class AdapterNotFoundError(ExecutionControlException, KeyError):
    """Raised when no integration adapter is registered for a capability."""

    pass


class PartialExecutionError(ExecutionControlException, RuntimeError):
    """Raised when a multi-action execution halts mid-sequence due to an adapter failure."""

    pass

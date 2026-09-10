"""
Exceptions for the Visual Intelligence Security Substrate.
"""

class SecuritySubstrateException(Exception):
    """Base exception for all Security Substrate errors."""
    pass


class FailClosedException(SecuritySubstrateException):
    """Triggered when an unexpected failure forces a fail-closed response."""
    pass


class ReplayAttackException(SecuritySubstrateException):
    """Triggered when a replayed nonce or evidence payload is detected."""
    pass


class StaleTimestampException(SecuritySubstrateException):
    """Triggered when an evidence timestamp exceeds the max freshness window."""
    pass


class MalformedEvidenceException(SecuritySubstrateException):
    """Triggered when an evidence payload is structurally invalid or un-signed."""
    pass


class InvalidStateTransitionException(SecuritySubstrateException):
    """Triggered when a state transition violates the canonical matrix."""
    pass


class ExecutionGateLockedException(SecuritySubstrateException):
    """Triggered when an execution call is rejected by the ExecutionGate."""
    pass


class InvalidDecisionException(SecuritySubstrateException):
    """Triggered when a decision classification, field, or structure is invalid or uses banned terms."""
    pass


class AttestationTamperedException(SecuritySubstrateException):
    """Triggered when an attestation record fails cryptographic commitment verification."""
    pass


class DecisionReplayException(SecuritySubstrateException):
    """Triggered when a decision artifact or nonce is replayed."""
    pass


class AuditIntegrityException(SecuritySubstrateException):
    """Triggered when an audit record or chain fails cryptographic hash integrity verification."""
    pass


class AuditReplayException(SecuritySubstrateException):
    """Triggered when a duplicate audit record ID or attestation commitment is replayed."""
    pass


class AuditSchemaException(SecuritySubstrateException):
    """Triggered when an audit record payload or metadata violates schema rules."""
    pass


class AuditSequenceException(SecuritySubstrateException):
    """Triggered when an audit record sequence gap or discontinuity is detected."""
    pass


class ReconciliationSchemaException(SecuritySubstrateException):
    """Triggered when a reconciliation model payload violates schema validation."""
    pass


class ReconciliationConflictException(SecuritySubstrateException):
    """Triggered when unresolvable classification conflicts are encountered during reconciliation."""
    pass


class ReconciliationIntegrityException(SecuritySubstrateException):
    """Triggered when a reconciliation snapshot commitment fails verification."""
    pass


class ReconciliationReferenceException(SecuritySubstrateException):
    """Triggered when broken cross-record references or identity mismatches are detected."""
    pass




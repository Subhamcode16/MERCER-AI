"""
Visual Intelligence Security Substrate — Epistemic Engine, Execution Gate, Verification Harness, & Recovery Parser.
Ratified Baselines: ARCH-IMPLEMENTATION-BOUNDARY-001 (Phase 1, Phase 2, & Phase 3).
"""

from .epistemic_state import (
    EpistemicState,
    validate_transition,
    PERMITTED_TRANSITIONS,
)
from .assurance_loop import (
    EvidencePayload,
    ConsumedNonceCache,
    EpistemicStateStore,
    AssuranceLoopController,
)
from .execution_gate import (
    ExecutionGate,
    GateResponse,
)
from .exceptions import (
    SecuritySubstrateException,
    FailClosedException,
    ReplayAttackException,
    StaleTimestampException,
    MalformedEvidenceException,
    InvalidStateTransitionException,
    ExecutionGateLockedException,
    InvalidDecisionException,
    AttestationTamperedException,
    DecisionReplayException,
    AuditIntegrityException,
    AuditReplayException,
    AuditSchemaException,
    AuditSequenceException,
    ReconciliationSchemaException,
    ReconciliationConflictException,
    ReconciliationIntegrityException,
    ReconciliationReferenceException,
)
from .crypto_utils import (
    compute_salted_commitment,
    generate_salt,
    generate_nonce,
    sign_evidence_payload,
    verify_evidence_signature,
)
from .verification_harness import (
    VerificationClaim,
    EvaluationResult,
    OptionHVerificationHarness,
    DEFAULT_TEST_DOMAIN_KEY,
)
from .recovery_parser import (
    RecoveryPayload,
    RecoveryAuthorizationResult,
    RecoveryEpochStore,
    CapabilityPayloadParser,
    RecoveryManager,
    DEFAULT_SYSTEM_ID,
    DEFAULT_OPERATION_ID,
    DEFAULT_AUTHORIZATION_SCOPE,
)
from .evidence_models import (
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    NormalizedEvidenceRecord,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from .evidence_policy import EvidencePolicy
from .evidence_orchestrator import EvidenceOrchestrator
from .research_adapter import ResearchAdapter

from .decision_models import (
    DecisionClassification,
    DecisionStatus,
    DecisionReasonCode,
    DecisionEvidenceReference,
    DecisionContext,
    SecurityDecision,
    AttestationRecord,
)
from .decision_policy import DecisionPolicy
from .attestation import (
    canonicalize_decision,
    compute_decision_commitment,
    create_attestation,
    verify_attestation,
)
from .decision_replay import DecisionReplayCache
from .decision_engine import SecurityDecisionEngine

from .audit_models import (
    AuditRecord,
    AuditRecordType,
    AuditRecordStatus,
    AuditIntegrityResult,
    AuditQuery,
    AuditSequenceMetadata,
)
from .audit_integrity import (
    canonicalize_audit_payload,
    compute_record_hash,
    create_genesis_record,
    verify_record_integrity,
    verify_chain_integrity,
)
from .audit_store import AuditStore
from .audit_boundary import SecurityAuditBoundary

from .reconciliation_models import (
    ReconciliationStatus,
    ReconciliationReasonCode,
    ReconciliationSource,
    ReconciliationFinding,
    ReconciliationSnapshot,
    ReconciliationResult,
)
from .reconciliation_policy import ReconciliationPolicy
from .reconciliation_integrity import (
    serialize_reconciliation_snapshot,
    compute_snapshot_digest,
    compute_result_commitment,
    verify_snapshot_digest,
    verify_result_commitment,
)
from .security_reconciler import SecurityReconciler

__all__ = [
    "EpistemicState",
    "validate_transition",
    "PERMITTED_TRANSITIONS",
    "EvidencePayload",
    "ConsumedNonceCache",
    "EpistemicStateStore",
    "AssuranceLoopController",
    "ExecutionGate",
    "GateResponse",
    "SecuritySubstrateException",
    "FailClosedException",
    "ReplayAttackException",
    "StaleTimestampException",
    "MalformedEvidenceException",
    "InvalidStateTransitionException",
    "ExecutionGateLockedException",
    "InvalidDecisionException",
    "AttestationTamperedException",
    "DecisionReplayException",
    "AuditIntegrityException",
    "AuditReplayException",
    "AuditSchemaException",
    "AuditSequenceException",
    "ReconciliationSchemaException",
    "ReconciliationConflictException",
    "ReconciliationIntegrityException",
    "ReconciliationReferenceException",
    "compute_salted_commitment",
    "generate_salt",
    "generate_nonce",
    "sign_evidence_payload",
    "verify_evidence_signature",
    "VerificationClaim",
    "EvaluationResult",
    "OptionHVerificationHarness",
    "DEFAULT_TEST_DOMAIN_KEY",
    "RecoveryPayload",
    "RecoveryAuthorizationResult",
    "RecoveryEpochStore",
    "CapabilityPayloadParser",
    "RecoveryManager",
    "DEFAULT_SYSTEM_ID",
    "DEFAULT_OPERATION_ID",
    "DEFAULT_AUTHORIZATION_SCOPE",
    "EvidenceClassification",
    "EvidenceProvenance",
    "EvidenceStatus",
    "NormalizedEvidenceRecord",
    "DEFAULT_TRUST_MARKER_RESEARCH",
    "EvidencePolicy",
    "EvidenceOrchestrator",
    "ResearchAdapter",
    "DecisionClassification",
    "DecisionStatus",
    "DecisionReasonCode",
    "DecisionEvidenceReference",
    "DecisionContext",
    "SecurityDecision",
    "AttestationRecord",
    "DecisionPolicy",
    "canonicalize_decision",
    "compute_decision_commitment",
    "create_attestation",
    "verify_attestation",
    "DecisionReplayCache",
    "SecurityDecisionEngine",
    "AuditRecord",
    "AuditRecordType",
    "AuditRecordStatus",
    "AuditIntegrityResult",
    "AuditQuery",
    "AuditSequenceMetadata",
    "canonicalize_audit_payload",
    "compute_record_hash",
    "create_genesis_record",
    "verify_record_integrity",
    "verify_chain_integrity",
    "AuditStore",
    "SecurityAuditBoundary",
    "ReconciliationStatus",
    "ReconciliationReasonCode",
    "ReconciliationSource",
    "ReconciliationFinding",
    "ReconciliationSnapshot",
    "ReconciliationResult",
    "ReconciliationPolicy",
    "serialize_reconciliation_snapshot",
    "compute_snapshot_digest",
    "compute_result_commitment",
    "verify_snapshot_digest",
    "verify_result_commitment",
    "SecurityReconciler",
]




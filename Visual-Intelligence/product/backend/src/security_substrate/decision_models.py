"""
IF-DECISION-001 Phase 6 Security Decision & Attestation Models.
Enforces strict schema validation, classification boundaries, and non-authorizing status tracking.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from .exceptions import InvalidDecisionException


class DecisionClassification(str, Enum):
    """
    Explicit classification categories for security evaluation outcomes.
    The classification 'AUTHORIZED' is strictly prohibited.
    """
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    EVIDENCE_CONFLICT = "EVIDENCE_CONFLICT"
    EVIDENCE_EXPIRED = "EVIDENCE_EXPIRED"
    EVIDENCE_QUARANTINED = "EVIDENCE_QUARANTINED"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    EVALUATION_PASS = "EVALUATION_PASS"
    EVALUATION_FAIL = "EVALUATION_FAIL"


class DecisionStatus(str, Enum):
    """
    Lifecycle status tracking for evaluation decisions.
    Explicitly avoids execution/authorization terms.
    """
    EVALUATED = "EVALUATED"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    EXPIRED = "EXPIRED"


class DecisionReasonCode(str, Enum):
    """
    Deterministic reason codes for evaluation results.
    """
    EVIDENCE_SUFFICIENT_AND_VALID = "EVIDENCE_SUFFICIENT_AND_VALID"
    MISSING_REQUIRED_EVIDENCE = "MISSING_REQUIRED_EVIDENCE"
    EVIDENCE_CONTRADICTION_DETECTED = "EVIDENCE_CONTRADICTION_DETECTED"
    EVIDENCE_EXPIRED_OR_STALE = "EVIDENCE_EXPIRED_OR_STALE"
    EVIDENCE_QUARANTINED_OR_REJECTED = "EVIDENCE_QUARANTINED_OR_REJECTED"
    PROVENANCE_POLICY_MISMATCH = "PROVENANCE_POLICY_MISMATCH"
    RESEARCH_EVIDENCE_NOT_AUTHORITATIVE = "RESEARCH_EVIDENCE_NOT_AUTHORITATIVE"
    POLICY_VERSION_MISMATCH = "POLICY_VERSION_MISMATCH"
    MALFORMED_INPUT_DETECTED = "MALFORMED_INPUT_DETECTED"
    EVALUATION_FAILED_GENERAL = "EVALUATION_FAILED_GENERAL"


BANNED_CLASSIFICATION_TERMS = {"AUTHORIZED", "AUTHORIZATION", "PERMITTED", "UNLOCKED", "EXECUTE"}


@dataclass
class DecisionEvidenceReference:
    """
    Lightweight reference binding evidence records to a decision artifact.
    Contains no raw asset bytes, secrets, or keys.
    """
    evidence_id: str
    classification: str
    payload_commitment: str
    trust_marker: str

    def __post_init__(self):
        # Reject boolean type confusion
        for name, val in [
            ("evidence_id", self.evidence_id),
            ("classification", self.classification),
            ("payload_commitment", self.payload_commitment),
            ("trust_marker", self.trust_marker),
        ]:
            if isinstance(val, bool):
                raise InvalidDecisionException(f"Boolean type confusion not permitted for field: {name}")

        # Reject empty or whitespace strings
        for name, val in [
            ("evidence_id", self.evidence_id),
            ("classification", self.classification),
            ("payload_commitment", self.payload_commitment),
            ("trust_marker", self.trust_marker),
        ]:
            if not isinstance(val, str) or not val.strip():
                raise InvalidDecisionException(f"Field {name} must be a non-empty string")


@dataclass
class DecisionContext:
    """
    Evaluation context containing environmental and temporal constraints.
    """
    context_id: str
    policy_version: str
    system_id: str
    evaluation_timestamp: float
    evaluation_nonce: str

    def __post_init__(self):
        # Reject boolean type confusion
        for name, val in [
            ("context_id", self.context_id),
            ("policy_version", self.policy_version),
            ("system_id", self.system_id),
            ("evaluation_nonce", self.evaluation_nonce),
            ("evaluation_timestamp", self.evaluation_timestamp),
        ]:
            if isinstance(val, bool):
                raise InvalidDecisionException(f"Boolean type confusion not permitted for field: {name}")

        # Reject empty/whitespace strings
        for name, val in [
            ("context_id", self.context_id),
            ("policy_version", self.policy_version),
            ("system_id", self.system_id),
            ("evaluation_nonce", self.evaluation_nonce),
        ]:
            if not isinstance(val, str) or not val.strip():
                raise InvalidDecisionException(f"Field {name} must be a non-empty string")

        # Timestamp validation
        if not isinstance(self.evaluation_timestamp, (int, float)) or self.evaluation_timestamp <= 0:
            raise InvalidDecisionException("evaluation_timestamp must be a positive number")

        if self.evaluation_timestamp > time.time() + 5.0:
            raise InvalidDecisionException("evaluation_timestamp cannot be in the future (> now + 5.0s)")


@dataclass
class SecurityDecision:
    """
    Deterministic security evaluation decision artifact.
    Explicitly carries zero execution or authorization authority.
    """
    decision_id: str
    classification: DecisionClassification
    status: DecisionStatus
    reason_codes: List[DecisionReasonCode]
    context: DecisionContext
    evidence_references: List[DecisionEvidenceReference]
    decision_timestamp: float

    def __post_init__(self):
        # Reject boolean type confusion
        for name, val in [
            ("decision_id", self.decision_id),
            ("decision_timestamp", self.decision_timestamp),
        ]:
            if isinstance(val, bool):
                raise InvalidDecisionException(f"Boolean type confusion not permitted for field: {name}")

        if not isinstance(self.decision_id, str) or not self.decision_id.strip():
            raise InvalidDecisionException("decision_id must be a non-empty string")

        # Classification check
        if not isinstance(self.classification, DecisionClassification):
            if isinstance(self.classification, str):
                val_upper = self.classification.upper().strip()
                if val_upper in BANNED_CLASSIFICATION_TERMS:
                    raise InvalidDecisionException(f"Classification term '{val_upper}' is banned in Phase 6")
                try:
                    self.classification = DecisionClassification(val_upper)
                except ValueError:
                    raise InvalidDecisionException(f"Invalid DecisionClassification: {self.classification}")
            else:
                raise InvalidDecisionException("classification must be a DecisionClassification enum")

        if self.classification.value in BANNED_CLASSIFICATION_TERMS:
            raise InvalidDecisionException(f"Forbidden classification term: {self.classification.value}")

        # Status check
        if not isinstance(self.status, DecisionStatus):
            if isinstance(self.status, str):
                try:
                    self.status = DecisionStatus(self.status.upper().strip())
                except ValueError:
                    raise InvalidDecisionException(f"Invalid DecisionStatus: {self.status}")
            else:
                raise InvalidDecisionException("status must be a DecisionStatus enum")

        # Reason codes check
        if not isinstance(self.reason_codes, list) or len(self.reason_codes) == 0:
            raise InvalidDecisionException("reason_codes must be a non-empty list of DecisionReasonCode")

        # Context check
        if not isinstance(self.context, DecisionContext):
            raise InvalidDecisionException("context must be a valid DecisionContext instance")

        # Evidence references check
        if not isinstance(self.evidence_references, list):
            raise InvalidDecisionException("evidence_references must be a list of DecisionEvidenceReference")

        # Timestamp validation
        if not isinstance(self.decision_timestamp, (int, float)) or self.decision_timestamp <= 0:
            raise InvalidDecisionException("decision_timestamp must be a positive number")

        if self.decision_timestamp > time.time() + 5.0:
            raise InvalidDecisionException("decision_timestamp cannot be in the future (> now + 5.0s)")


@dataclass
class AttestationRecord:
    """
    Cryptographically committed attestation of a security decision.
    Binds policy version, evidence commitments, classification, and nonces.
    """
    attestation_id: str
    decision_id: str
    decision_commitment: str
    policy_version: str
    classification: DecisionClassification
    attestation_timestamp: float
    attestation_nonce: str
    evidence_commitments: List[str]
    is_research_only: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Reject boolean type confusion for non-bool fields
        for name, val in [
            ("attestation_id", self.attestation_id),
            ("decision_id", self.decision_id),
            ("decision_commitment", self.decision_commitment),
            ("policy_version", self.policy_version),
            ("attestation_nonce", self.attestation_nonce),
            ("attestation_timestamp", self.attestation_timestamp),
        ]:
            if isinstance(val, bool):
                raise InvalidDecisionException(f"Boolean type confusion not permitted for field: {name}")

        if not isinstance(self.is_research_only, bool):
            raise InvalidDecisionException("is_research_only must be a boolean")

        # Check strings
        for name, val in [
            ("attestation_id", self.attestation_id),
            ("decision_id", self.decision_id),
            ("decision_commitment", self.decision_commitment),
            ("policy_version", self.policy_version),
            ("attestation_nonce", self.attestation_nonce),
        ]:
            if not isinstance(val, str) or not val.strip():
                raise InvalidDecisionException(f"Field {name} must be a non-empty string")

        # Classification check
        if not isinstance(self.classification, DecisionClassification):
            if isinstance(self.classification, str):
                val_upper = self.classification.upper().strip()
                if val_upper in BANNED_CLASSIFICATION_TERMS:
                    raise InvalidDecisionException(f"Classification term '{val_upper}' is banned in Phase 6")
                try:
                    self.classification = DecisionClassification(val_upper)
                except ValueError:
                    raise InvalidDecisionException(f"Invalid DecisionClassification: {self.classification}")
            else:
                raise InvalidDecisionException("classification must be a DecisionClassification enum")

        # Evidence commitments list check
        if not isinstance(self.evidence_commitments, list):
            raise InvalidDecisionException("evidence_commitments must be a list of strings")

        for item in self.evidence_commitments:
            if isinstance(item, bool) or not isinstance(item, str) or not item.strip():
                raise InvalidDecisionException("Each evidence commitment must be a non-empty string")

        # Timestamp check
        if not isinstance(self.attestation_timestamp, (int, float)) or self.attestation_timestamp <= 0:
            raise InvalidDecisionException("attestation_timestamp must be a positive number")

        if self.attestation_timestamp > time.time() + 5.0:
            raise InvalidDecisionException("attestation_timestamp cannot be in the future (> now + 5.0s)")

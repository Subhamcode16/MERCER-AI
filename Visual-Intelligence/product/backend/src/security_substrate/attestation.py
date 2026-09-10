"""
IF-ATTESTATION-001 Phase 6 Canonical Attestation & Cryptographic Binding.
Computes and verifies deterministic SHA-256 commitments over decision artifacts.
"""

import hmac
import hashlib
import json
import uuid
import time
from typing import List, Dict, Any, Optional

from .decision_models import (
    SecurityDecision,
    AttestationRecord,
    DecisionClassification,
    InvalidDecisionException,
)
from .exceptions import AttestationTamperedException


def canonicalize_decision(decision: SecurityDecision) -> str:
    """
    Produces a canonical JSON string representation of a SecurityDecision.
    Ensures deterministic key ordering and formatting.
    """
    if not isinstance(decision, SecurityDecision):
        raise InvalidDecisionException("decision must be a valid SecurityDecision instance")

    evidence_commitments = sorted([
        ref.payload_commitment for ref in decision.evidence_references
    ])
    reason_codes = sorted([r.value for r in decision.reason_codes])

    canonical_obj = {
        "decision_id": decision.decision_id,
        "classification": decision.classification.value,
        "status": decision.status.value,
        "reason_codes": reason_codes,
        "policy_version": decision.context.policy_version,
        "system_id": decision.context.system_id,
        "evaluation_nonce": decision.context.evaluation_nonce,
        "evaluation_timestamp": decision.context.evaluation_timestamp,
        "evidence_commitments": evidence_commitments,
        "decision_timestamp": decision.decision_timestamp,
    }
    return json.dumps(canonical_obj, sort_keys=True, separators=(",", ":"))


def compute_decision_commitment(decision: SecurityDecision) -> str:
    """
    Computes a SHA-256 commitment hash over the canonical decision object.
    """
    canonical_bytes = canonicalize_decision(decision).encode("utf-8")
    return hashlib.sha256(canonical_bytes).hexdigest()


def create_attestation(
    decision: SecurityDecision,
    attestation_nonce: Optional[str] = None,
) -> AttestationRecord:
    """
    Creates a cryptographically committed AttestationRecord bound to a SecurityDecision.
    """
    if not isinstance(decision, SecurityDecision):
        raise InvalidDecisionException("decision must be a valid SecurityDecision instance")

    if attestation_nonce is None:
        attestation_nonce = uuid.uuid4().hex
    elif isinstance(attestation_nonce, bool) or not isinstance(attestation_nonce, str) or not attestation_nonce.strip():
        raise InvalidDecisionException("attestation_nonce must be a non-empty string")

    commitment = compute_decision_commitment(decision)
    evidence_commitments = sorted([
        ref.payload_commitment for ref in decision.evidence_references
    ])
    is_research = (decision.classification == DecisionClassification.RESEARCH_ONLY)

    return AttestationRecord(
        attestation_id=f"att-{uuid.uuid4().hex[:12]}",
        decision_id=decision.decision_id,
        decision_commitment=commitment,
        policy_version=decision.context.policy_version,
        classification=decision.classification,
        attestation_timestamp=time.time(),
        attestation_nonce=attestation_nonce,
        evidence_commitments=evidence_commitments,
        is_research_only=is_research,
    )


def verify_attestation(attestation: AttestationRecord, decision: SecurityDecision) -> bool:
    """
    Verifies that an AttestationRecord matches a given SecurityDecision.
    Raises AttestationTamperedException if tampered or mismatched.
    """
    if not isinstance(attestation, AttestationRecord):
        raise InvalidDecisionException("attestation must be an AttestationRecord instance")
    if not isinstance(decision, SecurityDecision):
        raise InvalidDecisionException("decision must be a SecurityDecision instance")

    # 1. Structural matches
    if attestation.decision_id != decision.decision_id:
        raise AttestationTamperedException("attestation decision_id does not match decision")

    if attestation.classification != decision.classification:
        raise AttestationTamperedException("attestation classification does not match decision")

    if attestation.policy_version != decision.context.policy_version:
        raise AttestationTamperedException("attestation policy_version does not match decision context")

    # 2. Recompute commitment
    expected_commitment = compute_decision_commitment(decision)

    # 3. Constant-time comparison
    if not hmac.compare_digest(attestation.decision_commitment, expected_commitment):
        raise AttestationTamperedException("Cryptographic decision commitment verification failed")

    return True

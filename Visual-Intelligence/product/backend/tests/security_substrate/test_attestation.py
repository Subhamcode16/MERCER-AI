"""
Tests for Phase 6 attestation serialization and cryptographic commitment verification.
"""

import time
import pytest
from security_substrate import (
    DecisionContext,
    SecurityDecision,
    DecisionClassification,
    DecisionStatus,
    DecisionReasonCode,
    DecisionEvidenceReference,
    create_attestation,
    verify_attestation,
    compute_decision_commitment,
    AttestationTamperedException,
)


def make_decision() -> SecurityDecision:
    ctx = DecisionContext(
        context_id="ctx-att-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-att-1",
    )
    ref1 = DecisionEvidenceReference("ev-1", "VERIFICATION_EVIDENCE", "a" * 64, "PROD")
    ref2 = DecisionEvidenceReference("ev-2", "ASSURANCE_EVIDENCE", "b" * 64, "PROD")

    return SecurityDecision(
        decision_id="dec-att-100",
        classification=DecisionClassification.EVALUATION_PASS,
        status=DecisionStatus.EVALUATED,
        reason_codes=[DecisionReasonCode.EVIDENCE_SUFFICIENT_AND_VALID],
        context=ctx,
        evidence_references=[ref1, ref2],
        decision_timestamp=time.time(),
    )


def test_attestation_creation_and_verification_pass():
    dec = make_decision()
    att = create_attestation(dec, attestation_nonce="nonce-att-unique")

    assert att.decision_id == dec.decision_id
    assert att.classification == dec.classification
    assert verify_attestation(att, dec) is True


def test_attestation_verification_failure_on_decision_id_mismatch():
    dec = make_decision()
    att = create_attestation(dec)
    att.decision_id = "dec-tampered"

    with pytest.raises(AttestationTamperedException, match="decision_id"):
        verify_attestation(att, dec)


def test_attestation_verification_failure_on_commitment_tamper():
    dec = make_decision()
    att = create_attestation(dec)
    att.decision_commitment = "0" * 64

    with pytest.raises(AttestationTamperedException, match="commitment"):
        verify_attestation(att, dec)


def test_attestation_verification_failure_on_classification_tamper():
    dec = make_decision()
    att = create_attestation(dec)
    att.classification = DecisionClassification.EVALUATION_FAIL

    with pytest.raises(AttestationTamperedException, match="classification"):
        verify_attestation(att, dec)


def test_attestation_verification_failure_on_modified_evidence_ref():
    dec = make_decision()
    att = create_attestation(dec)

    # Mutate evidence ref in decision object
    dec.evidence_references[0].payload_commitment = "f" * 64

    with pytest.raises(AttestationTamperedException, match="commitment"):
        verify_attestation(att, dec)

"""
Tests for Phase 6 decision and attestation data models.
"""

import time
import pytest
from security_substrate import (
    DecisionClassification,
    DecisionStatus,
    DecisionReasonCode,
    DecisionEvidenceReference,
    DecisionContext,
    SecurityDecision,
    AttestationRecord,
    InvalidDecisionException,
)


def test_decision_evidence_reference_valid():
    ref = DecisionEvidenceReference(
        evidence_id="ev-123",
        classification="VERIFICATION_EVIDENCE",
        payload_commitment="a" * 64,
        trust_marker="PRODUCTION_EVIDENCE",
    )
    assert ref.evidence_id == "ev-123"


def test_decision_evidence_reference_boolean_confusion():
    with pytest.raises(InvalidDecisionException, match="Boolean type confusion"):
        DecisionEvidenceReference(
            evidence_id=True,
            classification="VERIFICATION_EVIDENCE",
            payload_commitment="a" * 64,
            trust_marker="PRODUCTION_EVIDENCE",
        )


def test_decision_evidence_reference_empty_string():
    with pytest.raises(InvalidDecisionException, match="non-empty string"):
        DecisionEvidenceReference(
            evidence_id="   ",
            classification="VERIFICATION_EVIDENCE",
            payload_commitment="a" * 64,
            trust_marker="PRODUCTION_EVIDENCE",
        )


def test_decision_context_valid():
    ctx = DecisionContext(
        context_id="ctx-001",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="nonce-999",
    )
    assert ctx.context_id == "ctx-001"


def test_decision_context_future_timestamp():
    with pytest.raises(InvalidDecisionException, match="future"):
        DecisionContext(
            context_id="ctx-001",
            policy_version="6.0.0",
            system_id="sys-prod",
            evaluation_timestamp=time.time() + 100.0,
            evaluation_nonce="nonce-999",
        )


def test_security_decision_banned_classification():
    ctx = DecisionContext(
        context_id="ctx-001",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="nonce-999",
    )
    with pytest.raises(InvalidDecisionException, match="banned"):
        SecurityDecision(
            decision_id="dec-001",
            classification="AUTHORIZED",
            status=DecisionStatus.EVALUATED,
            reason_codes=[DecisionReasonCode.EVIDENCE_SUFFICIENT_AND_VALID],
            context=ctx,
            evidence_references=[],
            decision_timestamp=time.time(),
        )


def test_security_decision_valid():
    ctx = DecisionContext(
        context_id="ctx-001",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="nonce-999",
    )
    dec = SecurityDecision(
        decision_id="dec-001",
        classification=DecisionClassification.EVALUATION_PASS,
        status=DecisionStatus.EVALUATED,
        reason_codes=[DecisionReasonCode.EVIDENCE_SUFFICIENT_AND_VALID],
        context=ctx,
        evidence_references=[],
        decision_timestamp=time.time(),
    )
    assert dec.decision_id == "dec-001"
    assert dec.classification == DecisionClassification.EVALUATION_PASS


def test_attestation_record_valid():
    rec = AttestationRecord(
        attestation_id="att-001",
        decision_id="dec-001",
        decision_commitment="b" * 64,
        policy_version="6.0.0",
        classification=DecisionClassification.EVALUATION_PASS,
        attestation_timestamp=time.time(),
        attestation_nonce="nonce-att-001",
        evidence_commitments=["c" * 64],
        is_research_only=False,
    )
    assert rec.attestation_id == "att-001"
    assert not rec.is_research_only

"""
Tests for Phase 6 DecisionPolicy evaluation logic.
"""

import time
import pytest
from security_substrate import (
    DecisionPolicy,
    DecisionContext,
    DecisionClassification,
    DecisionStatus,
    DecisionReasonCode,
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
)


def make_record(
    evidence_id: str,
    classification: EvidenceClassification,
    status: EvidenceStatus = EvidenceStatus.VALIDATED,
    creation_offset: float = 0.0,
    trust_marker: str = "PRODUCTION_EVIDENCE",
    correlation_id: str = "corr-001",
    payload_commitment: str = "comm-001",
) -> NormalizedEvidenceRecord:
    now = time.time()
    return NormalizedEvidenceRecord(
        evidence_id=evidence_id,
        classification=classification,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=status,
        system_id="sys-prod",
        protocol_version="1.0.0",
        creation_time=now - creation_offset,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment=payload_commitment,
        unique_nonce=f"nonce-{evidence_id}",
        correlation_id=correlation_id,
        trust_marker=trust_marker,
    )


def test_decision_policy_pass():
    policy = DecisionPolicy(policy_version="6.0.0")
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.EVALUATION_PASS
    assert status == DecisionStatus.EVALUATED
    assert DecisionReasonCode.EVIDENCE_SUFFICIENT_AND_VALID in reasons


def test_decision_policy_insufficient_evidence():
    policy = DecisionPolicy(policy_version="6.0.0")
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.INSUFFICIENT_EVIDENCE
    assert status == DecisionStatus.REJECTED
    assert DecisionReasonCode.MISSING_REQUIRED_EVIDENCE in reasons


def test_decision_policy_quarantined_evidence():
    policy = DecisionPolicy(policy_version="6.0.0")
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE, status=EvidenceStatus.QUARANTINED),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.EVIDENCE_QUARANTINED
    assert status == DecisionStatus.QUARANTINED
    assert DecisionReasonCode.EVIDENCE_QUARANTINED_OR_REJECTED in reasons


def test_decision_policy_expired_evidence():
    policy = DecisionPolicy(policy_version="6.0.0", max_freshness_window=60.0)
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE, creation_offset=100.0),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.EVIDENCE_EXPIRED
    assert status == DecisionStatus.EXPIRED
    assert DecisionReasonCode.EVIDENCE_EXPIRED_OR_STALE in reasons


def test_decision_policy_research_evidence():
    policy = DecisionPolicy(policy_version="6.0.0")
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE),
        make_record(
            "e2",
            EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE,
            trust_marker="TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION",
        ),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.RESEARCH_ONLY
    assert status == DecisionStatus.EVALUATED
    assert DecisionReasonCode.RESEARCH_EVIDENCE_NOT_AUTHORITATIVE in reasons


def test_decision_policy_conflict_evidence():
    policy = DecisionPolicy(policy_version="6.0.0")
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE, correlation_id="c1", payload_commitment="comm-A"),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE, correlation_id="c1", payload_commitment="comm-B"),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.EVIDENCE_CONFLICT
    assert status == DecisionStatus.REJECTED
    assert DecisionReasonCode.EVIDENCE_CONTRADICTION_DETECTED in reasons


def test_decision_policy_version_mismatch():
    policy = DecisionPolicy(policy_version="6.0.0")
    ctx = DecisionContext(
        context_id="ctx-1",
        policy_version="5.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE),
    ]
    cls, status, reasons = policy.evaluate(records, ctx)
    assert cls == DecisionClassification.EVALUATION_FAIL
    assert status == DecisionStatus.REJECTED
    assert DecisionReasonCode.POLICY_VERSION_MISMATCH in reasons

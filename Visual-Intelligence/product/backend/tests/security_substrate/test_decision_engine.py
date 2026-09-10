"""
Tests for Phase 6 SecurityDecisionEngine processing and attestation generation.
"""

import time
import pytest
from security_substrate import (
    SecurityDecisionEngine,
    DecisionPolicy,
    DecisionReplayCache,
    DecisionContext,
    DecisionClassification,
    DecisionStatus,
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    verify_attestation,
    DecisionReplayException,
)


def make_record(
    evidence_id: str,
    classification: EvidenceClassification,
) -> NormalizedEvidenceRecord:
    now = time.time()
    return NormalizedEvidenceRecord(
        evidence_id=evidence_id,
        classification=classification,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.VALIDATED,
        system_id="sys-prod",
        protocol_version="1.0.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment=f"comm-{evidence_id}",
        unique_nonce=f"nonce-{evidence_id}",
        correlation_id=f"corr-{evidence_id}",
        trust_marker="PRODUCTION_EVIDENCE",
    )



def test_decision_engine_evaluation_pass():
    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-eng-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-eng-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE),
    ]

    decision, attestation = engine.evaluate_evidence(records, ctx)

    assert decision.classification == DecisionClassification.EVALUATION_PASS
    assert decision.status == DecisionStatus.EVALUATED
    assert verify_attestation(attestation, decision) is True
    assert len(decision.evidence_references) == 2


def test_decision_engine_replays_decision_id():
    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-eng-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-eng-1",
    )
    records = [
        make_record("e1", EvidenceClassification.VERIFICATION_EVIDENCE),
        make_record("e2", EvidenceClassification.ASSURANCE_EVIDENCE),
    ]

    dec1, att1 = engine.evaluate_evidence(records, ctx)

    # Manually re-register same decision ID
    with pytest.raises(DecisionReplayException):
        engine.replay_cache.check_and_register(dec1.decision_id, "nonce-new")


def test_decision_engine_has_no_execution_gate_methods():
    engine = SecurityDecisionEngine()
    for method in ["authorize", "unlock", "execute", "permit", "verify_for_execution"]:
        assert not hasattr(engine, method), f"SecurityDecisionEngine must not possess method: {method}"

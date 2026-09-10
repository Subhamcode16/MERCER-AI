"""
Test T07 — Conflicting Evidence Handling in Real Workflow Execution.
"""

import time
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    NormalizedEvidenceRecord,
    SecurityDecisionEngine,
    DecisionContext,
)
from src.workflow_integration import (
    AssetReference,
    WorkflowRunContext,
)


def test_t07_conflicting_evidence_surfaced():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    now = time.time()
    # Create two evidence records with SAME correlation_id but DIFFERENT payload commitments
    ev1 = NormalizedEvidenceRecord(
        evidence_id="ev-t07-01",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="hash_AAA",
        unique_nonce="nonce_t07_1",
        correlation_id="corr-t07-shared",
        trust_marker="PRODUCTION_EVIDENCE",
    )
    ev2 = NormalizedEvidenceRecord(
        evidence_id="ev-t07-02",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="hash_BBB",  # Conflict! Same correlation_id, different commitment!
        unique_nonce="nonce_t07_2",
        correlation_id="corr-t07-shared",
        trust_marker="PRODUCTION_EVIDENCE",
    )

    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-t07",
        policy_version="6.0.0",
        system_id="SYSTEM_001",
        evaluation_timestamp=now,
        evaluation_nonce="non-t07",
    )

    decision, attestation = engine.evaluate_evidence([ev1, ev2], ctx)
    assert decision.classification.value == "EVIDENCE_CONFLICT"
    assert gate.is_permitted() is False


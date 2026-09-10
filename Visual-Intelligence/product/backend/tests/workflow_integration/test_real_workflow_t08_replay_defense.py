"""
Test T08 — Replay Defense in Real Workflow Execution.
"""

import time
import pytest
from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    EvidenceOrchestrator,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    NormalizedEvidenceRecord,
    ReplayAttackException,
)


def test_t08_replayed_evidence_rejected():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    orchestrator = EvidenceOrchestrator()
    now = time.time()

    rec1 = NormalizedEvidenceRecord(
        evidence_id="ev-t08-01",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="hash_t08",
        unique_nonce="nonce_t08_replay",
        correlation_id="corr-t08",
        trust_marker="PRODUCTION_EVIDENCE",
    )

    orchestrator.ingest_evidence(rec1)

    # Attempt to ingest duplicate evidence with same evidence_id
    with pytest.raises(ReplayAttackException):
        orchestrator.ingest_evidence(rec1)

    assert gate.is_permitted() is False

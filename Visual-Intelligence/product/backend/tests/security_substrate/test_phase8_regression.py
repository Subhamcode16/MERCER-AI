"""
Phase 8 Cross-Phase Baseline Regression Suite.
Validates that Phase 1 through Phase 7 core components function without degradation alongside Phase 8.
"""

import time
from dataclasses import asdict
import pytest

from src.security_substrate import (
    EpistemicStateStore,
    AssuranceLoopController,
    ExecutionGate,
    OptionHVerificationHarness,
    VerificationClaim,
    EvidenceOrchestrator,
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    SecurityDecisionEngine,
    DecisionContext,
    SecurityAuditBoundary,
    SecurityReconciler,
    ReconciliationSnapshot,
    ReconciliationStatus,
    compute_salted_commitment,
)


def test_phase1_to_phase8_end_to_end_baseline():
    # 1. Phase 1 — Epistemic Controller & Execution Gate
    store = EpistemicStateStore()
    controller = AssuranceLoopController(store)
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    # 2. Phase 2 — Option H Verification Harness
    harness = OptionHVerificationHarness()
    salt = b"0" * 32
    asset_bytes = bytearray(b"sample visual asset bytes")
    expected_hash = compute_salted_commitment(asset_bytes, salt)
    claim = VerificationClaim(
        claim_id="clm-reg-p8",
        target_property="VISUAL_INTEGRITY",
        expected_salted_hash=expected_hash,
        salt=salt,
    )
    res_harness = harness.evaluate_asset_claim(asset_bytes, claim, "ta-001")
    assert res_harness.claim_id == "clm-reg-p8"

    # 3. Phase 5 — Evidence Orchestrator Ingestion
    orchestrator = EvidenceOrchestrator()
    now = time.time()
    rec_verif = NormalizedEvidenceRecord(
        evidence_id="ev-reg-p8-verif",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment=expected_hash,
        unique_nonce="nonce-reg-p8-verif",
        correlation_id="corr-reg-p8",
        trust_marker="PRODUCTION_EVIDENCE",
    )
    orchestrator.ingest_evidence(rec_verif)
    assert orchestrator.get_audit_log_size() == 1

    # 4. Phase 6 — Security Decision Engine
    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-reg-p8",
        policy_version="6.0.0",
        system_id="SYSTEM_001",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-reg-p8",
    )
    evidence_records = orchestrator.list_evidence_records()
    decision, attestation = engine.evaluate_evidence(evidence_records, ctx)
    assert decision.decision_id is not None

    # 5. Phase 7 — Security Audit Boundary Logging
    boundary = SecurityAuditBoundary()
    audit_record = boundary.record_attestation(attestation, source_phase="PHASE_6_DECISION")
    assert audit_record.sequence_number == 1

    # 6. Phase 8 — Security Reconciler Execution
    reconciler = SecurityReconciler()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-reg-p8",
        system_id="SYSTEM_001",
        correlation_id="corr-reg-p8",
        timestamp=now,
        evidence_records=[asdict(rec_verif)],
        decision_records=[asdict(decision)],
        attestation_records=[asdict(attestation)],
        audit_records=[asdict(audit_record)],
    )


    res_rec = reconciler.reconcile(snapshot)
    assert res_rec.status == ReconciliationStatus.CONSISTENT
    assert res_rec.is_authoritative is False

    # ExecutionGate MUST remain fail-closed
    assert gate.is_permitted() is False

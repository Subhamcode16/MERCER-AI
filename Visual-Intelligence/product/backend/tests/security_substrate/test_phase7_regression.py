"""
Phase 7 Full Multi-Phase System Integration & Regression Suite.
Verifies end-to-end integration across Phases 1–7 while preserving all substrate security invariants.
"""

import time
import pytest
from security_substrate import (
    EpistemicState,
    EpistemicStateStore,
    AssuranceLoopController,
    ExecutionGate,
    OptionHVerificationHarness,
    VerificationClaim,
    RecoveryManager,
    RecoveryEpochStore,
    CapabilityPayloadParser,
    EvidenceOrchestrator,
    ResearchAdapter,
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    SecurityDecisionEngine,
    DecisionContext,
    DecisionClassification,
    SecurityAuditBoundary,
    AuditRecordType,
    compute_salted_commitment,
)



def test_full_multiphase_end_to_end_regression():
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
        claim_id="clm-reg-p7",
        target_property="VISUAL_INTEGRITY",
        expected_salted_hash=expected_hash,
        salt=salt,
    )
    res_harness = harness.evaluate_asset_claim(asset_bytes, claim, "ta-001")
    assert res_harness.claim_id == "clm-reg-p7"

    # 3. Phase 5 — Evidence Orchestrator Ingestion
    orchestrator = EvidenceOrchestrator()
    now = time.time()
    rec_verif = NormalizedEvidenceRecord(
        evidence_id="ev-reg-verif",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment=res_harness.evidence.asset_hash if res_harness.evidence else expected_hash,
        unique_nonce="nonce-reg-verif",
        correlation_id="corr-reg-1",
        trust_marker="PRODUCTION_EVIDENCE",
    )
    rec_assur = NormalizedEvidenceRecord(
        evidence_id="ev-reg-assur",
        classification=EvidenceClassification.ASSURANCE_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_1_ASSURANCE,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="comm-assur-hash",
        unique_nonce="nonce-reg-assur",
        correlation_id="corr-reg-2",
        trust_marker="PRODUCTION_EVIDENCE",
    )
    orchestrator.ingest_evidence(rec_verif)
    orchestrator.ingest_evidence(rec_assur)
    assert orchestrator.get_audit_log_size() == 2


    # 4. Phase 6 — Security Decision Engine
    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-reg-p7",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-reg-p7",
    )
    evidence_records = orchestrator.list_evidence_records()
    decision, attestation = engine.evaluate_evidence(evidence_records, ctx)
    assert decision.decision_id is not None

    # 5. Phase 7 — Security Audit Boundary Logging
    boundary = SecurityAuditBoundary()
    audit_record = boundary.record_attestation(attestation, source_phase="PHASE_6_DECISION")
    assert audit_record.sequence_number == 1

    # 6. Integrity Check
    res_integrity = boundary.verify_audit_integrity()
    assert res_integrity.is_valid is True
    assert res_integrity.total_records_checked == 2  # Genesis + Audit Record

    # 7. Final Gate Check — ExecutionGate remains strictly locked
    assert gate.is_permitted() is False

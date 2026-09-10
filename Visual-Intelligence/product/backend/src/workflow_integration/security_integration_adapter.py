"""
Security Integration Adapter for Visual Intelligence Real Workflow Pipeline (Phase 8).

Translates visual analysis outputs into security-substrate contracts across Phases 2, 5, 6, 7, and 8.
"""

import time
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Tuple

from src.security_substrate import (
    AuditRecord,
    AttestationRecord,
    DecisionContext,
    EvidenceClassification,
    EvidenceOrchestrator,
    EvidenceProvenance,
    EvidenceStatus,
    MalformedEvidenceException,
    NormalizedEvidenceRecord,
    OptionHVerificationHarness,
    ReconciliationResult,
    ReconciliationSnapshot,
    SecurityAuditBoundary,
    SecurityDecision,
    SecurityDecisionEngine,
    SecurityReconciler,
    VerificationClaim,
    compute_salted_commitment,
    generate_salt,
)
from .workflow_models import WorkflowRunContext


class SecurityIntegrationAdapter:
    """
    Adapter connecting Visual Intelligence visual pipeline outputs to the security substrate.
    
    Orchestrates:
    - Phase 2: Ephemeral verification via OptionHVerificationHarness
    - Phase 5: Ingestion into EvidenceOrchestrator
    - Phase 6: Evaluation via SecurityDecisionEngine
    - Phase 7: Logging via SecurityAuditBoundary
    - Phase 8: Consistency evaluation via SecurityReconciler
    """

    def __init__(
        self,
        harness: Optional[OptionHVerificationHarness] = None,
        orchestrator: Optional[EvidenceOrchestrator] = None,
        decision_engine: Optional[SecurityDecisionEngine] = None,
        audit_boundary: Optional[SecurityAuditBoundary] = None,
        reconciler: Optional[SecurityReconciler] = None,
    ) -> None:
        self.harness = harness or OptionHVerificationHarness()
        self.orchestrator = orchestrator or EvidenceOrchestrator()
        self.decision_engine = decision_engine or SecurityDecisionEngine()
        self.audit_boundary = audit_boundary or SecurityAuditBoundary()
        self.reconciler = reconciler or SecurityReconciler()

    def process_visual_claims(
        self,
        context: WorkflowRunContext,
        asset_bytes: bytearray,
        visual_extraction_data: Dict[str, Any],
        salt: Optional[bytes] = None,
        custom_trust_marker: str = "PRODUCTION_EVIDENCE",
    ) -> Tuple[NormalizedEvidenceRecord, SecurityDecision, AttestationRecord, AuditRecord, ReconciliationResult]:
        """
        Pipes visual analysis extraction data through the Phase 2–8 security substrate.
        
        Returns:
            Tuple of (NormalizedEvidenceRecord, SecurityDecision, AttestationRecord, AuditRecord, ReconciliationResult).
        """
        if asset_bytes is None or not isinstance(asset_bytes, (bytearray, bytes)):
            raise MalformedEvidenceException("asset_bytes must be a valid bytearray or bytes object")

        now = time.time()
        effective_salt = salt or generate_salt()
        expected_hash = compute_salted_commitment(asset_bytes, effective_salt)

        # 1. Phase 2 — Option H Ephemeral Verification
        claim = VerificationClaim(
            claim_id=f"clm-{context.run_id}",
            target_property="VISUAL_INTEGRITY_SALTED_HASH",
            expected_salted_hash=expected_hash,
            salt=effective_salt,
        )
        harness_buffer = bytearray(asset_bytes)
        eval_result = self.harness.evaluate_asset_claim(
            asset_bytes=harness_buffer,
            claim=claim,
            trust_anchor_id="ta-visual-intelligence-001",
        )

        verification_status = (
            EvidenceStatus.RECEIVED if eval_result.status == "PASS" else EvidenceStatus.REJECTED
        )

        # 2. Phase 5 — Evidence Orchestration
        evidence_record = NormalizedEvidenceRecord(
            evidence_id=f"ev-{context.run_id}",
            classification=EvidenceClassification.VERIFICATION_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
            status=verification_status,
            system_id=context.system_id,
            protocol_version="1.0",
            creation_time=context.timestamp,
            ingestion_time=now,
            expiration_time=context.timestamp + 600.0,
            payload_commitment=expected_hash,
            unique_nonce=f"nonce-{context.run_id}",
            correlation_id=context.correlation_id,
            trust_marker=custom_trust_marker,
            metadata={"raw_claims": visual_extraction_data.get("raw_claims", [])},
        )

        self.orchestrator.ingest_evidence(evidence_record)

        # 3. Phase 6 — Security Decision Engine
        dec_context = DecisionContext(
            context_id=f"ctx-{context.run_id}",
            policy_version="6.0.0",
            system_id=context.system_id,
            evaluation_timestamp=now,
            evaluation_nonce=f"dec-nonce-{context.run_id}",
        )
        decision, attestation = self.decision_engine.evaluate_evidence(
            evidence_records=[evidence_record],
            context=dec_context,
        )

        # 4. Phase 7 — Security Audit Boundary Logging
        audit_record = self.audit_boundary.record_attestation(
            attestation=attestation,
            source_phase="PHASE_6_DECISION",
        )


        # 5. Phase 8 — Security Reconciler Execution
        snapshot = ReconciliationSnapshot(
            snapshot_id=f"snap-{context.run_id}",
            system_id=context.system_id,
            correlation_id=context.correlation_id,
            timestamp=now,
            evidence_records=[asdict(evidence_record)],
            decision_records=[asdict(decision)],
            attestation_records=[asdict(attestation)],
            audit_records=[asdict(audit_record)],
        )

        reconciliation_res = self.reconciler.reconcile(snapshot)

        return evidence_record, decision, attestation, audit_record, reconciliation_res

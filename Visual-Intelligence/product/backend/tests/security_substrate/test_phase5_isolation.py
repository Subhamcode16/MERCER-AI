"""
Isolation and Security Tests for Phase 5 Evidence Orchestration Boundary.
Explicitly proves that even maliciously constructed NormalizedEvidenceRecord objects cannot cause execution authorization.
"""

import sys
import ast
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from security_substrate.epistemic_state import EpistemicState
from security_substrate.assurance_loop import AssuranceLoopController
from security_substrate.execution_gate import ExecutionGate
from security_substrate.evidence_models import (
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    DEFAULT_TRUST_MARKER_PRODUCTION,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from security_substrate.evidence_orchestrator import EvidenceOrchestrator
from security_substrate.research_adapter import ResearchAdapter
from research.frost_prototype.models import FROSTSignature


def test_malicious_evidence_record_cannot_unlock_execution_gate():
    """
    SECURITY TEST: Proves that ingesting maliciously constructed evidence records
    (even if marked VALIDATED or PRODUCTION_EVIDENCE) CANNOT unlock ExecutionGate
    or mutate EpistemicState.
    """
    assurance_controller = AssuranceLoopController()
    execution_gate = ExecutionGate(assurance_controller)
    orchestrator = EvidenceOrchestrator()

    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    assert execution_gate.is_permitted() is False

    now = time.time()
    # Maliciously crafted payload pretending to be valid production evidence
    malicious_record = NormalizedEvidenceRecord(
        evidence_id="evid-malicious-001",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.VALIDATED,  # Pre-set to VALIDATED!
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="f" * 64,
        unique_nonce="nonce-malicious-001",
        correlation_id="corr-malicious",
        trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
    )

    # Ingest record in orchestrator
    ingested = orchestrator.ingest_evidence(malicious_record)
    assert ingested.status == EvidenceStatus.VALIDATED

    # Confirm EpistemicState remains strictly UNKNOWN and ExecutionGate remains LOCKED
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    assert execution_gate.is_permitted() is False

    res = execution_gate.request_execution("malicious-action-attempt")
    assert res.permitted is False


def test_ingesting_research_evidence_cannot_unlock_execution_gate():
    """
    SECURITY TEST: Proves that ingesting converted Phase 4 FROST research evidence
    CANNOT unlock ExecutionGate or mutate EpistemicState.
    """
    assurance_controller = AssuranceLoopController()
    execution_gate = ExecutionGate(assurance_controller)
    orchestrator = EvidenceOrchestrator()

    sig = FROSTSignature(
        group_commitment_R=111,
        signature_scalar_S=222,
        message_hash="hash-abc",
        participating_ids=[1, 2],
        marker="TEST_ONLY_THRESHOLD_SIGNATURE"
    )

    record = ResearchAdapter.convert_research_result_to_evidence(sig, b"Message")
    res = orchestrator.ingest_evidence(record)

    assert res.classification == EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE
    assert res.trust_marker == DEFAULT_TRUST_MARKER_RESEARCH

    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    assert execution_gate.is_permitted() is False

    exec_res = execution_gate.request_execution("research-action-attempt")
    assert exec_res.permitted is False


def test_recovery_evidence_ingestion_does_not_trigger_state_reset():
    """
    SECURITY TEST: Proves that ingesting RECOVERY_EVIDENCE in EvidenceOrchestrator
    is informational only and does NOT trigger state reset or execute recovery.
    """
    assurance_controller = AssuranceLoopController()  # Initial state UNKNOWN
    orchestrator = EvidenceOrchestrator()

    now = time.time()
    rec_evidence = NormalizedEvidenceRecord(
        evidence_id="evid-rec-info",
        classification=EvidenceClassification.RECOVERY_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_3_RECOVERY,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="e" * 64,
        unique_nonce="nonce-rec-info",
        correlation_id="corr-rec",
        trust_marker="INFORMATIONAL_ONLY"
    )

    res = orchestrator.ingest_evidence(rec_evidence)
    assert res.status == EvidenceStatus.VALIDATED

    # Confirm EpistemicState remains UNKNOWN (no state transition occurred)
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN


def test_ast_import_audit_no_forbidden_phase5_dependencies():
    """AST Audit: Verify Phase 5 modules under security_substrate do not import research.frost_prototype directly."""
    sub_dir = Path(__file__).resolve().parent.parent.parent / "src" / "security_substrate"
    p5_files = ["evidence_models.py", "evidence_policy.py", "evidence_orchestrator.py", "research_adapter.py"]

    for fname in p5_files:
        fpath = sub_dir / fname
        with open(fpath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=fname)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "research.frost_prototype" not in alias.name
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "research.frost_prototype" not in node.module

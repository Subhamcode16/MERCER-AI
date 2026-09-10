"""
Tests for Phase 5 Evidence Orchestrator Boundary.
"""

import sys
import time
import concurrent.futures
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from security_substrate.evidence_models import (
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    DEFAULT_TRUST_MARKER_PRODUCTION,
)
from security_substrate.evidence_orchestrator import EvidenceOrchestrator


def create_sample_record(i: int) -> NormalizedEvidenceRecord:
    now = time.time()
    return NormalizedEvidenceRecord(
        evidence_id=f"evid-orch-{i}",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment=f"comm-hash-{i}",
        unique_nonce=f"nonce-orch-{i}",
        correlation_id=f"corr-{i}",
        trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
    )


def test_orchestrator_ingestion_success():
    """Verify ingesting valid evidence normalizes record and stores in audit log."""
    orchestrator = EvidenceOrchestrator()
    rec = create_sample_record(1)

    res = orchestrator.ingest_evidence(rec)
    assert res.status == EvidenceStatus.VALIDATED
    assert orchestrator.get_audit_log_size() == 1

    fetched = orchestrator.get_evidence_record("evid-orch-1")
    assert fetched is not None
    assert fetched.evidence_id == "evid-orch-1"


def test_orchestrator_filtering():
    """Verify filtering ingested records by classification and provenance."""
    orchestrator = EvidenceOrchestrator()
    rec1 = create_sample_record(1)
    rec2 = create_sample_record(2)

    orchestrator.ingest_evidence(rec1)
    orchestrator.ingest_evidence(rec2)

    verif_records = orchestrator.list_evidence_records(classification=EvidenceClassification.VERIFICATION_EVIDENCE)
    assert len(verif_records) == 2

    research_records = orchestrator.list_evidence_records(classification=EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE)
    assert len(research_records) == 0


def test_concurrent_evidence_ingestion():
    """Verify 20 concurrent threads ingesting evidence execute safely."""
    orchestrator = EvidenceOrchestrator()

    def worker(i):
        rec = create_sample_record(i)
        res = orchestrator.ingest_evidence(rec)
        return res.status

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(worker, range(20)))

    assert len(results) == 20
    assert all(r == EvidenceStatus.VALIDATED for r in results)
    assert orchestrator.get_audit_log_size() == 20


def test_orchestrator_has_no_execution_or_authorization_methods():
    """Reflection Audit: Verify EvidenceOrchestrator has NO authorize/unlock/execution methods."""
    orchestrator = EvidenceOrchestrator()
    prohibited_names = ["authorize", "verify_for_execution", "unlock", "permit_execution", "execute"]

    dir_names = dir(orchestrator)
    for forbidden in prohibited_names:
        assert forbidden not in dir_names, f"Forbidden method name '{forbidden}' found on EvidenceOrchestrator"

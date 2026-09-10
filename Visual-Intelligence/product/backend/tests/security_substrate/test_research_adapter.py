"""
Tests for Phase 5 Research Cryptographic Evidence Adapter.
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from research.frost_prototype.models import FROSTSignature
from security_substrate.evidence_models import (
    EvidenceClassification,
    EvidenceProvenance,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from security_substrate.research_adapter import ResearchAdapter
from security_substrate.evidence_orchestrator import EvidenceOrchestrator
from security_substrate.exceptions import MalformedEvidenceException


def test_research_adapter_conversion():
    """Verify converting FROSTSignature to NormalizedEvidenceRecord."""
    sig = FROSTSignature(
        group_commitment_R=123456789,
        signature_scalar_S=987654321,
        message_hash="hash-123",
        participating_ids=[1, 2, 3],
        marker="TEST_ONLY_THRESHOLD_SIGNATURE"
    )
    msg = b"Research Adapter Test Message"

    record = ResearchAdapter.convert_research_result_to_evidence(sig, msg, correlation_id="corr-research-1")

    assert record.classification == EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE
    assert record.provenance == EvidenceProvenance.PHASE_4_RESEARCH
    assert record.trust_marker == DEFAULT_TRUST_MARKER_RESEARCH
    assert record.metadata["group_commitment_R"] == "123456789"
    assert record.metadata["participating_ids"] == [1, 2, 3]


def test_research_adapter_ingestion_in_orchestrator():
    """Verify research evidence record ingests cleanly in EvidenceOrchestrator as RESEARCH_CRYPTOGRAPHIC_EVIDENCE."""
    sig = FROSTSignature(
        group_commitment_R=123456789,
        signature_scalar_S=987654321,
        message_hash="hash-123",
        participating_ids=[1, 2],
        marker="TEST_ONLY_THRESHOLD_SIGNATURE"
    )
    msg = b"Orchestration Ingestion Message"

    record = ResearchAdapter.convert_research_result_to_evidence(sig, msg)

    orchestrator = EvidenceOrchestrator()
    res = orchestrator.ingest_evidence(record)

    assert res.classification == EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE
    assert res.trust_marker == DEFAULT_TRUST_MARKER_RESEARCH


def test_invalid_signature_object_rejection():
    """Verify null signature object raises MalformedEvidenceException."""
    with pytest.raises(MalformedEvidenceException, match="Invalid or null"):
        ResearchAdapter.convert_research_result_to_evidence(None, b"msg")

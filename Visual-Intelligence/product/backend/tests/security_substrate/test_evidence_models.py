"""
Tests for Phase 5 Evidence Models & Schema Normalization Rules.
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pytest
from security_substrate.evidence_models import (
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    DEFAULT_TRUST_MARKER_RESEARCH,
    DEFAULT_TRUST_MARKER_PRODUCTION,
)
from security_substrate.exceptions import MalformedEvidenceException


def test_valid_evidence_record_creation():
    """Verify creating a valid NormalizedEvidenceRecord."""
    now = time.time()
    record = NormalizedEvidenceRecord(
        evidence_id="evid-001",
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=now + 600.0,
        payload_commitment="a" * 64,
        unique_nonce="nonce-001",
        correlation_id="corr-001",
        trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
    )

    assert record.evidence_id == "evid-001"
    assert record.classification == EvidenceClassification.VERIFICATION_EVIDENCE
    assert record.status == EvidenceStatus.RECEIVED


def test_boolean_type_confusion_rejection():
    """Verify boolean values in string/timestamp fields raise MalformedEvidenceException."""
    now = time.time()
    with pytest.raises(MalformedEvidenceException, match="Boolean type confusion"):
        NormalizedEvidenceRecord(
            evidence_id=True,  # Boolean confusion!
            classification=EvidenceClassification.VERIFICATION_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
            status=EvidenceStatus.RECEIVED,
            system_id="SYSTEM_001",
            protocol_version="1.0",
            creation_time=now,
            ingestion_time=now,
            expiration_time=now + 600.0,
            payload_commitment="a" * 64,
            unique_nonce="nonce-001",
            correlation_id="corr-001",
            trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
        )


def test_empty_string_rejection():
    """Verify empty or whitespace-only strings raise MalformedEvidenceException."""
    now = time.time()
    with pytest.raises(MalformedEvidenceException, match="non-empty string"):
        NormalizedEvidenceRecord(
            evidence_id="   ",  # Whitespace string!
            classification=EvidenceClassification.VERIFICATION_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
            status=EvidenceStatus.RECEIVED,
            system_id="SYSTEM_001",
            protocol_version="1.0",
            creation_time=now,
            ingestion_time=now,
            expiration_time=now + 600.0,
            payload_commitment="a" * 64,
            unique_nonce="nonce-001",
            correlation_id="corr-001",
            trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
        )


def test_research_provenance_trust_marker_enforcement():
    """Verify Phase 4 research evidence MUST carry RESEARCH_CRYPTOGRAPHIC_EVIDENCE and TEST_ONLY trust marker."""
    now = time.time()

    # Attempt to spoof research evidence as production evidence raises MalformedEvidenceException
    with pytest.raises(MalformedEvidenceException, match="Research evidence provenance"):
        NormalizedEvidenceRecord(
            evidence_id="evid-spoof",
            classification=EvidenceClassification.VERIFICATION_EVIDENCE,  # Attempted spoof!
            provenance=EvidenceProvenance.PHASE_4_RESEARCH,
            status=EvidenceStatus.RECEIVED,
            system_id="SYSTEM_001",
            protocol_version="1.0",
            creation_time=now,
            ingestion_time=now,
            expiration_time=now + 600.0,
            payload_commitment="a" * 64,
            unique_nonce="nonce-001",
            correlation_id="corr-001",
            trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION  # Attempted spoof!
        )


def test_expiration_before_creation_rejection():
    """Verify expiration_time < creation_time raises MalformedEvidenceException."""
    now = time.time()
    with pytest.raises(MalformedEvidenceException, match="Expiration time cannot be earlier"):
        NormalizedEvidenceRecord(
            evidence_id="evid-time-error",
            classification=EvidenceClassification.VERIFICATION_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
            status=EvidenceStatus.RECEIVED,
            system_id="SYSTEM_001",
            protocol_version="1.0",
            creation_time=now,
            ingestion_time=now,
            expiration_time=now - 50.0,  # Negative window!
            payload_commitment="a" * 64,
            unique_nonce="nonce-001",
            correlation_id="corr-001",
            trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
        )

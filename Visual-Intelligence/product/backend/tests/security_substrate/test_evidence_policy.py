"""
Tests for Phase 5 Evidence Policy Engine.
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
    DEFAULT_TRUST_MARKER_PRODUCTION,
)
from security_substrate.evidence_policy import EvidencePolicy
from security_substrate.exceptions import (
    ReplayAttackException,
    StaleTimestampException,
)


def create_test_record(
    evid_id: str = "evid-100",
    nonce: str = "nonce-100",
    commitment: str = "comm-100",
    creation_time: float = None,
    expiration_time: float = None
) -> NormalizedEvidenceRecord:
    now = time.time() if creation_time is None else creation_time
    exp = now + 600.0 if expiration_time is None else expiration_time
    return NormalizedEvidenceRecord(
        evidence_id=evid_id,
        classification=EvidenceClassification.VERIFICATION_EVIDENCE,
        provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
        status=EvidenceStatus.RECEIVED,
        system_id="SYSTEM_001",
        protocol_version="1.0",
        creation_time=now,
        ingestion_time=now,
        expiration_time=exp,
        payload_commitment=commitment,
        unique_nonce=nonce,
        correlation_id="corr-100",
        trust_marker=DEFAULT_TRUST_MARKER_PRODUCTION
    )


def test_valid_record_policy_pass():
    """Verify valid record passes policy validation and status becomes VALIDATED."""
    policy = EvidencePolicy()
    rec = create_test_record()
    status = policy.validate_record(rec)
    assert status == EvidenceStatus.VALIDATED
    assert rec.status == EvidenceStatus.VALIDATED


def test_expired_record_policy_failure():
    """Verify expired evidence record raises StaleTimestampException and sets status EXPIRED."""
    policy = EvidencePolicy()
    now = time.time()
    rec = create_test_record(creation_time=now - 2000.0, expiration_time=now - 100.0)

    with pytest.raises(StaleTimestampException, match="Expired evidence record"):
        policy.validate_record(rec)

    assert rec.status == EvidenceStatus.EXPIRED


def test_future_timestamp_policy_failure():
    """Verify creation_time > 5s in future raises StaleTimestampException."""
    policy = EvidencePolicy()
    now = time.time()
    rec = create_test_record(creation_time=now + 50.0, expiration_time=now + 600.0)

    with pytest.raises(StaleTimestampException, match="Future-dated creation timestamp"):
        policy.validate_record(rec)

    assert rec.status == EvidenceStatus.QUARANTINED


def test_duplicate_evidence_id_replay():
    """Verify submitting duplicate evidence ID raises ReplayAttackException."""
    policy = EvidencePolicy()
    rec1 = create_test_record(evid_id="dup-id", nonce="nonce-1", commitment="comm-1")
    rec2 = create_test_record(evid_id="dup-id", nonce="nonce-2", commitment="comm-2")

    policy.validate_record(rec1)

    with pytest.raises(ReplayAttackException, match="Duplicate evidence ID"):
        policy.validate_record(rec2)


def test_duplicate_nonce_replay():
    """Verify submitting replayed unique_nonce raises ReplayAttackException."""
    policy = EvidencePolicy()
    rec1 = create_test_record(evid_id="id-1", nonce="dup-nonce", commitment="comm-1")
    rec2 = create_test_record(evid_id="id-2", nonce="dup-nonce", commitment="comm-2")

    policy.validate_record(rec1)

    with pytest.raises(ReplayAttackException, match="Replayed unique_nonce"):
        policy.validate_record(rec2)


def test_duplicate_payload_commitment_replay():
    """Verify semantically identical payload commitment with different ID raises ReplayAttackException."""
    policy = EvidencePolicy()
    rec1 = create_test_record(evid_id="id-1", nonce="nonce-1", commitment="same-commitment-hash")
    rec2 = create_test_record(evid_id="id-2", nonce="nonce-2", commitment="same-commitment-hash")

    policy.validate_record(rec1)

    with pytest.raises(ReplayAttackException, match="Replayed payload commitment"):
        policy.validate_record(rec2)

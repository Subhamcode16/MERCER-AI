"""
Tests for Phase 7 audit record hashing, genesis record, and chain integrity verification.
"""

import time
import pytest
from security_substrate import (
    AuditRecord,
    AuditRecordType,
    AuditRecordStatus,
    create_genesis_record,
    compute_record_hash,
    verify_record_integrity,
    verify_chain_integrity,
)
from security_substrate.audit_integrity import (
    GENESIS_RECORD_ID,
    GENESIS_PREVIOUS_HASH,
)



def test_genesis_record_creation_and_integrity():
    genesis = create_genesis_record()
    assert genesis.record_id == GENESIS_RECORD_ID
    assert genesis.sequence_number == 0
    assert genesis.previous_record_hash == GENESIS_PREVIOUS_HASH
    assert verify_record_integrity(genesis) is True


def test_single_record_hash_tampering_detected():
    genesis = create_genesis_record()
    genesis.classification = "TAMPERED_CLASSIFICATION"
    assert verify_record_integrity(genesis) is False


def test_chain_integrity_valid_sequence():
    now = time.time()
    rec0 = create_genesis_record(creation_time=now)

    rec1_hash = compute_record_hash(
        record_id="aud-1",
        sequence_number=1,
        record_type=AuditRecordType.DECISION_ATTESTATION.value,
        created_at=now + 1,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash=rec0.record_hash,
        status=AuditRecordStatus.RECORDED.value,
    )
    rec1 = AuditRecord(
        record_id="aud-1",
        sequence_number=1,
        record_type=AuditRecordType.DECISION_ATTESTATION,
        created_at=now + 1,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash=rec0.record_hash,
        record_hash=rec1_hash,
        status=AuditRecordStatus.RECORDED,
    )

    res = verify_chain_integrity([rec0, rec1])
    assert res.is_valid is True
    assert res.total_records_checked == 2
    assert res.last_valid_sequence == 1


def test_chain_integrity_sequence_gap_detected():
    now = time.time()
    rec0 = create_genesis_record(creation_time=now)
    rec2_hash = compute_record_hash(
        record_id="aud-2",
        sequence_number=2,
        record_type=AuditRecordType.DECISION_ATTESTATION.value,
        created_at=now + 1,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash=rec0.record_hash,
        status=AuditRecordStatus.RECORDED.value,
    )
    rec2 = AuditRecord(
        record_id="aud-2",
        sequence_number=2,
        record_type=AuditRecordType.DECISION_ATTESTATION,
        created_at=now + 1,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash=rec0.record_hash,
        record_hash=rec2_hash,
        status=AuditRecordStatus.RECORDED,
    )

    res = verify_chain_integrity([rec0, rec2])
    assert res.is_valid is False
    assert "Sequence gap" in res.violation_reason


def test_chain_integrity_broken_previous_hash_link():
    now = time.time()
    rec0 = create_genesis_record(creation_time=now)
    rec1_hash = compute_record_hash(
        record_id="aud-1",
        sequence_number=1,
        record_type=AuditRecordType.DECISION_ATTESTATION.value,
        created_at=now + 1,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash="0" * 64,  # Mismatched previous_record_hash
        status=AuditRecordStatus.RECORDED.value,
    )
    rec1 = AuditRecord(
        record_id="aud-1",
        sequence_number=1,
        record_type=AuditRecordType.DECISION_ATTESTATION,
        created_at=now + 1,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash="0" * 64,
        record_hash=rec1_hash,
        status=AuditRecordStatus.RECORDED,
    )

    res = verify_chain_integrity([rec0, rec1])
    assert res.is_valid is False
    assert "Hash chain broken" in res.violation_reason

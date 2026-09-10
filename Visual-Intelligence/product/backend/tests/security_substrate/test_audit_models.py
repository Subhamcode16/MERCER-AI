"""
Tests for Phase 7 audit data models and schema validation rules.
"""

import time
import pytest
from security_substrate import (
    AuditRecord,
    AuditRecordType,
    AuditRecordStatus,
    AuditIntegrityResult,
    AuditQuery,
    AuditSequenceMetadata,
    AuditSchemaException,
)


def test_valid_audit_record_creation():
    rec = AuditRecord(
        record_id="aud-001",
        sequence_number=1,
        record_type=AuditRecordType.DECISION_ATTESTATION,
        created_at=time.time(),
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="a" * 64,
        previous_record_hash="b" * 64,
        record_hash="c" * 64,
        status=AuditRecordStatus.RECORDED,
    )
    assert rec.record_id == "aud-001"
    assert rec.sequence_number == 1


def test_audit_record_boolean_type_confusion():
    with pytest.raises(AuditSchemaException, match="Boolean type confusion"):
        AuditRecord(
            record_id=True,
            sequence_number=1,
            record_type=AuditRecordType.DECISION_ATTESTATION,
            created_at=time.time(),
            source_phase="PHASE_6_DECISION",
            classification="EVALUATION_PASS",
            policy_version="6.0.0",
            attestation_commitment="a" * 64,
            previous_record_hash="b" * 64,
            record_hash="c" * 64,
            status=AuditRecordStatus.RECORDED,
        )


def test_audit_record_negative_sequence_rejection():
    with pytest.raises(AuditSchemaException, match="non-negative integer"):
        AuditRecord(
            record_id="aud-001",
            sequence_number=-1,
            record_type=AuditRecordType.DECISION_ATTESTATION,
            created_at=time.time(),
            source_phase="PHASE_6_DECISION",
            classification="EVALUATION_PASS",
            policy_version="6.0.0",
            attestation_commitment="a" * 64,
            previous_record_hash="b" * 64,
            record_hash="c" * 64,
            status=AuditRecordStatus.RECORDED,
        )


def test_audit_record_banned_classification_term():
    with pytest.raises(AuditSchemaException, match="Forbidden classification"):
        AuditRecord(
            record_id="aud-001",
            sequence_number=1,
            record_type=AuditRecordType.DECISION_ATTESTATION,
            created_at=time.time(),
            source_phase="PHASE_6_DECISION",
            classification="AUTHORIZED",
            policy_version="6.0.0",
            attestation_commitment="a" * 64,
            previous_record_hash="b" * 64,
            record_hash="c" * 64,
            status=AuditRecordStatus.RECORDED,
        )


def test_audit_integrity_result_valid():
    res = AuditIntegrityResult(
        is_valid=True,
        total_records_checked=10,
        last_valid_sequence=9,
    )
    assert res.is_valid is True
    assert res.total_records_checked == 10

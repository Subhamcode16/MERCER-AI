"""
Tests for Phase 7 AuditStore append, monotonic sequence assignment, and concurrent safety.
"""

import time
import pytest
import concurrent.futures
from security_substrate import (
    AuditStore,
    AuditRecordType,
    AuditQuery,
    AuditReplayException,
    AuditSchemaException,
)


def test_audit_store_initialization_includes_genesis():
    store = AuditStore()
    records = store.get_all_records()
    assert len(records) == 1
    assert records[0].sequence_number == 0
    assert records[0].record_id == "audit-genesis-000"


def test_audit_store_append_single_attestation():
    store = AuditStore()
    rec = store.append_attestation(
        record_type=AuditRecordType.DECISION_ATTESTATION,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="comm-100",
    )
    assert rec.sequence_number == 1
    assert rec.attestation_commitment == "comm-100"
    assert store.get_audit_log_size() == 2 if hasattr(store, "get_audit_log_size") else len(store.get_all_records()) == 2


def test_audit_store_duplicate_commitment_rejection():
    store = AuditStore()
    store.append_attestation(
        record_type=AuditRecordType.DECISION_ATTESTATION,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="comm-duplicate",
    )

    with pytest.raises(AuditReplayException, match="Replayed attestation commitment"):
        store.append_attestation(
            record_type=AuditRecordType.DECISION_ATTESTATION,
            source_phase="PHASE_6_DECISION",
            classification="EVALUATION_PASS",
            policy_version="6.0.0",
            attestation_commitment="comm-duplicate",
        )


def test_audit_store_duplicate_record_id_rejection():
    store = AuditStore()
    store.append_attestation(
        record_type=AuditRecordType.DECISION_ATTESTATION,
        source_phase="PHASE_6_DECISION",
        classification="EVALUATION_PASS",
        policy_version="6.0.0",
        attestation_commitment="comm-1",
        custom_record_id="aud-unique",
    )

    with pytest.raises(AuditReplayException, match="Replayed audit record ID"):
        store.append_attestation(
            record_type=AuditRecordType.DECISION_ATTESTATION,
            source_phase="PHASE_6_DECISION",
            classification="EVALUATION_PASS",
            policy_version="6.0.0",
            attestation_commitment="comm-2",
            custom_record_id="aud-unique",
        )


def test_audit_store_concurrent_append_thread_safety():
    store = AuditStore()

    def append_worker(idx: int):
        return store.append_attestation(
            record_type=AuditRecordType.DECISION_ATTESTATION,
            source_phase="PHASE_6_DECISION",
            classification="EVALUATION_PASS",
            policy_version="6.0.0",
            attestation_commitment=f"comm-worker-{idx}",
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(append_worker, i) for i in range(20)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(store.get_all_records()) == 21  # 1 genesis + 20 appends
    res_integrity = store.verify_store_integrity()
    assert res_integrity.is_valid is True
    assert res_integrity.total_records_checked == 21

"""
Tests for Phase 8 Reconciliation Integrity & Commitment Functions.
"""

import time
from src.security_substrate.reconciliation_integrity import (
    compute_result_commitment,
    compute_snapshot_digest,
    serialize_reconciliation_snapshot,
    verify_result_commitment,
    verify_snapshot_digest,
)
from src.security_substrate.reconciliation_models import (
    ReconciliationFinding,
    ReconciliationReasonCode,
    ReconciliationResult,
    ReconciliationSnapshot,
    ReconciliationSource,
    ReconciliationStatus,
)


def test_snapshot_canonical_serialization_determinism():
    snap1 = ReconciliationSnapshot(
        snapshot_id="snap-200",
        system_id="sys-01",
        correlation_id="corr-200",
        timestamp=100000.0,
        evidence_records=[{"b": 2, "a": 1}],
        metadata={"z": 1, "m": 2},
    )
    snap2 = ReconciliationSnapshot(
        snapshot_id="snap-200",
        system_id="sys-01",
        correlation_id="corr-200",
        timestamp=100000.0,
        evidence_records=[{"a": 1, "b": 2}],
        metadata={"m": 2, "z": 1},
    )

    ser1 = serialize_reconciliation_snapshot(snap1)
    ser2 = serialize_reconciliation_snapshot(snap2)
    assert ser1 == ser2
    assert compute_snapshot_digest(snap1) == compute_snapshot_digest(snap2)


def test_snapshot_digest_verification():
    snap = ReconciliationSnapshot(
        snapshot_id="snap-201",
        system_id="sys-01",
        correlation_id="corr-201",
        timestamp=100001.0,
    )
    digest = compute_snapshot_digest(snap)
    assert verify_snapshot_digest(snap, digest) is True
    assert verify_snapshot_digest(snap, "bad" + digest[3:]) is False


def test_result_commitment_verification():
    finding = ReconciliationFinding(
        finding_id="fnd-1",
        source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
        reason_code=ReconciliationReasonCode.ALL_RECORDS_CONSISTENT,
        description="All good",
    )
    findings_dicts = [finding.to_dict()]
    digest = "a" * 64

    commitment = compute_result_commitment(
        result_id="res-200",
        snapshot_digest=digest,
        status_str=ReconciliationStatus.CONSISTENT.value,
        system_id="sys-01",
        correlation_id="corr-200",
        findings_dicts=findings_dicts,
    )

    result = ReconciliationResult(
        result_id="res-200",
        snapshot_id="snap-200",
        system_id="sys-01",
        correlation_id="corr-200",
        status=ReconciliationStatus.CONSISTENT,
        timestamp=100002.0,
        findings=[finding],
        snapshot_digest=digest,
        result_commitment=commitment,
    )

    assert verify_result_commitment(result) is True


def test_result_tampered_commitment_rejected():
    finding = ReconciliationFinding(
        finding_id="fnd-1",
        source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
        reason_code=ReconciliationReasonCode.ALL_RECORDS_CONSISTENT,
        description="All good",
    )

    result = ReconciliationResult(
        result_id="res-201",
        snapshot_id="snap-201",
        system_id="sys-01",
        correlation_id="corr-201",
        status=ReconciliationStatus.CONSISTENT,
        timestamp=100003.0,
        findings=[finding],
        snapshot_digest="a" * 64,
        result_commitment="f" * 64,  # Bad commitment
    )

    assert verify_result_commitment(result) is False

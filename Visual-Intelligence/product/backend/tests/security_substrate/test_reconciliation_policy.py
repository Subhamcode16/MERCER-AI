"""
Tests for Phase 8 Reconciliation Policy Engine.
"""

import time
from src.security_substrate.reconciliation_models import (
    ReconciliationReasonCode,
    ReconciliationSnapshot,
    ReconciliationStatus,
)
from src.security_substrate.reconciliation_policy import ReconciliationPolicy


def test_policy_consistent_records():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-100",
        system_id="sys-01",
        correlation_id="corr-100",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-1", "system_id": "sys-01", "correlation_id": "corr-100", "lifecycle_status": "VALIDATED"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-01", "correlation_id": "corr-100", "classification": "VALIDATED_VERDICT"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-100"}],
        audit_records=[{"record_id": "aud-1", "system_id": "sys-01", "correlation_id": "corr-100", "chain_valid": True}],
    )

    status, findings = policy.evaluate(snapshot)
    assert status == ReconciliationStatus.CONSISTENT
    assert any(f.reason_code == ReconciliationReasonCode.ALL_RECORDS_CONSISTENT for f in findings)


def test_policy_missing_records():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-101",
        system_id="sys-01",
        correlation_id="corr-101",
        timestamp=time.time(),
        evidence_records=[],
        decision_records=[],
        attestation_records=[],
    )

    status, findings = policy.evaluate(snapshot)
    assert status == ReconciliationStatus.INCOMPLETE
    reasons = {f.reason_code for f in findings}
    assert ReconciliationReasonCode.EVIDENCE_MISSING in reasons
    assert ReconciliationReasonCode.DECISION_MISSING in reasons
    assert ReconciliationReasonCode.ATTESTATION_MISSING in reasons


def test_policy_quarantined_evidence():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-102",
        system_id="sys-01",
        correlation_id="corr-102",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-q", "system_id": "sys-01", "correlation_id": "corr-102", "lifecycle_status": "QUARANTINED"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-01", "correlation_id": "corr-102"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-102"}],
    )

    status, findings = policy.evaluate(snapshot)
    assert status == ReconciliationStatus.QUARANTINED
    assert any(f.reason_code == ReconciliationReasonCode.QUARANTINED_RECORD for f in findings)


def test_policy_classification_conflict():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-103",
        system_id="sys-01",
        correlation_id="corr-103",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-rej", "system_id": "sys-01", "correlation_id": "corr-103", "lifecycle_status": "REJECTED"}],
        decision_records=[{"decision_id": "dec-val", "system_id": "sys-01", "correlation_id": "corr-103", "classification": "VALIDATED_VERDICT"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-103"}],
    )

    status, findings = policy.evaluate(snapshot)
    assert status == ReconciliationStatus.CONFLICT
    assert any(f.reason_code == ReconciliationReasonCode.CLASSIFICATION_CONFLICT for f in findings)


def test_policy_audit_integrity_failure():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-104",
        system_id="sys-01",
        correlation_id="corr-104",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-1", "system_id": "sys-01", "correlation_id": "corr-104"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-01", "correlation_id": "corr-104"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-104"}],
        audit_records=[{"record_id": "aud-bad", "system_id": "sys-01", "correlation_id": "corr-104", "chain_valid": False}],
    )

    status, findings = policy.evaluate(snapshot)
    assert status == ReconciliationStatus.INCONSISTENT
    assert any(f.reason_code == ReconciliationReasonCode.AUDIT_INTEGRITY_FAILURE for f in findings)


def test_policy_provenance_mismatch():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-105",
        system_id="sys-01",
        correlation_id="corr-105",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-1", "system_id": "sys-OTHER", "correlation_id": "corr-105"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-01", "correlation_id": "corr-105"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-105"}],
    )

    status, findings = policy.evaluate(snapshot)
    assert status == ReconciliationStatus.INCONSISTENT
    assert any(f.reason_code == ReconciliationReasonCode.PROVENANCE_MISMATCH for f in findings)


def test_policy_research_records_preserved():
    policy = ReconciliationPolicy()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-106",
        system_id="sys-01",
        correlation_id="corr-106",
        timestamp=time.time(),
        research_records=[{"record_id": "res-frost-1", "system_id": "sys-01", "correlation_id": "corr-106"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-01", "correlation_id": "corr-106"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-106"}],
    )

    status, findings = policy.evaluate(snapshot)
    assert any(f.reason_code == ReconciliationReasonCode.RESEARCH_BOUND_ONLY for f in findings)
    research_finding = next(f for f in findings if f.reason_code == ReconciliationReasonCode.RESEARCH_BOUND_ONLY)
    assert research_finding.metadata.get("trust_marker") == "TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION"

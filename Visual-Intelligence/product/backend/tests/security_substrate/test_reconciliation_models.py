"""
Tests for Phase 8 Reconciliation Data Models.
"""

import time
import pytest
from src.security_substrate.exceptions import ReconciliationSchemaException
from src.security_substrate.reconciliation_models import (
    ReconciliationFinding,
    ReconciliationReasonCode,
    ReconciliationResult,
    ReconciliationSnapshot,
    ReconciliationSource,
    ReconciliationStatus,
)


def test_reconciliation_finding_valid():
    finding = ReconciliationFinding(
        finding_id="fnd-001",
        source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
        reason_code=ReconciliationReasonCode.QUARANTINED_RECORD,
        description="Quarantined evidence item",
        affected_record_ids=["ev-100"],
        metadata={"note": "test"},
    )
    assert finding.finding_id == "fnd-001"
    assert finding.source == ReconciliationSource.EVIDENCE_ORCHESTRATOR
    assert finding.reason_code == ReconciliationReasonCode.QUARANTINED_RECORD
    d = finding.to_dict()
    assert d["finding_id"] == "fnd-001"
    assert d["source"] == "EVIDENCE_ORCHESTRATOR"
    assert d["reason_code"] == "QUARANTINED_RECORD"


def test_reconciliation_finding_type_confusion_rejection():
    with pytest.raises(ReconciliationSchemaException, match="must be a string"):
        ReconciliationFinding(
            finding_id=True,  # Bool confusion
            source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
            reason_code=ReconciliationReasonCode.QUARANTINED_RECORD,
            description="Valid description",
        )


def test_reconciliation_finding_empty_id_rejection():
    with pytest.raises(ReconciliationSchemaException, match="cannot be empty"):
        ReconciliationFinding(
            finding_id="   ",
            source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
            reason_code=ReconciliationReasonCode.QUARANTINED_RECORD,
            description="Valid description",
        )


def test_reconciliation_finding_sensitive_key_rejection():
    with pytest.raises(ReconciliationSchemaException, match="Prohibited sensitive key"):
        ReconciliationFinding(
            finding_id="fnd-002",
            source=ReconciliationSource.DECISION_ENGINE,
            reason_code=ReconciliationReasonCode.CLASSIFICATION_CONFLICT,
            description="Test finding",
            metadata={"user_private_key": "12345"},
        )


def test_reconciliation_snapshot_valid():
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-001",
        system_id="sys-prod-01",
        correlation_id="corr-abc-123",
        timestamp=time.time(),
        evidence_records=[{"record_id": "ev-1", "system_id": "sys-prod-01", "correlation_id": "corr-abc-123"}],
        metadata={"env": "test"},
    )
    assert snapshot.snapshot_id == "snap-001"
    assert snapshot.system_id == "sys-prod-01"
    d = snapshot.to_dict()
    assert d["snapshot_id"] == "snap-001"


def test_reconciliation_snapshot_sensitive_key_in_payload():
    with pytest.raises(ReconciliationSchemaException, match="Prohibited sensitive key"):
        ReconciliationSnapshot(
            snapshot_id="snap-002",
            system_id="sys-prod-01",
            correlation_id="corr-abc-123",
            timestamp=time.time(),
            evidence_records=[{"record_id": "ev-1", "secret_hmac_key": "bad_data"}],
        )


def test_reconciliation_result_non_authoritative():
    result = ReconciliationResult(
        result_id="rec-res-001",
        snapshot_id="snap-001",
        system_id="sys-prod-01",
        correlation_id="corr-abc-123",
        status=ReconciliationStatus.CONSISTENT,
        timestamp=time.time(),
        snapshot_digest="a" * 64,
        result_commitment="b" * 64,
    )
    assert result.is_authoritative is False
    assert result.trust_marker == "NON_AUTHORITATIVE_RECONCILIATION_VIEW"
    d = result.to_dict()
    assert d["is_authoritative"] is False
    assert d["trust_marker"] == "NON_AUTHORITATIVE_RECONCILIATION_VIEW"

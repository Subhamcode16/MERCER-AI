"""
Tests for Phase 7 SecurityAuditBoundary ingestion and query functionality.
"""

import time
import pytest
from security_substrate import (
    SecurityAuditBoundary,
    AttestationRecord,
    DecisionClassification,
    AuditRecordType,
    AuditQuery,
    AuditSchemaException,
)


def make_attestation(
    attestation_id: str,
    classification: DecisionClassification = DecisionClassification.EVALUATION_PASS,
    is_research: bool = False,
) -> AttestationRecord:
    return AttestationRecord(
        attestation_id=attestation_id,
        decision_id=f"dec-{attestation_id}",
        decision_commitment=f"comm-{attestation_id}",
        policy_version="6.0.0",
        classification=classification,
        attestation_timestamp=time.time(),
        attestation_nonce=f"nonce-{attestation_id}",
        evidence_commitments=["ev-comm-1"],
        is_research_only=is_research,
    )


def test_audit_boundary_record_attestation_pass():
    boundary = SecurityAuditBoundary()
    att = make_attestation("att-1")
    rec = boundary.record_attestation(att)

    assert rec.record_type == AuditRecordType.DECISION_ATTESTATION
    assert rec.attestation_commitment == "comm-att-1"
    assert boundary.verify_audit_integrity().is_valid is True


def test_audit_boundary_record_research_attestation():
    boundary = SecurityAuditBoundary()
    att = make_attestation("att-res-1", classification=DecisionClassification.RESEARCH_ONLY, is_research=True)
    rec = boundary.record_attestation(att)

    assert rec.record_type == AuditRecordType.RESEARCH_ATTESTATION
    assert rec.metadata["is_research_only"] is True


def test_audit_boundary_query_filtering():
    boundary = SecurityAuditBoundary()
    boundary.record_attestation(make_attestation("att-1"))
    boundary.record_attestation(make_attestation("att-res-1", classification=DecisionClassification.RESEARCH_ONLY, is_research=True))

    q_research = AuditQuery(record_type=AuditRecordType.RESEARCH_ATTESTATION)
    res_research = boundary.query_audit_trail(q_research)
    assert len(res_research) == 1
    assert res_research[0].metadata["attestation_id"] == "att-res-1"


def test_audit_boundary_has_no_execution_or_authorization_methods():
    boundary = SecurityAuditBoundary()
    for method in ["authorize", "unlock", "execute", "grant_access", "verify_for_execution", "set_verified"]:
        assert not hasattr(boundary, method), f"SecurityAuditBoundary must not possess method: {method}"

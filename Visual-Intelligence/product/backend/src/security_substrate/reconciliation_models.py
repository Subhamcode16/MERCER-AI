"""
Reconciliation Data Models for the Visual Intelligence Security Substrate (Phase 8).

Defines read-only models for constructing deterministic reconciliation snapshots,
evaluating findings, and expressing non-authoritative consistency results.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .exceptions import ReconciliationSchemaException

SENSITIVE_KEY_SUBSTRINGS = {
    "private_key",
    "secret",
    "hmac_key",
    "signing_key",
    "seed",
    "passphrase",
    "raw_bytes",
    "token_secret",
}


def _validate_non_empty_str(val: Any, name: str) -> None:
    if isinstance(val, bool) or not isinstance(val, str):
        raise ReconciliationSchemaException(f"Field '{name}' must be a string, got {type(val).__name__}.")
    if not val.strip():
        raise ReconciliationSchemaException(f"Field '{name}' cannot be empty or whitespace-only.")


def _validate_non_negative_number(val: Any, name: str) -> None:
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ReconciliationSchemaException(f"Field '{name}' must be a numeric value, got {type(val).__name__}.")
    if val < 0:
        raise ReconciliationSchemaException(f"Field '{name}' cannot be negative, got {val}.")


def _check_sensitive_keys(data: Any, path: str = "") -> None:
    """Recursively inspect dictionaries and lists for prohibited sensitive keys."""
    if isinstance(data, dict):
        for k, v in data.items():
            current_path = f"{path}.{k}" if path else str(k)
            k_lower = str(k).lower()
            for sensitive_term in SENSITIVE_KEY_SUBSTRINGS:
                if sensitive_term in k_lower:
                    raise ReconciliationSchemaException(
                        f"Prohibited sensitive key detected at '{current_path}': '{k}' contains '{sensitive_term}'."
                    )
            _check_sensitive_keys(v, current_path)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            _check_sensitive_keys(item, f"{path}[{idx}]")


class ReconciliationStatus(str, Enum):
    """Execution status of security record reconciliation."""
    CONSISTENT = "CONSISTENT"
    INCONSISTENT = "INCONSISTENT"
    CONFLICT = "CONFLICT"
    INCOMPLETE = "INCOMPLETE"
    QUARANTINED = "QUARANTINED"


class ReconciliationReasonCode(str, Enum):
    """Specific diagnostic reason codes for reconciliation findings."""
    ALL_RECORDS_CONSISTENT = "ALL_RECORDS_CONSISTENT"
    EVIDENCE_MISSING = "EVIDENCE_MISSING"
    DECISION_MISSING = "DECISION_MISSING"
    ATTESTATION_MISSING = "ATTESTATION_MISSING"
    AUDIT_INTEGRITY_FAILURE = "AUDIT_INTEGRITY_FAILURE"
    CLASSIFICATION_CONFLICT = "CLASSIFICATION_CONFLICT"
    PROVENANCE_MISMATCH = "PROVENANCE_MISMATCH"
    EXPIRED_RECORD = "EXPIRED_RECORD"
    QUARANTINED_RECORD = "QUARANTINED_RECORD"
    REFERENCE_MISMATCH = "REFERENCE_MISMATCH"
    RESEARCH_BOUND_ONLY = "RESEARCH_BOUND_ONLY"
    SCHEMA_VALIDATION_ERROR = "SCHEMA_VALIDATION_ERROR"


class ReconciliationSource(str, Enum):
    """Identifies the origin subsystem of a reconciled record."""
    ASSURANCE_LOOP = "ASSURANCE_LOOP"
    VERIFICATION_HARNESS = "VERIFICATION_HARNESS"
    RECOVERY_MANAGER = "RECOVERY_MANAGER"
    FROST_PROTOTYPE = "FROST_PROTOTYPE"
    EVIDENCE_ORCHESTRATOR = "EVIDENCE_ORCHESTRATOR"
    DECISION_ENGINE = "DECISION_ENGINE"
    AUDIT_BOUNDARY = "AUDIT_BOUNDARY"


@dataclass(frozen=True)
class ReconciliationFinding:
    """Individual consistency finding detected during record reconciliation."""
    finding_id: str
    source: ReconciliationSource
    reason_code: ReconciliationReasonCode
    description: str
    affected_record_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.finding_id, "finding_id")
        if not isinstance(self.source, ReconciliationSource):
            raise ReconciliationSchemaException(f"Invalid source: {self.source}")
        if not isinstance(self.reason_code, ReconciliationReasonCode):
            raise ReconciliationSchemaException(f"Invalid reason_code: {self.reason_code}")
        _validate_non_empty_str(self.description, "description")
        
        if not isinstance(self.affected_record_ids, list):
            raise ReconciliationSchemaException("affected_record_ids must be a list of strings.")
        for idx, rec_id in enumerate(self.affected_record_ids):
            _validate_non_empty_str(rec_id, f"affected_record_ids[{idx}]")
            
        if not isinstance(self.metadata, dict):
            raise ReconciliationSchemaException("metadata must be a dictionary.")
        _check_sensitive_keys(self.metadata, "metadata")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "source": self.source.value,
            "reason_code": self.reason_code.value,
            "description": self.description,
            "affected_record_ids": list(sorted(self.affected_record_ids)),
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class ReconciliationSnapshot:
    """Immutable collection of pre-fetched security records across Phases 1-7."""
    snapshot_id: str
    system_id: str
    correlation_id: str
    timestamp: float
    evidence_records: List[Dict[str, Any]] = field(default_factory=list)
    decision_records: List[Dict[str, Any]] = field(default_factory=list)
    attestation_records: List[Dict[str, Any]] = field(default_factory=list)
    audit_records: List[Dict[str, Any]] = field(default_factory=list)
    recovery_records: List[Dict[str, Any]] = field(default_factory=list)
    research_records: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.snapshot_id, "snapshot_id")
        _validate_non_empty_str(self.system_id, "system_id")
        _validate_non_empty_str(self.correlation_id, "correlation_id")
        _validate_non_negative_number(self.timestamp, "timestamp")

        for name, record_list in [
            ("evidence_records", self.evidence_records),
            ("decision_records", self.decision_records),
            ("attestation_records", self.attestation_records),
            ("audit_records", self.audit_records),
            ("recovery_records", self.recovery_records),
            ("research_records", self.research_records),
        ]:
            if not isinstance(record_list, list):
                raise ReconciliationSchemaException(f"{name} must be a list of dicts.")
            for idx, item in enumerate(record_list):
                if not isinstance(item, dict):
                    raise ReconciliationSchemaException(f"{name}[{idx}] must be a dictionary.")
                _check_sensitive_keys(item, f"{name}[{idx}]")

        if not isinstance(self.metadata, dict):
            raise ReconciliationSchemaException("metadata must be a dictionary.")
        _check_sensitive_keys(self.metadata, "metadata")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "system_id": self.system_id,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp,
            "evidence_records": self.evidence_records,
            "decision_records": self.decision_records,
            "attestation_records": self.attestation_records,
            "audit_records": self.audit_records,
            "recovery_records": self.recovery_records,
            "research_records": self.research_records,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class ReconciliationResult:
    """Non-authoritative result summarizing security record consistency."""
    result_id: str
    snapshot_id: str
    system_id: str
    correlation_id: str
    status: ReconciliationStatus
    timestamp: float
    findings: List[ReconciliationFinding] = field(default_factory=list)
    snapshot_digest: str = ""
    result_commitment: str = ""
    is_authoritative: bool = field(default=False, init=False)
    trust_marker: str = field(default="NON_AUTHORITATIVE_RECONCILIATION_VIEW", init=False)

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.result_id, "result_id")
        _validate_non_empty_str(self.snapshot_id, "snapshot_id")
        _validate_non_empty_str(self.system_id, "system_id")
        _validate_non_empty_str(self.correlation_id, "correlation_id")
        if not isinstance(self.status, ReconciliationStatus):
            raise ReconciliationSchemaException(f"Invalid status: {self.status}")
        _validate_non_negative_number(self.timestamp, "timestamp")
        _validate_non_empty_str(self.snapshot_digest, "snapshot_digest")
        _validate_non_empty_str(self.result_commitment, "result_commitment")

        if not isinstance(self.findings, list):
            raise ReconciliationSchemaException("findings must be a list of ReconciliationFinding objects.")
        for idx, finding in enumerate(self.findings):
            if not isinstance(finding, ReconciliationFinding):
                raise ReconciliationSchemaException(f"findings[{idx}] must be a ReconciliationFinding instance.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "snapshot_id": self.snapshot_id,
            "system_id": self.system_id,
            "correlation_id": self.correlation_id,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "findings": [f.to_dict() for f in sorted(self.findings, key=lambda x: x.finding_id)],
            "snapshot_digest": self.snapshot_digest,
            "result_commitment": self.result_commitment,
            "is_authoritative": False,
            "trust_marker": "NON_AUTHORITATIVE_RECONCILIATION_VIEW",
        }

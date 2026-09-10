"""
IF-AUDIT-001 Phase 7 Security Audit & Integrity Data Models.
Defines append-only audit log entry structures, query models, and integrity check results.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from .exceptions import AuditSchemaException

BANNED_AUTHORIZATION_TERMS = {"AUTHORIZED", "AUTHORIZATION", "PERMITTED", "UNLOCKED", "EXECUTE"}


class AuditRecordType(str, Enum):
    """
    Categorizes the origin and type of audited event records.
    """
    GENESIS_RECORD = "GENESIS_RECORD"
    DECISION_ATTESTATION = "DECISION_ATTESTATION"
    RESEARCH_ATTESTATION = "RESEARCH_ATTESTATION"


class AuditRecordStatus(str, Enum):
    """
    Lifecycle status tracking for audit records.
    Explicitly decoupled from authorization or runtime execution permission.
    """
    RECORDED = "RECORDED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    FLAGGED = "FLAGGED"


@dataclass
class AuditRecord:
    """
    Immutable, cryptographically chained audit record container.
    Guarantees structural schema compliance and non-trust metadata tracking.
    """
    record_id: str
    sequence_number: int
    record_type: AuditRecordType
    created_at: float
    source_phase: str
    classification: str
    policy_version: str
    attestation_commitment: str
    previous_record_hash: str
    record_hash: str
    status: AuditRecordStatus
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # 1. Reject boolean type confusion for non-bool scalar fields
        scalar_checks = [
            ("record_id", self.record_id),
            ("sequence_number", self.sequence_number),
            ("created_at", self.created_at),
            ("source_phase", self.source_phase),
            ("classification", self.classification),
            ("policy_version", self.policy_version),
            ("attestation_commitment", self.attestation_commitment),
            ("previous_record_hash", self.previous_record_hash),
            ("record_hash", self.record_hash),
        ]
        for name, val in scalar_checks:
            if isinstance(val, bool):
                raise AuditSchemaException(f"Boolean type confusion not permitted for field: {name}")

        # 2. Reject empty or whitespace-only strings
        str_checks = [
            ("record_id", self.record_id),
            ("source_phase", self.source_phase),
            ("classification", self.classification),
            ("policy_version", self.policy_version),
            ("attestation_commitment", self.attestation_commitment),
            ("previous_record_hash", self.previous_record_hash),
            ("record_hash", self.record_hash),
        ]
        for name, val in str_checks:
            if not isinstance(val, str) or not val.strip():
                raise AuditSchemaException(f"Field {name} must be a non-empty string")

        # 3. Reject negative sequence numbers
        if not isinstance(self.sequence_number, int) or self.sequence_number < 0:
            raise AuditSchemaException("sequence_number must be a non-negative integer")

        # 4. Timestamp validation
        if not isinstance(self.created_at, (int, float)) or self.created_at <= 0:
            raise AuditSchemaException("created_at must be a positive number")
        if self.created_at > time.time() + 5.0:
            raise AuditSchemaException("created_at cannot be in the future (> now + 5.0s)")

        # 5. Check record_type enum
        if not isinstance(self.record_type, AuditRecordType):
            if isinstance(self.record_type, str):
                try:
                    self.record_type = AuditRecordType(self.record_type.upper().strip())
                except ValueError:
                    raise AuditSchemaException(f"Invalid AuditRecordType: {self.record_type}")
            else:
                raise AuditSchemaException("record_type must be an AuditRecordType enum")

        # 6. Check status enum
        if not isinstance(self.status, AuditRecordStatus):
            if isinstance(self.status, str):
                try:
                    self.status = AuditRecordStatus(self.status.upper().strip())
                except ValueError:
                    raise AuditSchemaException(f"Invalid AuditRecordStatus: {self.status}")
            else:
                raise AuditSchemaException("status must be an AuditRecordStatus enum")

        # 7. Check for forbidden classification terms
        upper_class = str(self.classification).upper().strip()
        if upper_class in BANNED_AUTHORIZATION_TERMS:
            raise AuditSchemaException(f"Forbidden classification term '{upper_class}' in AuditRecord")


@dataclass
class AuditIntegrityResult:
    """
    Result artifact produced by chain integrity verification operations.
    """
    is_valid: bool
    total_records_checked: int
    last_valid_sequence: int
    violation_sequence: Optional[int] = None
    violation_reason: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.is_valid, bool):
            raise AuditSchemaException("is_valid must be a boolean")
        if isinstance(self.total_records_checked, bool) or not isinstance(self.total_records_checked, int) or self.total_records_checked < 0:
            raise AuditSchemaException("total_records_checked must be a non-negative integer")
        if isinstance(self.last_valid_sequence, bool) or not isinstance(self.last_valid_sequence, int) or self.last_valid_sequence < -1:
            raise AuditSchemaException("last_valid_sequence must be an integer >= -1")


@dataclass
class AuditQuery:
    """
    Query filter specification for audit record retrieval.
    """
    record_type: Optional[AuditRecordType] = None
    source_phase: Optional[str] = None
    classification: Optional[str] = None
    policy_version: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    limit: int = 1000

    def __post_init__(self):
        if isinstance(self.limit, bool) or not isinstance(self.limit, int) or self.limit <= 0:
            raise AuditSchemaException("limit must be a positive integer")


@dataclass
class AuditSequenceMetadata:
    """
    Summary metadata describing the current state of the audit hash chain.
    """
    total_records: int
    latest_sequence_number: int
    latest_record_hash: str
    genesis_record_hash: str

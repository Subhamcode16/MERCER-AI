"""
IF-INTEGRITY-001 Phase 7 Cryptographic Audit Hash Chaining & Verification.
Computes SHA-256 record commitments, previous-record hash links, and verifies chain integrity.
"""

import hmac
import hashlib
import json
import time
from typing import List, Optional

from .audit_models import (
    AuditRecord,
    AuditRecordType,
    AuditRecordStatus,
    AuditIntegrityResult,
)
from .exceptions import AuditIntegrityException, AuditSchemaException

GENESIS_RECORD_ID = "audit-genesis-000"
GENESIS_PREVIOUS_HASH = "0" * 64
GENESIS_COMMITMENT = "0" * 64


def canonicalize_audit_payload(
    record_id: str,
    sequence_number: int,
    record_type: str,
    created_at: float,
    source_phase: str,
    classification: str,
    policy_version: str,
    attestation_commitment: str,
    previous_record_hash: str,
    status: str,
) -> str:
    """
    Produces a canonical JSON string representation of audit record fields for hashing.
    """
    canonical_obj = {
        "attestation_commitment": attestation_commitment,
        "classification": classification,
        "created_at": created_at,
        "policy_version": policy_version,
        "previous_record_hash": previous_record_hash,
        "record_id": record_id,
        "record_type": record_type,
        "sequence_number": sequence_number,
        "source_phase": source_phase,
        "status": status,
    }
    return json.dumps(canonical_obj, sort_keys=True, separators=(",", ":"))


def compute_record_hash(
    record_id: str,
    sequence_number: int,
    record_type: str,
    created_at: float,
    source_phase: str,
    classification: str,
    policy_version: str,
    attestation_commitment: str,
    previous_record_hash: str,
    status: str,
) -> str:
    """
    Computes SHA-256 commitment hash over canonical audit record payload.
    """
    canonical_str = canonicalize_audit_payload(
        record_id=record_id,
        sequence_number=sequence_number,
        record_type=record_type,
        created_at=created_at,
        source_phase=source_phase,
        classification=classification,
        policy_version=policy_version,
        attestation_commitment=attestation_commitment,
        previous_record_hash=previous_record_hash,
        status=status,
    )
    return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()


def compute_record_hash_from_record(record: AuditRecord) -> str:
    """
    Helper computing SHA-256 hash directly from an AuditRecord instance.
    """
    return compute_record_hash(
        record_id=record.record_id,
        sequence_number=record.sequence_number,
        record_type=record.record_type.value,
        created_at=record.created_at,
        source_phase=record.source_phase,
        classification=record.classification,
        policy_version=record.policy_version,
        attestation_commitment=record.attestation_commitment,
        previous_record_hash=record.previous_record_hash,
        status=record.status.value,
    )


def create_genesis_record(creation_time: Optional[float] = None) -> AuditRecord:
    """
    Creates sequence 0 deterministic genesis audit record.
    """
    now = creation_time if creation_time is not None else time.time()
    rec_hash = compute_record_hash(
        record_id=GENESIS_RECORD_ID,
        sequence_number=0,
        record_type=AuditRecordType.GENESIS_RECORD.value,
        created_at=now,
        source_phase="PHASE_7_GENESIS",
        classification="GENESIS",
        policy_version="7.0.0",
        attestation_commitment=GENESIS_COMMITMENT,
        previous_record_hash=GENESIS_PREVIOUS_HASH,
        status=AuditRecordStatus.RECORDED.value,
    )

    return AuditRecord(
        record_id=GENESIS_RECORD_ID,
        sequence_number=0,
        record_type=AuditRecordType.GENESIS_RECORD,
        created_at=now,
        source_phase="PHASE_7_GENESIS",
        classification="GENESIS",
        policy_version="7.0.0",
        attestation_commitment=GENESIS_COMMITMENT,
        previous_record_hash=GENESIS_PREVIOUS_HASH,
        record_hash=rec_hash,
        status=AuditRecordStatus.RECORDED,
        metadata={"genesis": True},
    )


def verify_record_integrity(record: AuditRecord) -> bool:
    """
    Verifies that an AuditRecord's recorded_hash matches its recomputed hash.
    Constant-time comparison.
    """
    if not isinstance(record, AuditRecord):
        raise AuditSchemaException("record must be an AuditRecord instance")

    expected_hash = compute_record_hash_from_record(record)
    return hmac.compare_digest(record.record_hash, expected_hash)


def verify_chain_integrity(records: List[AuditRecord]) -> AuditIntegrityResult:
    """
    Verifies complete audit log hash chain integrity across a sequence of records.
    Verifies:
      1. Monotonic sequence numbering starting from 0.
      2. Record hash self-consistency (verify_record_integrity).
      3. Hash link consistency (previous_record_hash == records[i-1].record_hash).
    Returns AuditIntegrityResult.
    """
    if not isinstance(records, list):
        raise AuditSchemaException("records must be a list of AuditRecord instances")

    if len(records) == 0:
        return AuditIntegrityResult(
            is_valid=True,
            total_records_checked=0,
            last_valid_sequence=-1,
        )

    last_valid_seq = -1

    for idx, rec in enumerate(records):
        if not isinstance(rec, AuditRecord):
            return AuditIntegrityResult(
                is_valid=False,
                total_records_checked=idx,
                last_valid_sequence=last_valid_seq,
                violation_sequence=idx,
                violation_reason=f"Non-AuditRecord object encountered at index {idx}",
            )

        # Sequence continuity check
        expected_seq = idx
        if rec.sequence_number != expected_seq:
            return AuditIntegrityResult(
                is_valid=False,
                total_records_checked=idx,
                last_valid_sequence=last_valid_seq,
                violation_sequence=rec.sequence_number,
                violation_reason=f"Sequence gap/discontinuity: expected {expected_seq}, got {rec.sequence_number}",
            )

        # Record hash verification
        if not verify_record_integrity(rec):
            return AuditIntegrityResult(
                is_valid=False,
                total_records_checked=idx,
                last_valid_sequence=last_valid_seq,
                violation_sequence=rec.sequence_number,
                violation_reason=f"Record hash tampered/mismatched at sequence {rec.sequence_number}",
            )

        # Hash link verification
        if idx == 0:
            if rec.previous_record_hash != GENESIS_PREVIOUS_HASH:
                return AuditIntegrityResult(
                    is_valid=False,
                    total_records_checked=0,
                    last_valid_sequence=-1,
                    violation_sequence=0,
                    violation_reason="Genesis previous_record_hash does not match expected genesis anchor",
                )
        else:
            prev_rec = records[idx - 1]
            if not hmac.compare_digest(rec.previous_record_hash, prev_rec.record_hash):
                return AuditIntegrityResult(
                    is_valid=False,
                    total_records_checked=idx,
                    last_valid_sequence=last_valid_seq,
                    violation_sequence=rec.sequence_number,
                    violation_reason=f"Hash chain broken at sequence {rec.sequence_number}: previous_record_hash mismatch",
                )

        last_valid_seq = rec.sequence_number

    return AuditIntegrityResult(
        is_valid=True,
        total_records_checked=len(records),
        last_valid_sequence=last_valid_seq,
    )

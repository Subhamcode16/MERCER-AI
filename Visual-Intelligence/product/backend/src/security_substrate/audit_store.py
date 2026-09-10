"""
IF-STORE-001 Phase 7 Thread-Safe In-Memory Append-Only Audit Store.
Guarantees monotonic sequence assignment, hash link binding, and duplicate attestation replay defense.
"""

import uuid
import time
import threading
from typing import Dict, List, Optional

from .audit_models import (
    AuditRecord,
    AuditRecordType,
    AuditRecordStatus,
    AuditQuery,
    AuditIntegrityResult,
    AuditSequenceMetadata,
    AuditSchemaException,
)
from .audit_integrity import (
    create_genesis_record,
    compute_record_hash,
    verify_chain_integrity,
    GENESIS_RECORD_ID,
    GENESIS_COMMITMENT,
)
from .exceptions import AuditReplayException, AuditSequenceException, AuditIntegrityException


class AuditStore:
    """
    Process-lifetime in-memory append-only audit log store.
    Thread-safe synchronization via threading.RLock().
    Monotonic internal sequence numbering and hash chain verification.
    """
    def __init__(self, creation_time: Optional[float] = None):
        self._lock = threading.RLock()
        self._records: List[AuditRecord] = []
        self._records_by_id: Dict[str, AuditRecord] = {}
        self._records_by_commitment: Dict[str, AuditRecord] = {}

        # Automatically append Genesis Record (Seq 0)
        genesis = create_genesis_record(creation_time=creation_time)
        self._records.append(genesis)
        self._records_by_id[genesis.record_id] = genesis

    def append_attestation(
        self,
        record_type: AuditRecordType,
        source_phase: str,
        classification: str,
        policy_version: str,
        attestation_commitment: str,
        created_at: Optional[float] = None,
        metadata: Optional[dict] = None,
        custom_record_id: Optional[str] = None,
    ) -> AuditRecord:
        """
        Atomically appends an attestation audit record to the store.
        Assigns the next monotonic sequence number and binds previous record hash.
        Raises AuditReplayException if record_id or attestation_commitment is replayed.
        """
        if isinstance(source_phase, bool) or not isinstance(source_phase, str) or not source_phase.strip():
            raise AuditSchemaException("source_phase must be a non-empty string")
        if isinstance(classification, bool) or not isinstance(classification, str) or not classification.strip():
            raise AuditSchemaException("classification must be a non-empty string")
        if isinstance(policy_version, bool) or not isinstance(policy_version, str) or not policy_version.strip():
            raise AuditSchemaException("policy_version must be a non-empty string")
        if isinstance(attestation_commitment, bool) or not isinstance(attestation_commitment, str) or not attestation_commitment.strip():
            raise AuditSchemaException("attestation_commitment must be a non-empty string")

        if created_at is None:
            created_at = time.time()

        record_id = custom_record_id if custom_record_id else f"aud-{uuid.uuid4().hex[:12]}"
        if isinstance(record_id, bool) or not isinstance(record_id, str) or not record_id.strip():
            raise AuditSchemaException("record_id must be a non-empty string")

        with self._lock:
            # 1. Check duplicate record ID
            if record_id in self._records_by_id:
                raise AuditReplayException(f"Replayed audit record ID detected: {record_id}")

            # 2. Check duplicate attestation commitment (skip for genesis commitment)
            if attestation_commitment != GENESIS_COMMITMENT and attestation_commitment in self._records_by_commitment:
                raise AuditReplayException(f"Replayed attestation commitment detected: {attestation_commitment}")

            # 3. Determine next sequence number and previous hash link
            next_seq = len(self._records)
            prev_hash = self._records[-1].record_hash

            # 4. Compute record hash
            rec_hash = compute_record_hash(
                record_id=record_id,
                sequence_number=next_seq,
                record_type=record_type.value if isinstance(record_type, AuditRecordType) else str(record_type),
                created_at=created_at,
                source_phase=source_phase,
                classification=classification,
                policy_version=policy_version,
                attestation_commitment=attestation_commitment,
                previous_record_hash=prev_hash,
                status=AuditRecordStatus.RECORDED.value,
            )

            # 5. Construct AuditRecord
            record = AuditRecord(
                record_id=record_id,
                sequence_number=next_seq,
                record_type=record_type,
                created_at=created_at,
                source_phase=source_phase,
                classification=classification,
                policy_version=policy_version,
                attestation_commitment=attestation_commitment,
                previous_record_hash=prev_hash,
                record_hash=rec_hash,
                status=AuditRecordStatus.RECORDED,
                metadata=metadata if metadata is not None else {},
            )

            # 6. Append to storage
            self._records.append(record)
            self._records_by_id[record_id] = record
            if attestation_commitment != GENESIS_COMMITMENT:
                self._records_by_commitment[attestation_commitment] = record

            return record

    def get_record_by_sequence(self, sequence_number: int) -> Optional[AuditRecord]:
        """Returns an AuditRecord by sequence number or None."""
        with self._lock:
            if 0 <= sequence_number < len(self._records):
                return self._records[sequence_number]
            return None

    def get_record_by_id(self, record_id: str) -> Optional[AuditRecord]:
        """Returns an AuditRecord by record_id or None."""
        with self._lock:
            return self._records_by_id.get(record_id)

    def get_all_records(self) -> List[AuditRecord]:
        """Returns a copy of all audit records in sequence order."""
        with self._lock:
            return list(self._records)

    def query_records(self, query: AuditQuery) -> List[AuditRecord]:
        """Serves bounded audit record queries based on AuditQuery specifications."""
        if not isinstance(query, AuditQuery):
            raise AuditSchemaException("query must be an AuditQuery instance")

        with self._lock:
            results = list(self._records)
            if query.record_type:
                results = [r for r in results if r.record_type == query.record_type]
            if query.source_phase:
                results = [r for r in results if r.source_phase == query.source_phase]
            if query.classification:
                results = [r for r in results if r.classification == query.classification]
            if query.policy_version:
                results = [r for r in results if r.policy_version == query.policy_version]
            if query.start_time is not None:
                results = [r for r in results if r.created_at >= query.start_time]
            if query.end_time is not None:
                results = [r for r in results if r.created_at <= query.end_time]

            return results[: query.limit]

    def get_sequence_metadata(self) -> AuditSequenceMetadata:
        """Returns summary sequence metadata of the audit chain."""
        with self._lock:
            latest = self._records[-1]
            return AuditSequenceMetadata(
                total_records=len(self._records),
                latest_sequence_number=latest.sequence_number,
                latest_record_hash=latest.record_hash,
                genesis_record_hash=self._records[0].record_hash,
            )

    def verify_store_integrity(self) -> AuditIntegrityResult:

        """Verifies the complete hash chain integrity of the stored audit records."""
        with self._lock:
            return verify_chain_integrity(self._records)

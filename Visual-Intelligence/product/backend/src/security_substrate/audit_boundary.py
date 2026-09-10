"""
IF-BOUNDARY-001 Phase 7 Security Audit Boundary.
Ingests normalized Phase 6 attestation records into process-lifetime append-only audit log.
Explicitly carries zero execution authority, zero state mutation capabilities, and zero ExecutionGate coupling.
"""

import threading
from typing import List, Optional

from .decision_models import AttestationRecord, DecisionClassification
from .audit_models import (
    AuditRecord,
    AuditRecordType,
    AuditQuery,
    AuditIntegrityResult,
    AuditSequenceMetadata,
    AuditSchemaException,
)
from .audit_store import AuditStore
from .exceptions import AuditSchemaException


class SecurityAuditBoundary:
    """
    Public entry point for recording security decision attestations into the append-only audit log.
    Provides integrity verification and filtered query capabilities.
    Explicitly possesses NO execution, gating, unlock, or authorization methods.
    """
    def __init__(self, store: Optional[AuditStore] = None):
        self.store = store if store is not None else AuditStore()
        self._lock = threading.RLock()

    def record_attestation(
        self,
        attestation: AttestationRecord,
        source_phase: str = "PHASE_6_DECISION",
    ) -> AuditRecord:
        """
        Ingests a Phase 6 AttestationRecord and records it in the append-only audit log.
        Preserves research/production classifications and binds hash chain.
        """
        if not isinstance(attestation, AttestationRecord):
            raise AuditSchemaException("attestation must be an AttestationRecord instance")

        with self._lock:
            # Determine record type based on research classification
            if attestation.is_research_only or attestation.classification == DecisionClassification.RESEARCH_ONLY:
                rec_type = AuditRecordType.RESEARCH_ATTESTATION
            else:
                rec_type = AuditRecordType.DECISION_ATTESTATION

            metadata = {
                "decision_id": attestation.decision_id,
                "attestation_id": attestation.attestation_id,
                "attestation_nonce": attestation.attestation_nonce,
                "is_research_only": attestation.is_research_only,
                "evidence_commitments_count": len(attestation.evidence_commitments),
            }

            return self.store.append_attestation(
                record_type=rec_type,
                source_phase=source_phase,
                classification=attestation.classification.value,
                policy_version=attestation.policy_version,
                attestation_commitment=attestation.decision_commitment,
                created_at=attestation.attestation_timestamp,
                metadata=metadata,
            )

    def verify_audit_integrity(self) -> AuditIntegrityResult:
        """
        Verifies full cryptographic hash-chain integrity across all recorded audit entries.
        """
        with self._lock:
            return self.store.verify_store_integrity()

    def query_audit_trail(self, query: AuditQuery) -> List[AuditRecord]:
        """
        Serves filtered audit log queries.
        """
        with self._lock:
            return self.store.query_records(query)

    def get_sequence_metadata(self) -> AuditSequenceMetadata:
        """
        Returns summary metadata describing current audit chain state.
        """
        with self._lock:
            return self.store.get_sequence_metadata()

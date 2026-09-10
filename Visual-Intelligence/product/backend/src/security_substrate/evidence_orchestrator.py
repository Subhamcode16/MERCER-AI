"""
IF-EVIDENCE-001 Evidence Orchestrator Boundary.
Coordinates ingestion, normalization, provenance classification, and audit logging of security evidence.
STRICTLY DECOUPLED FROM EXECUTION GATES AND STATE MUTATIONS.
HAS NO AUTHORIZE, UNLOCK, OR EXECUTION METHODS.
"""

import time
import threading
from typing import Dict, List, Optional, Any
from .evidence_models import (
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from .evidence_policy import EvidencePolicy
from .exceptions import FailClosedException, MalformedEvidenceException


class EvidenceOrchestrator:
    """
    Evidence Orchestrator Boundary.
    Provides thread-safe evidence ingestion, provenance verification, and evidence audit trail storage.
    Does NOT possess execution, authorization, recovery reset, or state-transition authority.
    """
    def __init__(self, policy: Optional[EvidencePolicy] = None):
        self._lock = threading.RLock()
        self.policy = policy or EvidencePolicy()
        self._audit_log: Dict[str, NormalizedEvidenceRecord] = {}

    def ingest_evidence(self, record: NormalizedEvidenceRecord) -> NormalizedEvidenceRecord:
        """
        Ingests and normalizes an evidence record.
        Validates record against EvidencePolicy and records it in the in-memory audit log.
        Returns the normalized record with updated status (VALIDATED, QUARANTINED, or REJECTED).
        Does NOT grant runtime authorization or unlock execution capability.
        """
        if not record or not isinstance(record, NormalizedEvidenceRecord):
            raise MalformedEvidenceException("Invalid or null evidence record submitted to EvidenceOrchestrator")

        with self._lock:
            # Set ingestion timestamp
            record.ingestion_time = time.time()
            record.status = EvidenceStatus.RECEIVED

            # Validate against policy engine
            validated_status = self.policy.validate_record(record)
            record.status = validated_status

            # Record in audit log
            self._audit_log[record.evidence_id] = record
            return record

    def get_evidence_record(self, evidence_id: str) -> Optional[NormalizedEvidenceRecord]:
        """Retrieves a normalized evidence record from the audit log by ID."""
        with self._lock:
            return self._audit_log.get(evidence_id)

    def list_evidence_records(
        self,
        classification: Optional[EvidenceClassification] = None,
        provenance: Optional[EvidenceProvenance] = None
    ) -> List[NormalizedEvidenceRecord]:
        """Lists ingested evidence records filtered by classification or provenance."""
        with self._lock:
            results = list(self._audit_log.values())
            if classification:
                results = [r for r in results if r.classification == classification]
            if provenance:
                results = [r for r in results if r.provenance == provenance]
            return results

    def get_audit_log_size(self) -> int:
        """Returns total count of ingested evidence records in audit log."""
        with self._lock:
            return len(self._audit_log)

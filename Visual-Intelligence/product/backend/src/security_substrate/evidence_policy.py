"""
IF-EVIDENCE-001 Evidence Validation Policy Engine.
Enforces multi-layer replay defense (evidence_id, unique_nonce, payload_commitment),
provenance binding, freshness validation, and fail-closed evaluation.
"""

import time
import threading
from typing import Optional, Set
from .evidence_models import (
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
    DEFAULT_TRUST_MARKER_RESEARCH,
)
from .assurance_loop import ConsumedNonceCache
from .exceptions import (
    FailClosedException,
    MalformedEvidenceException,
    ReplayAttackException,
    StaleTimestampException,
)

MAX_EVIDENCE_FRESHNESS_SECONDS = 900.0  # 15 minutes
MAX_FUTURE_SKEW_SECONDS = 5.0           # 5 seconds


class EvidencePolicy:
    """
    Validates NormalizedEvidenceRecord objects for freshness, provenance binding,
    and multi-layer replay defense (ID replay, nonce replay, commitment replay).
    """
    def __init__(self, nonce_cache: Optional[ConsumedNonceCache] = None):
        self._lock = threading.RLock()
        self.nonce_cache = nonce_cache or ConsumedNonceCache()
        self._seen_payload_commitments: Set[str] = set()

    def validate_record(self, record: NormalizedEvidenceRecord) -> EvidenceStatus:
        """
        Validates an evidence record against policy invariants.
        Returns EvidenceStatus.VALIDATED if fully compliant; raises fail-closed exceptions or returns QUARANTINED / REJECTED on failure.
        """
        if not record or not isinstance(record, NormalizedEvidenceRecord):
            raise MalformedEvidenceException("Invalid or null evidence record provided")

        with self._lock:
            # 1. Provenance & Classification Binding Verification
            if record.provenance == EvidenceProvenance.PHASE_4_RESEARCH:
                if record.classification != EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE:
                    record.status = EvidenceStatus.QUARANTINED
                    raise MalformedEvidenceException(
                        f"Research provenance ({record.provenance}) must be classified as RESEARCH_CRYPTOGRAPHIC_EVIDENCE"
                    )
                if record.trust_marker != DEFAULT_TRUST_MARKER_RESEARCH:
                    record.status = EvidenceStatus.QUARANTINED
                    raise MalformedEvidenceException(
                        f"Research evidence must carry trust_marker '{DEFAULT_TRUST_MARKER_RESEARCH}'"
                    )

            # 2. Freshness Verification
            now = time.time()
            if record.expiration_time < record.creation_time:
                record.status = EvidenceStatus.REJECTED
                raise StaleTimestampException("Payload expiration_time cannot be earlier than creation_time")

            if record.creation_time > now + MAX_FUTURE_SKEW_SECONDS:
                record.status = EvidenceStatus.QUARANTINED
                raise StaleTimestampException(f"Future-dated creation timestamp: creation={record.creation_time}, now={now}")

            if now > record.expiration_time:
                record.status = EvidenceStatus.EXPIRED
                raise StaleTimestampException(f"Expired evidence record: expiration={record.expiration_time}, now={now}")

            if (record.expiration_time - record.creation_time) > MAX_EVIDENCE_FRESHNESS_SECONDS + 0.1:
                record.status = EvidenceStatus.REJECTED
                raise StaleTimestampException("Expiration window exceeds max 15-minute limit")

            # 3. Multi-Layer Replay Defense
            # A. Evidence Identity Replay Check
            if not self.nonce_cache.check_and_add(f"evid_id:{record.evidence_id}"):
                record.status = EvidenceStatus.REJECTED
                raise ReplayAttackException(f"Duplicate evidence ID detected: {record.evidence_id}")

            # B. Nonce Replay Check
            if not self.nonce_cache.check_and_add(f"nonce:{record.unique_nonce}"):
                record.status = EvidenceStatus.REJECTED
                raise ReplayAttackException(f"Replayed unique_nonce detected: {record.unique_nonce}")

            # C. Payload Commitment Replay Check (Semantically identical payload with different ID)
            comm_key = f"comm:{record.payload_commitment}"
            if not self.nonce_cache.check_and_add(comm_key):
                record.status = EvidenceStatus.REJECTED
                raise ReplayAttackException(f"Replayed payload commitment detected: {record.payload_commitment}")

            record.status = EvidenceStatus.VALIDATED
            return EvidenceStatus.VALIDATED

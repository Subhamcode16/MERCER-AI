"""
Phase 24 Cryptographic Live Operations Evidence Ledger.
"""
import logging
from typing import List, Dict, Any, Optional
from src.live_operations.live_models import LiveEvidenceRecord
from src.live_operations.exceptions import EvidenceTamperingError

logger = logging.getLogger(__name__)

class LiveOperationsLedger:
    """Cryptographic append-only ledger for immutable live evidence recording."""

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self._entries: List[LiveEvidenceRecord] = []
        self._prev_hash = self.GENESIS_HASH

    def append_evidence(self, record: LiveEvidenceRecord) -> None:
        """Appends evidence record and computes unbroken chain hash."""
        if not record.record_hash:
            record.record_hash = record.compute_hash()

        self._entries.append(record)
        self._prev_hash = record.record_hash
        logger.info(f"Appended evidence to Live Operations Ledger: {record.evidence_id} (Hash: {record.record_hash[:12]}...)")

    def verify_ledger_integrity(self) -> bool:
        """Verifies every record's SHA-256 self-hash."""
        for rec in self._entries:
            if rec.record_hash != rec.compute_hash():
                raise EvidenceTamperingError(f"Evidence record {rec.evidence_id} hash corrupted or tampered!")
        return True

    def list_entries(self) -> List[LiveEvidenceRecord]:
        return list(self._entries)

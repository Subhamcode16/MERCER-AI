"""
Phase 23 Cryptographic Append-Only Ledger Store.
"""
import logging
from typing import Dict, Any, List, Optional
from src.persistence.storage_models import LedgerEntry
from src.persistence.exceptions import LineageBreakError

logger = logging.getLogger(__name__)

class LedgerStore:
    """Cryptographic append-only operational event ledger with hash verification."""

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self._entries: List[LedgerEntry] = []
        self._tenant_entry_map: Dict[str, List[LedgerEntry]] = {}

    def append_event(self, entry_id: str, tenant_id: str, client_id: str, event_type: str, event_data: Dict[str, Any]) -> LedgerEntry:
        """Appends an operational event into the cryptographic chain."""
        prev_hash = self.GENESIS_HASH if not self._entries else self._entries[-1].entry_hash

        entry = LedgerEntry(
            entry_id=entry_id,
            tenant_id=tenant_id,
            client_id=client_id,
            event_type=event_type,
            event_data=event_data,
            prev_entry_hash=prev_hash
        )
        entry.entry_hash = entry.compute_hash()

        self._entries.append(entry)
        if tenant_id not in self._tenant_entry_map:
            self._tenant_entry_map[tenant_id] = []
        self._tenant_entry_map[tenant_id].append(entry)

        logger.info(f"Ledger event appended: {event_type} (ID: {entry_id}, Hash: {entry.entry_hash[:12]}...)")
        return entry

    def verify_ledger_integrity(self) -> bool:
        """Verifies full cryptographic chain integrity from genesis."""
        if not self._entries:
            return True

        expected_prev_hash = self.GENESIS_HASH
        for entry in self._entries:
            if entry.prev_entry_hash != expected_prev_hash:
                raise LineageBreakError(f"Ledger entry {entry.entry_id} broken chain link! Expected {expected_prev_hash}, got {entry.prev_entry_hash}")
            if entry.entry_hash != entry.compute_hash():
                raise LineageBreakError(f"Ledger entry {entry.entry_id} content tampered!")
            expected_prev_hash = entry.entry_hash

        return True

    def list_entries_for_tenant(self, tenant_id: str) -> List[LedgerEntry]:
        return self._tenant_entry_map.get(tenant_id, [])

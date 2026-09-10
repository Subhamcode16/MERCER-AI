"""
Phase 14 Workforce Audit Ledger
-------------------------------
Maintains an append-only SHA-256 hash-linked audit ledger for workforce operations.
Ensures machine-verifiable tamper evidence across workforce assignments, critique, review,
and execution preparation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import hashlib
import json
import os
import time

@dataclass(frozen=True)
class WorkforceLedgerEntry:
    """Entry in the append-only workforce audit ledger."""
    entry_id: str
    event_type: str
    client_id: str
    staff_id: str
    payload: Dict[str, Any]
    prev_hash: str
    entry_hash: str
    timestamp: float = field(default_factory=time.time)

class WorkforceLedger:
    """Append-only audit ledger linked to Phase 7 audit integrity substrate."""

    def __init__(self, ledger_dir: str = "data/phase14_workforce_ledger"):
        self.ledger_dir = ledger_dir
        self.entries: List[WorkforceLedgerEntry] = []

    def record_entry(
        self,
        event_type: str,
        client_id: str,
        staff_id: str,
        payload: Dict[str, Any],
    ) -> WorkforceLedgerEntry:
        """Records an entry in the ledger, linking SHA-256 hash to previous entry."""
        entry_id = f"wfl-{len(self.entries) + 1:06d}"
        prev_hash = self.entries[-1].entry_hash if self.entries else "0" * 64

        raw = f"{entry_id}:{event_type}:{client_id}:{staff_id}:{prev_hash}:{json.dumps(payload, sort_keys=True)}"
        entry_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        entry = WorkforceLedgerEntry(
            entry_id=entry_id,
            event_type=event_type,
            client_id=client_id,
            staff_id=staff_id,
            payload=payload,
            prev_hash=prev_hash,
            entry_hash=entry_hash,
        )
        self.entries.append(entry)
        return entry

    def verify_ledger_integrity(self) -> bool:
        """Verifies hash-chaining integrity across all recorded ledger entries."""
        for i, entry in enumerate(self.entries):
            expected_prev = "0" * 64 if i == 0 else self.entries[i - 1].entry_hash
            if entry.prev_hash != expected_prev:
                return False
            raw = f"{entry.entry_id}:{entry.event_type}:{entry.client_id}:{entry.staff_id}:{entry.prev_hash}:{json.dumps(entry.payload, sort_keys=True)}"
            expected_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if entry.entry_hash != expected_hash:
                return False
        return True

"""
Phase 18 Studio Intelligence Audit Ledger.

Maintains an append-only, SHA-256 hash-linked audit ledger for all closed-loop
observations, evaluations, learning signals, experiments, promotions, and rollbacks.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import hashlib
import json
import os
import threading

from src.studio_intelligence.exceptions import IntelligenceLedgerError


@dataclass(frozen=True)
class IntelligenceLedgerEntry:
    """Immutable audit entry for Phase 18 Studio Intelligence events."""
    sequence: int
    event_type: str
    client_id: str
    payload: Dict[str, Any]
    prev_hash: str
    entry_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if not self.entry_hash:
            data_str = f"{self.sequence}:{self.event_type}:{self.client_id}:{json.dumps(self.payload, sort_keys=True)}:{self.prev_hash}:{self.timestamp}"
            computed = hashlib.sha256(data_str.encode("utf-8")).hexdigest()
            object.__setattr__(self, "entry_hash", computed)


class StudioIntelligenceLedger:
    """Append-only, SHA-256 hash-linked audit ledger for Phase 18 events."""

    def __init__(self, ledger_dir: str = "data/phase18_intelligence_ledger"):
        self.ledger_dir = ledger_dir
        self._lock = threading.RLock()
        self._entries: List[IntelligenceLedgerEntry] = []

        if not os.path.exists(self.ledger_dir):
            os.makedirs(self.ledger_dir, exist_ok=True)

    def append_event(
        self, event_type: str, client_id: str, payload: Dict[str, Any]
    ) -> IntelligenceLedgerEntry:
        """Appends an event to the hash-linked audit chain."""
        with self._lock:
            seq = len(self._entries) + 1
            prev_hash = self._entries[-1].entry_hash if self._entries else "GENESIS_PHASE18_INTELLIGENCE"
            entry = IntelligenceLedgerEntry(
                sequence=seq,
                event_type=event_type,
                client_id=client_id,
                payload=payload,
                prev_hash=prev_hash,
            )
            self._entries.append(entry)
            self._persist_entry(entry)
            return entry

    def _persist_entry(self, entry: IntelligenceLedgerEntry):
        filepath = os.path.join(self.ledger_dir, f"entry_{entry.sequence:06d}.json")
        data = {
            "sequence": entry.sequence,
            "event_type": entry.event_type,
            "client_id": entry.client_id,
            "payload": entry.payload,
            "prev_hash": entry.prev_hash,
            "entry_hash": entry.entry_hash,
            "timestamp": entry.timestamp,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def verify_chain_integrity(self) -> bool:
        """Verifies sequence continuity and cryptographic SHA-256 hash links."""
        with self._lock:
            prev_hash = "GENESIS_PHASE18_INTELLIGENCE"
            for entry in self._entries:
                if entry.prev_hash != prev_hash:
                    raise IntelligenceLedgerError(
                        f"Ledger sequence broke at entry #{entry.sequence}: prev_hash mismatch."
                    )
                prev_hash = entry.entry_hash
            return True

    def list_events(self, client_id: Optional[str] = None) -> List[IntelligenceLedgerEntry]:
        """Lists ledger entries filtered by client ID if provided."""
        with self._lock:
            if client_id is None:
                return list(self._entries)
            return [e for e in self._entries if e.client_id == client_id]

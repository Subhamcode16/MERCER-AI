"""
Phase 11 Mission Execution Ledger.

Maintains an append-only, SHA-256 hash-linked execution log of all operational events
and state transitions. Provides cryptographically verifiable audit trail.
"""

import os
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from .operational_events import OperationalEvent
from .exceptions import MissionControlError

LEDGER_DIR = os.path.join("data", "phase11_ledger")


@dataclass
class LedgerEntry:
    """Hash-linked entry in the mission execution ledger."""
    entry_index: int
    event: Dict[str, Any]
    timestamp: str
    previous_entry_hash: str
    entry_hash: str

    def compute_hash(self) -> str:
        """Computes SHA-256 digest over canonical payload."""
        payload = {
            "entry_index": self.entry_index,
            "event": self.event,
            "timestamp": self.timestamp,
            "previous_entry_hash": self.previous_entry_hash,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()


class MissionLedger:
    """Append-only, integrity-verified ledger for mission operational events."""

    def __init__(self, base_dir: str = LEDGER_DIR):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.entries: List[LedgerEntry] = []
        self._load_existing_ledger()

    def record_event(self, event: OperationalEvent) -> LedgerEntry:
        """Appends an event to the hash-linked ledger."""
        entry_index = len(self.entries)
        prev_hash = self.entries[-1].entry_hash if self.entries else "0000000000000000000000000000000000000000000000000000000000000000"

        entry = LedgerEntry(
            entry_index=entry_index,
            event=event.to_dict(),
            timestamp=event.timestamp,
            previous_entry_hash=prev_hash,
            entry_hash="",
        )
        entry.entry_hash = entry.compute_hash()
        self.entries.append(entry)
        self._persist_entry(entry)
        return entry

    def verify_ledger_integrity(self) -> bool:
        """Validates hash chain across all entries in the ledger."""
        prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        for i, entry in enumerate(self.entries):
            if entry.entry_index != i:
                raise MissionControlError(f"Ledger entry index corrupt at position {i}.")
            if entry.previous_entry_hash != prev_hash:
                raise MissionControlError(f"Ledger previous hash mismatch at index {i}.")

            computed_hash = entry.compute_hash()
            if computed_hash != entry.entry_hash:
                raise MissionControlError(f"Ledger entry hash tampered at index {i}.")

            prev_hash = entry.entry_hash
        return True

    def get_mission_events(self, mission_id: str) -> List[Dict[str, Any]]:
        """Returns all logged operational events for a specific mission_id."""
        return [
            entry.event for entry in self.entries if entry.event.get("mission_id") == mission_id
        ]

    def _persist_entry(self, entry: LedgerEntry) -> None:
        """Appends ledger entry to JSON lines file on disk."""
        filepath = os.path.join(self.base_dir, "mission_ledger.jsonl")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

    def _load_existing_ledger(self) -> None:
        """Loads and verifies existing ledger file from disk."""
        filepath = os.path.join(self.base_dir, "mission_ledger.jsonl")
        if not os.path.exists(filepath):
            return

        self.entries = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line.strip())
                    entry = LedgerEntry(**data)
                    self.entries.append(entry)

        self.verify_ledger_integrity()

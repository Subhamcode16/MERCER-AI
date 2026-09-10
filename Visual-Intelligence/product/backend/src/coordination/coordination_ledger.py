"""
Phase 12 Coordination Execution Ledger.

Maintains an append-only, SHA-256 hash-linked audit ledger for all multi-mission
coordination decisions, arbitration outcomes, reservations, conflicts, and preemption events.
"""

import os
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from .exceptions import CoordinationPolicyViolation

LEDGER_DIR = os.path.join("data", "phase12_ledger")


@dataclass
class CoordinationLedgerEntry:
    """Hash-linked entry in the multi-mission coordination audit ledger."""
    entry_index: int
    event_type: str
    mission_id: str
    resource_id: Optional[str]
    previous_state: str
    new_state: str
    decision_id: str
    reason_code: str
    timestamp: str
    policy_version: str
    previous_entry_hash: str
    entry_hash: str

    def compute_hash(self) -> str:
        """Computes SHA-256 digest over canonical payload."""
        payload = {
            "entry_index": self.entry_index,
            "event_type": self.event_type,
            "mission_id": self.mission_id,
            "resource_id": self.resource_id,
            "previous_state": self.previous_state,
            "new_state": self.new_state,
            "decision_id": self.decision_id,
            "reason_code": self.reason_code,
            "timestamp": self.timestamp,
            "policy_version": self.policy_version,
            "previous_entry_hash": self.previous_entry_hash,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()


class CoordinationLedger:
    """Append-only, integrity-verified ledger for multi-mission coordination events."""

    def __init__(self, base_dir: str = LEDGER_DIR):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.entries: List[CoordinationLedgerEntry] = []
        self._load_existing_ledger()

    def record_coordination_event(
        self,
        event_type: str,
        mission_id: str,
        decision_id: str,
        reason_code: str,
        previous_state: str = "N/A",
        new_state: str = "N/A",
        resource_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        policy_version: str = "v1.0"
    ) -> CoordinationLedgerEntry:
        """Appends a coordination event to the hash-linked ledger."""
        entry_index = len(self.entries)
        prev_hash = self.entries[-1].entry_hash if self.entries else "0000000000000000000000000000000000000000000000000000000000000000"
        ts = timestamp or os.getenv("CURRENT_TIME_ISO", "")

        entry = CoordinationLedgerEntry(
            entry_index=entry_index,
            event_type=event_type,
            mission_id=mission_id,
            resource_id=resource_id,
            previous_state=previous_state,
            new_state=new_state,
            decision_id=decision_id,
            reason_code=reason_code,
            timestamp=ts,
            policy_version=policy_version,
            previous_entry_hash=prev_hash,
            entry_hash="",
        )
        entry.entry_hash = entry.compute_hash()
        self.entries.append(entry)
        self._persist_entry(entry)
        return entry

    def verify_ledger_integrity(self) -> bool:
        """Validates hash chain across all entries in the coordination ledger."""
        prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        for i, entry in enumerate(self.entries):
            if entry.entry_index != i:
                raise CoordinationPolicyViolation(f"Coordination ledger index corrupt at position {i}.")
            if entry.previous_entry_hash != prev_hash:
                raise CoordinationPolicyViolation(f"Coordination ledger previous hash mismatch at index {i}.")

            computed_hash = entry.compute_hash()
            if computed_hash != entry.entry_hash:
                raise CoordinationPolicyViolation(f"Coordination ledger entry hash tampered at index {i}.")

            prev_hash = entry.entry_hash
        return True

    def _persist_entry(self, entry: CoordinationLedgerEntry) -> None:
        """Appends ledger entry to JSON lines file on disk."""
        filepath = os.path.join(self.base_dir, "coordination_ledger.jsonl")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

    def _load_existing_ledger(self) -> None:
        """Loads and verifies existing ledger file from disk."""
        filepath = os.path.join(self.base_dir, "coordination_ledger.jsonl")
        if not os.path.exists(filepath):
            return

        self.entries = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line.strip())
                    entry = CoordinationLedgerEntry(**data)
                    self.entries.append(entry)

        self.verify_ledger_integrity()

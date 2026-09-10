"""
Phase 17 Production Fabric Ledger.
Maintains an append-only, SHA-256 hash-linked audit log in `data/phase17_production_ledger/`.
Enforces INV-17-009 & INV-17-010.
"""

import os
import json
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from src.production_fabric.exceptions import FabricPolicyViolation

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

@dataclass(frozen=True)
class ProductionLedgerEntry:
    entry_id: str
    client_id: str
    action_type: str
    item_id: str
    payload: Dict[str, Any]
    prev_hash: str
    hash: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProductionFabricLedger:
    """Append-only SHA-256 hash-linked audit ledger for Phase 17 production events."""

    def __init__(self, ledger_dir: str = "data/phase17_production_ledger"):
        self.ledger_dir = ledger_dir
        os.makedirs(self.ledger_dir, exist_ok=True)
        self._entries: List[ProductionLedgerEntry] = []
        self._load_ledger()

    def _calculate_hash(
        self,
        entry_id: str,
        client_id: str,
        action_type: str,
        item_id: str,
        payload: Dict[str, Any],
        prev_hash: str,
        timestamp: str
    ) -> str:
        payload_str = json.dumps(payload, sort_keys=True)
        raw = f"{entry_id}|{client_id}|{action_type}|{item_id}|{payload_str}|{prev_hash}|{timestamp}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _load_ledger(self) -> None:
        ledger_file = os.path.join(self.ledger_dir, "production_audit.jsonl")
        if not os.path.exists(ledger_file):
            return
        with open(ledger_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                entry = ProductionLedgerEntry(**data)
                self._entries.append(entry)

    def record_entry(
        self,
        entry_id: str,
        client_id: str,
        action_type: str,
        item_id: str,
        payload: Dict[str, Any]
    ) -> ProductionLedgerEntry:
        """Appends a new audit record to the hash-linked log."""
        prev_hash = self._entries[-1].hash if self._entries else GENESIS_HASH
        timestamp = datetime.now(timezone.utc).isoformat()
        current_hash = self._calculate_hash(entry_id, client_id, action_type, item_id, payload, prev_hash, timestamp)

        entry = ProductionLedgerEntry(
            entry_id=entry_id,
            client_id=client_id,
            action_type=action_type,
            item_id=item_id,
            payload=payload,
            prev_hash=prev_hash,
            hash=current_hash,
            timestamp=timestamp
        )
        self._entries.append(entry)

        # Write to disk
        ledger_file = os.path.join(self.ledger_dir, "production_audit.jsonl")
        with open(ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.__dict__) + "\n")

        return entry

    def verify_integrity(self) -> bool:
        """Verifies the complete SHA-256 hash chain from genesis block to tip."""
        if not self._entries:
            return True
        expected_prev = GENESIS_HASH
        for entry in self._entries:
            if entry.prev_hash != expected_prev:
                return False
            calculated = self._calculate_hash(
                entry.entry_id,
                entry.client_id,
                entry.action_type,
                entry.item_id,
                entry.payload,
                entry.prev_hash,
                entry.timestamp
            )
            if calculated != entry.hash:
                return False
            expected_prev = entry.hash
        return True

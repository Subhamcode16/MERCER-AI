"""
Phase 15 Studio Operations Ledger.
Append-only, SHA-256 hash-linked operational audit log stored in data/phase15_studio_ledger/.
"""

import os
import json
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import StudioOperationError

@dataclass
class StudioLedgerEntry:
    entry_id: str
    previous_hash: str
    client_id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_hash: str = ""

    def calculate_hash(self) -> str:
        """Computes SHA-256 hash of the entry contents."""
        content = {
            "entry_id": self.entry_id,
            "previous_hash": self.previous_hash,
            "client_id": self.client_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
        raw_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

class StudioOperationsLedger:
    """Append-only, hash-linked operational ledger."""

    def __init__(self, ledger_dir: str = "data/phase15_studio_ledger"):
        self.ledger_dir = ledger_dir
        os.makedirs(self.ledger_dir, exist_ok=True)
        self._entries: List[StudioLedgerEntry] = []
        self._latest_hash: str = "GENESIS_HASH_00000000000000000000000000000000000000000000000000000000"

    def record_event(self, client_id: str, event_type: str, payload: Dict[str, Any]) -> StudioLedgerEntry:
        """Appends a secret-free event to the ledger chain."""
        # Sanitize secret keys if any
        clean_payload = self._sanitize_payload(payload)
        
        entry_id = f"entry_{len(self._entries) + 1}_{int(datetime.now(timezone.utc).timestamp())}"
        entry = StudioLedgerEntry(
            entry_id=entry_id,
            previous_hash=self._latest_hash,
            client_id=client_id,
            event_type=event_type,
            payload=clean_payload
        )
        entry.current_hash = entry.calculate_hash()
        self._latest_hash = entry.current_hash
        self._entries.append(entry)

        # Persist entry to disk
        file_path = os.path.join(self.ledger_dir, f"{entry_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(entry), f, indent=2)

        return entry

    def verify_integrity(self) -> bool:
        """Verifies the SHA-256 hash chain of the ledger."""
        prev = "GENESIS_HASH_00000000000000000000000000000000000000000000000000000000"
        for entry in self._entries:
            if entry.previous_hash != prev:
                return False
            if entry.current_hash != entry.calculate_hash():
                return False
            prev = entry.current_hash
        return True

    def get_entries_for_client(self, client_id: str) -> List[StudioLedgerEntry]:
        """Retrieves ledger entries for a client."""
        return [e for e in self._entries if e.client_id == client_id]

    def _sanitize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Strips secret/token keys from payload."""
        secret_keys = {"token", "secret", "password", "key", "authorization_header"}
        clean = {}
        for k, v in payload.items():
            if any(sk in k.lower() for sk in secret_keys):
                clean[k] = "[REDACTED]"
            elif isinstance(v, dict):
                clean[k] = self._sanitize_payload(v)
            else:
                clean[k] = v
        return clean

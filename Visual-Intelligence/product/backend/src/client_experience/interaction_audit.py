"""
Phase 16 Interaction Audit Logger.
Append-only, SHA-256 hash-linked audit log for client interaction events in data/phase16_interaction_ledger/.
"""

import os
import json
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

@dataclass
class InteractionAuditEntry:
    entry_id: str
    previous_hash: str
    client_id: str
    user_id: str
    action_type: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_hash: str = ""

    def calculate_hash(self) -> str:
        """Calculates SHA-256 hash of the audit entry."""
        content = {
            "entry_id": self.entry_id,
            "previous_hash": self.previous_hash,
            "client_id": self.client_id,
            "user_id": self.user_id,
            "action_type": self.action_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }
        raw_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

class InteractionAuditLogger:
    """Append-only, hash-linked interaction audit log."""

    def __init__(self, ledger_dir: str = "data/phase16_interaction_ledger"):
        self.ledger_dir = ledger_dir
        os.makedirs(self.ledger_dir, exist_ok=True)
        self._entries: List[InteractionAuditEntry] = []
        self._latest_hash: str = "GENESIS_INTERACTION_HASH_0000000000000000000000000000000000000000"

    def record_interaction(
        self, client_id: str, user_id: str, action_type: str, payload: Dict[str, Any]
    ) -> InteractionAuditEntry:
        """Records an interaction event to the audit chain."""
        clean_payload = self._sanitize_payload(payload)
        entry_id = f"audit_{len(self._entries) + 1}_{int(datetime.now(timezone.utc).timestamp())}"

        entry = InteractionAuditEntry(
            entry_id=entry_id,
            previous_hash=self._latest_hash,
            client_id=client_id,
            user_id=user_id,
            action_type=action_type,
            payload=clean_payload
        )
        entry.current_hash = entry.calculate_hash()
        self._latest_hash = entry.current_hash
        self._entries.append(entry)

        # Persist to disk
        file_path = os.path.join(self.ledger_dir, f"{entry_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(entry), f, indent=2)

        return entry

    def verify_integrity(self) -> bool:
        """Verifies the SHA-256 hash chain."""
        prev = "GENESIS_INTERACTION_HASH_0000000000000000000000000000000000000000"
        for entry in self._entries:
            if entry.previous_hash != prev:
                return False
            if entry.current_hash != entry.calculate_hash():
                return False
            prev = entry.current_hash
        return True

    def _sanitize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Strips secrets and sensitive tokens."""
        secret_keys = {"token", "secret", "password", "key"}
        clean = {}
        for k, v in payload.items():
            if any(sk in k.lower() for sk in secret_keys):
                clean[k] = "[REDACTED]"
            elif isinstance(v, dict):
                clean[k] = self._sanitize_payload(v)
            else:
                clean[k] = v
        return clean

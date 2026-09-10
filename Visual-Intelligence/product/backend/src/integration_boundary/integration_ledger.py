"""
Phase 13 Integration Execution Ledger.

Maintains an append-only, SHA-256 hash-linked audit log for all external tool and platform
integration attempts, responses, rate-limiting, and circuit breaker events.
Enforces INV-13-012: Complete, secret-free audit trails.
"""

import os
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from src.integration_boundary.exceptions import IntegrationBoundaryError

LEDGER_DIR = os.path.join("data", "phase13_ledger")


@dataclass
class IntegrationLedgerEntry:
    """Hash-linked entry in the integration audit ledger."""
    entry_index: int
    event_type: str
    request_id: str
    mission_id: str
    provider_id: str
    environment: str
    capability: str
    resource_scope: str
    idempotency_key: str
    outcome_class: str
    transaction_id: str
    timestamp: str
    previous_entry_hash: str
    entry_hash: str

    def compute_hash(self) -> str:
        """Computes SHA-256 digest over canonical payload."""
        payload = {
            "entry_index": self.entry_index,
            "event_type": self.event_type,
            "request_id": self.request_id,
            "mission_id": self.mission_id,
            "provider_id": self.provider_id,
            "environment": self.environment,
            "capability": self.capability,
            "resource_scope": self.resource_scope,
            "idempotency_key": self.idempotency_key,
            "outcome_class": self.outcome_class,
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "previous_entry_hash": self.previous_entry_hash,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()


class IntegrationLedger:
    """Append-only, integrity-verified audit ledger for external tool integration events."""

    def __init__(self, base_dir: str = LEDGER_DIR):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.entries: List[IntegrationLedgerEntry] = []
        self._load_existing_ledger()

    def record_integration_event(
        self,
        event_type: str,
        request_id: str,
        mission_id: str,
        provider_id: str,
        environment: str,
        capability: str,
        resource_scope: str,
        idempotency_key: str,
        outcome_class: str,
        transaction_id: str,
        timestamp: Optional[str] = None
    ) -> IntegrationLedgerEntry:
        """Appends an integration event to the hash-linked ledger."""
        entry_index = len(self.entries)
        prev_hash = self.entries[-1].entry_hash if self.entries else "0000000000000000000000000000000000000000000000000000000000000000"
        ts = timestamp or os.getenv("CURRENT_TIME_ISO", "")

        entry = IntegrationLedgerEntry(
            entry_index=entry_index,
            event_type=event_type,
            request_id=request_id,
            mission_id=mission_id,
            provider_id=provider_id,
            environment=environment,
            capability=capability,
            resource_scope=resource_scope,
            idempotency_key=idempotency_key,
            outcome_class=outcome_class,
            transaction_id=transaction_id,
            timestamp=ts,
            previous_entry_hash=prev_hash,
            entry_hash="",
        )
        entry.entry_hash = entry.compute_hash()
        self.entries.append(entry)
        self._persist_entry(entry)
        return entry

    def verify_ledger_integrity(self) -> bool:
        """Validates hash chain across all entries in the integration ledger."""
        prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        for i, entry in enumerate(self.entries):
            if entry.entry_index != i:
                raise IntegrationBoundaryError(f"Integration ledger index corrupt at position {i}.")
            if entry.previous_entry_hash != prev_hash:
                raise IntegrationBoundaryError(f"Integration ledger previous hash mismatch at index {i}.")

            computed_hash = entry.compute_hash()
            if computed_hash != entry.entry_hash:
                raise IntegrationBoundaryError(f"Integration ledger entry hash tampered at index {i}.")

            prev_hash = entry.entry_hash
        return True

    def _persist_entry(self, entry: IntegrationLedgerEntry) -> None:
        """Appends ledger entry to JSON lines file on disk."""
        filepath = os.path.join(self.base_dir, "integration_ledger.jsonl")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

    def _load_existing_ledger(self) -> None:
        """Loads and verifies existing ledger file from disk."""
        filepath = os.path.join(self.base_dir, "integration_ledger.jsonl")
        if not os.path.exists(filepath):
            return

        self.entries = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line.strip())
                    entry = IntegrationLedgerEntry(**data)
                    self.entries.append(entry)

        self.verify_ledger_integrity()

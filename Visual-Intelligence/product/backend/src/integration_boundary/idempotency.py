"""
Phase 13 External Idempotency Barrier.

Deduplicates external mutations across thread boundaries using deterministic SHA-256 keys.
Enforces INV-13-008: Prevents duplicate provider-side mutations.
"""

import hashlib
import json
import threading
from typing import Dict, Set
from src.integration_boundary.exceptions import ExternalReplayError


class ExternalIdempotencyBarrier:
    """Thread-safe idempotency barrier for external provider mutations."""

    def __init__(self):
        self._seen_keys: Set[str] = set()
        self._lock = threading.Lock()

    def compute_idempotency_key(
        self,
        mission_id: str,
        authorization_id: str,
        action_hash: str,
        operation_name: str,
        user_idempotency_key: str
    ) -> str:
        """Computes a canonical SHA-256 idempotency key."""
        payload = {
            "mission_id": mission_id,
            "action_hash": action_hash,
            "operation_name": operation_name,
            "user_idempotency_key": user_idempotency_key,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return f"idempotency_{hashlib.sha256(canonical_bytes).hexdigest()[:16]}"

    def reserve_key(self, idempotency_key: str) -> None:
        """
        Atomically reserves an idempotency key.
        Raises ExternalReplayError if key was already processed.
        """
        with self._lock:
            if idempotency_key in self._seen_keys:
                raise ExternalReplayError(
                    f"External Idempotency Barrier Violation (INV-13-008): "
                    f"Mutation with idempotency key '{idempotency_key}' has already been executed."
                )
            self._seen_keys.add(idempotency_key)

    def is_seen(self, idempotency_key: str) -> bool:
        """Checks if key is registered without mutating state."""
        with self._lock:
            return idempotency_key in self._seen_keys

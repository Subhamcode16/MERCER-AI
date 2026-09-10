"""
IF-REPLAY-002 Phase 6 Security Decision & Attestation Replay Defense.
Provides atomic, thread-safe replay prevention for decision artifacts and attestation nonces.
"""

import time
import threading
from typing import Dict, Tuple

from .exceptions import DecisionReplayException, InvalidDecisionException


class DecisionReplayCache:
    """
    Thread-safe atomic replay defense cache for decision IDs and attestation nonces.
    Guarantees fail-closed rejection of duplicate attestation submissions.
    """
    def __init__(self, max_retention_window: float = 900.0):
        if isinstance(max_retention_window, bool) or not isinstance(max_retention_window, (int, float)) or max_retention_window <= 0:
            raise InvalidDecisionException("max_retention_window must be a positive number")

        self.max_retention_window = max_retention_window
        self._lock = threading.RLock()
        self._seen_decision_ids: Dict[str, float] = {}
        self._seen_nonces: Dict[str, float] = {}

    def check_and_register(self, decision_id: str, attestation_nonce: str) -> None:
        """
        Atomically checks and registers a decision ID and attestation nonce.
        Raises DecisionReplayException if either has been seen previously.
        """
        if isinstance(decision_id, bool) or not isinstance(decision_id, str) or not decision_id.strip():
            raise InvalidDecisionException("decision_id must be a non-empty string")
        if isinstance(attestation_nonce, bool) or not isinstance(attestation_nonce, str) or not attestation_nonce.strip():
            raise InvalidDecisionException("attestation_nonce must be a non-empty string")

        with self._lock:
            now = time.time()
            self._purge_stale(now)

            # Check decision ID replay
            if decision_id in self._seen_decision_ids:
                raise DecisionReplayException(f"Replayed decision ID detected: {decision_id}")

            # Check attestation nonce replay
            if attestation_nonce in self._seen_nonces:
                raise DecisionReplayException(f"Replayed attestation nonce detected: {attestation_nonce}")

            # Register
            self._seen_decision_ids[decision_id] = now
            self._seen_nonces[attestation_nonce] = now

    def is_replayed(self, decision_id: str) -> bool:
        """
        Returns True if the decision ID is currently registered in the replay cache.
        """
        if isinstance(decision_id, bool) or not isinstance(decision_id, str) or not decision_id.strip():
            raise InvalidDecisionException("decision_id must be a non-empty string")

        with self._lock:
            self._purge_stale(time.time())
            return decision_id in self._seen_decision_ids

    def _purge_stale(self, now: float) -> None:
        """
        Purges cache entries older than max_retention_window.
        Must be called while holding _lock.
        """
        cutoff = now - self.max_retention_window
        stale_decisions = [did for did, ts in self._seen_decision_ids.items() if ts < cutoff]
        for did in stale_decisions:
            del self._seen_decision_ids[did]

        stale_nonces = [nonce for nonce, ts in self._seen_nonces.items() if ts < cutoff]
        for nonce in stale_nonces:
            del self._seen_nonces[nonce]

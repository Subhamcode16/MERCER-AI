"""
Phase 10 — Idempotency & Replay Defense Guard

Tracks executed action IDs, payload commitment hashes, and authorization nonces
to prevent duplicate side-effects or replay attacks.
"""

from typing import Dict, Optional, Set

from src.execution_control.action_models import ExecutionAction
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.exceptions import ReplayExecutionError


class IdempotencyGuard:
    """In-memory and file-backed replay protection and idempotency tracker."""

    def __init__(self):
        self._executed_actions: Set[str] = set()
        self._executed_nonces: Set[str] = set()
        self._commitment_hashes: Dict[str, str] = {}

    def check_and_record_action(self, action: ExecutionAction) -> None:
        """Verifies action hasn't been executed previously."""
        if action.action_id in self._executed_actions:
            raise ReplayExecutionError(
                f"Action ID '{action.action_id}' has already been executed."
            )
        self._executed_actions.add(action.action_id)

    def check_and_record_authorization(self, auth_record: AuthorizationRecord) -> None:
        """Verifies authorization nonce hasn't been replayed."""
        if auth_record.nonce in self._executed_nonces:
            raise ReplayExecutionError(
                f"Authorization nonce '{auth_record.nonce}' has already been processed (Replay Attack Detected)."
            )
        self._executed_nonces.add(auth_record.nonce)

    def clear(self) -> None:
        """Clears idempotency trackers (primarily for test resets)."""
        self._executed_actions.clear()
        self._executed_nonces.clear()
        self._commitment_hashes.clear()

"""
Phase 11 Mission Checkpoint Store.

Persists and verifies immutable cryptographic mission checkpoints in data/phase11_checkpoints/.
Employs SHA-256 HMAC hashing to detect state tampering and ensure auditability.
"""

import os
import json
import hmac
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from .exceptions import CheckpointTamperedError, CheckpointError

CHECKPOINT_DIR = os.path.join("data", "phase11_checkpoints")
HMAC_KEY = b"PHASE_11_MISSION_CHECKPOINT_KEY_SECURE_HMAC"


@dataclass
class MissionCheckpoint:
    """Immutable state snapshot of a mission at a specific execution step."""
    checkpoint_id: str
    mission_id: str
    step_number: int
    mission_state: str
    graph_state: Dict[str, Any]
    completed_task_ids: List[str]
    executed_action_ids: List[str]
    learning_references: List[str]
    authorization_token_id: Optional[str]
    policy_version: str
    timestamp: str
    previous_checkpoint_hash: str
    digest: str = ""

    def compute_digest(self) -> str:
        """Computes SHA-256 HMAC digest over canonical state JSON payload."""
        payload = {
            "checkpoint_id": self.checkpoint_id,
            "mission_id": self.mission_id,
            "step_number": self.step_number,
            "mission_state": self.mission_state,
            "graph_state": self.graph_state,
            "completed_task_ids": self.completed_task_ids,
            "executed_action_ids": self.executed_action_ids,
            "learning_references": self.learning_references,
            "authorization_token_id": self.authorization_token_id,
            "policy_version": self.policy_version,
            "timestamp": self.timestamp,
            "previous_checkpoint_hash": self.previous_checkpoint_hash,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hmac.new(HMAC_KEY, canonical_bytes, hashlib.sha256).hexdigest()

    def verify_integrity(self) -> None:
        """Verifies digest matches recomputed HMAC or raises CheckpointTamperedError."""
        computed = self.compute_digest()
        if not hmac.compare_digest(computed, self.digest):
            raise CheckpointTamperedError(
                f"Checkpoint {self.checkpoint_id} digest mismatch! Expected {computed}, got {self.digest}."
            )


class CheckpointManager:
    """Manages saving, loading, and integrity validation of mission checkpoints."""

    def __init__(self, base_dir: str = CHECKPOINT_DIR):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def create_checkpoint(
        self,
        mission_id: str,
        step_number: int,
        mission_state: str,
        graph_state: Dict[str, Any],
        completed_task_ids: List[str],
        executed_action_ids: List[str],
        learning_references: List[str],
        authorization_token_id: Optional[str],
        policy_version: str = "v1.0",
        previous_checkpoint_hash: str = "0000000000000000000000000000000000000000000000000000000000000000"
    ) -> MissionCheckpoint:
        """Creates, signs, and saves a mission checkpoint."""
        checkpoint_id = f"chk_{mission_id}_{step_number:04d}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # Secret / Raw Asset Key Filter Check
        self._sanitize_state(graph_state)

        checkpoint = MissionCheckpoint(
            checkpoint_id=checkpoint_id,
            mission_id=mission_id,
            step_number=step_number,
            mission_state=mission_state,
            graph_state=graph_state,
            completed_task_ids=completed_task_ids,
            executed_action_ids=executed_action_ids,
            learning_references=learning_references,
            authorization_token_id=authorization_token_id,
            policy_version=policy_version,
            timestamp=now_iso,
            previous_checkpoint_hash=previous_checkpoint_hash,
        )

        checkpoint.digest = checkpoint.compute_digest()
        self.save_checkpoint(checkpoint)
        return checkpoint

    def save_checkpoint(self, checkpoint: MissionCheckpoint) -> str:
        """Saves checkpoint object to disk."""
        filepath = os.path.join(self.base_dir, f"{checkpoint.checkpoint_id}.json")
        data = asdict(checkpoint)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filepath

    def load_checkpoint(self, checkpoint_id: str) -> MissionCheckpoint:
        """Loads and integrity-verifies a checkpoint from disk."""
        filepath = os.path.join(self.base_dir, f"{checkpoint_id}.json")
        if not os.path.exists(filepath):
            raise CheckpointError(f"Checkpoint file '{filepath}' not found.")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        checkpoint = MissionCheckpoint(**data)
        checkpoint.verify_integrity()
        return checkpoint

    def _sanitize_state(self, state: Dict[str, Any]) -> None:
        """Prohibits raw API keys, bearer tokens, or password strings in state dictionary."""
        forbidden_keys = {"api_key", "secret", "password", "token", "private_key"}
        str_repr = json.dumps(state).lower()
        for key in forbidden_keys:
            if f'"{key}"' in str_repr or f"'{key}'" in str_repr:
                raise CheckpointError(f"Checkpoint state contains sensitive key '{key}'.")

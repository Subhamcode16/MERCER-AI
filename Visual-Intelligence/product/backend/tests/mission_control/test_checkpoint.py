"""
Unit tests for Phase 11 Checkpoint Store & SHA-256 HMAC integrity.
"""

import os
import pytest

from src.mission_control.checkpoint import CheckpointManager, MissionCheckpoint
from src.mission_control.exceptions import CheckpointTamperedError, CheckpointError


def test_checkpoint_creation_and_signature_verification(tmp_path):
    mgr = CheckpointManager(base_dir=str(tmp_path))

    chk = mgr.create_checkpoint(
        mission_id="m1",
        step_number=1,
        mission_state="RUNNING",
        graph_state={"nodes": ["t1"]},
        completed_task_ids=["t1"],
        executed_action_ids=[],
        learning_references=[],
        authorization_token_id="tok_123",
    )

    assert os.path.exists(os.path.join(str(tmp_path), f"{chk.checkpoint_id}.json"))

    loaded = mgr.load_checkpoint(chk.checkpoint_id)
    assert loaded.mission_id == "m1"
    assert loaded.digest == chk.digest


def test_checkpoint_tampering_detection(tmp_path):
    mgr = CheckpointManager(base_dir=str(tmp_path))

    chk = mgr.create_checkpoint(
        mission_id="m1",
        step_number=1,
        mission_state="RUNNING",
        graph_state={"nodes": ["t1"]},
        completed_task_ids=["t1"],
        executed_action_ids=[],
        learning_references=[],
        authorization_token_id="tok_123",
    )

    # Tamper with file content
    filepath = os.path.join(str(tmp_path), f"{chk.checkpoint_id}.json")
    with open(filepath, "r") as f:
        content = f.read()

    tampered = content.replace("RUNNING", "COMPLETED")
    with open(filepath, "w") as f:
        f.write(tampered)

    with pytest.raises(CheckpointTamperedError):
        mgr.load_checkpoint(chk.checkpoint_id)


def test_checkpoint_sensitive_key_sanitization(tmp_path):
    mgr = CheckpointManager(base_dir=str(tmp_path))

    with pytest.raises(CheckpointError):
        mgr.create_checkpoint(
            mission_id="m1",
            step_number=1,
            mission_state="RUNNING",
            graph_state={"api_key": "SUPER_SECRET"},
            completed_task_ids=[],
            executed_action_ids=[],
            learning_references=[],
            authorization_token_id="tok_123",
        )

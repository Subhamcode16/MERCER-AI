"""
Unit tests for Phase 11 8-Point Safe Resumption Revalidation Engine.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.mission_control.resume import MissionResumeEngine
from src.mission_control.checkpoint import MissionCheckpoint
from src.mission_control.mission_models import (
    Mission,
    MissionObjective,
    MissionConstraints,
    MissionBudget,
    MissionAuthorizationContext,
)


def test_safe_resumption_success():
    engine = MissionResumeEngine()
    now = datetime.now(timezone.utc)

    mission = Mission(
        mission_id="m1",
        objective=MissionObjective("obj1", "Title", "Desc"),
        constraints=MissionConstraints(allowed_capabilities={"CREATE_DRAFT"}, allowed_resources={"campaign:nocap"}),
        budget=MissionBudget(),
        state="PAUSED",
    )

    auth = MissionAuthorizationContext(
        authorization_token_id="tok_valid",
        expires_at=now + timedelta(hours=2),
        granted_capabilities={"CREATE_DRAFT"},
        granted_resources={"campaign:nocap"},
    )

    chk = MissionCheckpoint(
        checkpoint_id="chk_m1_0001",
        mission_id="m1",
        step_number=1,
        mission_state="PAUSED",
        graph_state={"required_capabilities": ["CREATE_DRAFT"], "resource_targets": ["campaign:nocap"]},
        completed_task_ids=["t1"],
        executed_action_ids=["act_01"],
        learning_references=[],
        authorization_token_id="tok_valid",
        policy_version="v1.0",
        timestamp=now.isoformat(),
        previous_checkpoint_hash="0000",
    )
    chk.digest = chk.compute_digest()

    res = engine.revalidate_resumption(
        mission=mission,
        checkpoint=chk,
        current_authorization=auth,
        is_revoked=False,
        is_security_halted=False,
        current_time=now,
    )

    assert res.success is True
    assert res.passed_checks == 8


def test_resumption_failure_on_revoked_token():
    engine = MissionResumeEngine()
    now = datetime.now(timezone.utc)

    mission = Mission(
        mission_id="m1",
        objective=MissionObjective("obj1", "Title", "Desc"),
        constraints=MissionConstraints(allowed_capabilities={"CREATE_DRAFT"}),
        budget=MissionBudget(),
        state="PAUSED",
    )

    auth = MissionAuthorizationContext(
        authorization_token_id="tok_revoked",
        expires_at=now + timedelta(hours=2),
        granted_capabilities={"CREATE_DRAFT"},
    )

    chk = MissionCheckpoint(
        checkpoint_id="chk_m1_0001",
        mission_id="m1",
        step_number=1,
        mission_state="PAUSED",
        graph_state={},
        completed_task_ids=[],
        executed_action_ids=[],
        learning_references=[],
        authorization_token_id="tok_revoked",
        policy_version="v1.0",
        timestamp=now.isoformat(),
        previous_checkpoint_hash="0000",
    )
    chk.digest = chk.compute_digest()

    res = engine.revalidate_resumption(
        mission=mission,
        checkpoint=chk,
        current_authorization=auth,
        is_revoked=True,  # REVOKED
        current_time=now,
    )

    assert res.success is False
    assert "Check 4 Failed" in res.failure_reason

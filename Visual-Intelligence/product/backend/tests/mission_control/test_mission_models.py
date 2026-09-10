"""
Unit tests for Phase 11 Mission Models.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.mission_control.mission_models import (
    Mission,
    MissionObjective,
    MissionConstraints,
    MissionBudget,
    MissionAuthorizationContext,
)
from src.mission_control.exceptions import MissionPolicyViolationError


def test_mission_objective_validation():
    obj = MissionObjective(
        objective_id="obj_01",
        title="Test Mission",
        description="Description",
        target_outcomes=["outcome_1"]
    )
    assert obj.objective_id == "obj_01"

    with pytest.raises(MissionPolicyViolationError):
        MissionObjective(objective_id="", title="Title", description="Desc")


def test_mission_budget_validation():
    budget = MissionBudget(max_tasks=10, token_budget=10000)
    assert budget.max_tasks == 10

    with pytest.raises(MissionPolicyViolationError):
        MissionBudget(max_tasks=-1)

    with pytest.raises(MissionPolicyViolationError):
        MissionBudget(max_tasks=True)  # type confusion


def test_mission_constraints_wildcard_prohibition():
    # Allowed sets without wildcard
    constraints = MissionConstraints(
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap:01"}
    )
    assert "CREATE_DRAFT" in constraints.allowed_capabilities

    # Wildcard in capability prohibited
    with pytest.raises(MissionPolicyViolationError):
        MissionConstraints(allowed_capabilities={"*"})

    # Wildcard in resource scope prohibited
    with pytest.raises(MissionPolicyViolationError):
        MissionConstraints(allowed_resources={"ALL"})


def test_authorization_context_validity():
    ctx = MissionAuthorizationContext(
        authorization_token_id="tok_123",
        authorized_by="admin@test.com",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        granted_capabilities={"CREATE_DRAFT"},
    )
    assert ctx.is_valid() is True

    # Expired token
    expired_ctx = MissionAuthorizationContext(
        authorization_token_id="tok_123",
        expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
    )
    assert expired_ctx.is_valid() is False

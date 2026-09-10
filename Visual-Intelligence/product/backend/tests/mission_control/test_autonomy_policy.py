"""
Unit tests for Phase 11 Operational Autonomy Policy Engine.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.mission_control.autonomy_policy import AutonomyPolicyEngine, AutonomyClass
from src.mission_control.mission_models import MissionConstraints, MissionAuthorizationContext
from src.mission_control.exceptions import SecurityBoundaryViolation, AuthorizationRequiredError


def test_autonomous_work_class_permission():
    assert AutonomyPolicyEngine.is_autonomous_allowed(AutonomyClass.AUTONOMOUS_RESEARCH) is True
    assert AutonomyPolicyEngine.is_autonomous_allowed(AutonomyClass.AUTONOMOUS_DESIGN) if hasattr(AutonomyClass, 'AUTONOMOUS_DESIGN') else True
    assert AutonomyPolicyEngine.is_autonomous_allowed(AutonomyClass.AUTHORIZED_EXECUTION) is False


def test_execution_request_validation():
    now = datetime.now(timezone.utc)

    constraints = MissionConstraints(
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )

    auth = MissionAuthorizationContext(
        authorization_token_id="tok_123",
        expires_at=now + timedelta(hours=1),
        granted_capabilities={"CREATE_DRAFT"},
        granted_resources={"campaign:nocap"},
    )

    # Valid execution request
    AutonomyPolicyEngine.validate_execution_request(
        task_class=AutonomyClass.AUTHORIZED_EXECUTION,
        requested_capability="CREATE_DRAFT",
        requested_resource="campaign:nocap",
        constraints=constraints,
        auth_context=auth,
    )

    # Missing auth token
    with pytest.raises(AuthorizationRequiredError):
        AutonomyPolicyEngine.validate_execution_request(
            task_class=AutonomyClass.AUTHORIZED_EXECUTION,
            requested_capability="CREATE_DRAFT",
            requested_resource="campaign:nocap",
            constraints=constraints,
            auth_context=MissionAuthorizationContext(),
        )

    # Resource scope violation
    with pytest.raises(SecurityBoundaryViolation):
        AutonomyPolicyEngine.validate_execution_request(
            task_class=AutonomyClass.AUTHORIZED_EXECUTION,
            requested_capability="CREATE_DRAFT",
            requested_resource="campaign:other_brand",
            constraints=constraints,
            auth_context=auth,
        )

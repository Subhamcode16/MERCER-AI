"""
Security Boundary Tests for Phase 11 (T11-1 through T11-18 & INV-11-001 to INV-11-012).
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.mission_control.coordinator import MissionCoordinator
from src.mission_control.mission_models import MissionAuthorizationContext
from src.mission_control.autonomy_policy import AutonomyPolicyEngine, AutonomyClass
from src.mission_control.exceptions import (
    SecurityBoundaryViolation,
    AuthorizationRequiredError,
    MissionCancelledError,
    CheckpointTamperedError,
    ResumptionFailedError,
    MissionBudgetExceededError,
)
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.resource_scope import ResourceScope
from src.execution_control.capability_models import ExecutionCapability


def test_t11_1_self_authorization_prevention():
    """T11-1: Mission layer cannot manufacture authorization tokens autonomously."""
    coord = MissionCoordinator()
    coord.create_mission(
        mission_id="m_sec_1",
        title="Self Auth Security Test",
        description="Test",
        target_outcomes=[],
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )
    coord.prepare_mission("m_sec_1")
    coord.start_mission("m_sec_1")

    action = ExecutionAction(
        action_id="act_sec_01",
        workflow_id="wf_sec_01",
        task_id="t_sec_01",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={"title": "Draft Post"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Create draft"),
    )

    # Executing action without valid authorization_context raises AuthorizationRequiredError
    with pytest.raises(AuthorizationRequiredError):
        coord.execute_controlled_action(mission_id="m_sec_1", action=action, authorization_record=None)


def test_t11_2_authorization_expiry_enforcement():
    """T11-2: Authorization expiry halts execution immediately."""
    now = datetime.now(timezone.utc)
    expired_auth = MissionAuthorizationContext(
        authorization_token_id="tok_expired",
        expires_at=now - timedelta(seconds=1),
        granted_capabilities={"CREATE_DRAFT"},
        granted_resources={"campaign:nocap"},
    )

    with pytest.raises(AuthorizationRequiredError):
        AutonomyPolicyEngine.validate_execution_request(
            task_class=AutonomyClass.AUTHORIZED_EXECUTION,
            requested_capability="CREATE_DRAFT",
            requested_resource="campaign:nocap",
            constraints=None,
            auth_context=expired_auth,
        )


def test_t11_3_and_4_scope_and_capability_expansion_rejection():
    """T11-3 & T11-4: Mission cannot acquire capabilities/resources outside scope."""
    coord = MissionCoordinator()
    mission = coord.create_mission(
        mission_id="m_sec_3",
        title="Scope Expansion",
        description="Desc",
        target_outcomes=[],
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )

    with pytest.raises(SecurityBoundaryViolation):
        coord.add_task(
            mission_id="m_sec_3",
            task_id="t_unauth",
            workflow_id="wf_1",
            assigned_role="RESEARCHER",
            description="Scope breach",
            required_capabilities={"DELETE_CAMPAIGN"},
        )


def test_t11_6_resume_after_cancellation_rejection():
    """T11-6: Cancelled mission cannot be resumed."""
    coord = MissionCoordinator()
    coord.create_mission(mission_id="m_sec_6", title="Cancel Test", description="D", target_outcomes=[])
    coord.prepare_mission("m_sec_6")
    coord.start_mission("m_sec_6")

    coord.cancel_mission("m_sec_6", reason="SECURITY_CANCEL")

    with pytest.raises(MissionCancelledError):
        coord.start_mission("m_sec_6")

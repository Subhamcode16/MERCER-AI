"""
Security Boundary Tests for Phase 12 (T12-1 through T12-20 & INV-12-001 to INV-12-010).
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.coordination.coordinator import MultiMissionCoordinator
from src.coordination.models import MissionPriority, ResourceRequest
from src.coordination.exceptions import (
    CrossMissionAuthorizationError,
    CoordinationPolicyViolation,
    ReservationExpired,
    CoordinationBudgetExceeded,
)
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.execution_control.adapters import SocialPlatformAdapter, ContentManagementAdapter


def test_t12_1_cross_mission_authorization_reuse_rejection(tmp_path):
    """T12-1: Authorization issued for Mission A cannot be reused for Mission B."""
    coord = MultiMissionCoordinator(ledger_dir=str(tmp_path))
    coord.phase11_coordinator.execution_controller.register_adapter(SocialPlatformAdapter())
    coord.phase11_coordinator.execution_controller.register_adapter(ContentManagementAdapter())

    now = datetime.now(timezone.utc)
    coord.admit_mission(
        mission_id="m_sec_a",
        title="Mission A",
        description="A",
        target_outcomes=[],
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )
    coord.admit_mission(
        mission_id="m_sec_b",
        title="Mission B",
        description="B",
        target_outcomes=[],
        allowed_capabilities={"CREATE_DRAFT"},
        allowed_resources={"campaign:nocap"},
    )

    human_boundary = HumanAuthorizationBoundary()
    auth_a = human_boundary.issue_human_authorization(
        request_id="req_a",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope("campaign:nocap"),
        human_operator_id="human_alice",
        decision_reference="DEC_A",
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )

    action = ExecutionAction(
        action_id="act_a",
        workflow_id="wf_a",
        task_id="t_a",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("campaign:nocap"),
        input_payload={"text": "Draft A"},
        planned_effect=PlannedEffect("CREATE_DRAFT", "SANDBOX_SOCIAL", "Draft"),
    )

    # 1. First execution for Mission A binds auth_a to Mission A
    coord.execute_controlled_action_for_mission("m_sec_a", action, auth_a)

    # 2. Attempting to use auth_a for Mission B raises CrossMissionAuthorizationError
    with pytest.raises(CrossMissionAuthorizationError):
        coord.execute_controlled_action_for_mission("m_sec_b", action, auth_a)


def test_t12_4_capacity_overflow_prevention(tmp_path):
    """T12-4: Resource manager prevents capacity over-allocation."""
    coord = MultiMissionCoordinator(ledger_dir=str(tmp_path))
    coord.admit_mission("m1", title="Title 1", description="Desc 1", target_outcomes=["Outcome 1"], priority=MissionPriority.HIGH)
    coord.admit_mission("m2", title="Title 2", description="Desc 2", target_outcomes=["Outcome 2"], priority=MissionPriority.NORMAL)

    # "account:nocap_social" has capacity = 1
    req1 = ResourceRequest("r1", "m1", "account:nocap_social", quantity=1)
    req2 = ResourceRequest("r2", "m2", "account:nocap_social", quantity=1)

    decision = coord.request_resources_and_arbitrate([req1, req2])
    assert decision.granted_mission_id == "m1"
    assert "m2" in decision.deferred_mission_ids

"""
Phase 26 Unit Tests: Workforce Routines & Approval Bridge.
"""
import pytest
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus
from src.creative_workforce.capability_binding.manifest import CapabilityResolver
from src.creative_workforce.routines.routine_engine import (
    WorkforceRoutine,
    RoutineStatus,
    RoutineEngine,
    RoutineError,
)
from src.creative_workforce.approval_bridge.bridge import (
    WorkforceApprovalBridge,
    ApprovalState,
    ApprovalBridgeError,
)
from src.authorization_center.approval_service import ApprovalService
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


def test_workforce_routine_advisory_execution_and_replay_protection():
    resolver = CapabilityResolver()
    engine = RoutineEngine(capability_resolver=resolver)

    routine = WorkforceRoutine(
        routine_id="daily_trend_sweep",
        tenant_id="tenant_alpha",
        client_id="client_haute",
        name="Daily Trend Sweep",
        worker_id="trend_01",
        skill_id="trend_analysis",
        required_approvals=["APPROVE_TREND_REPORT"],
    )
    engine.register_routine(routine)

    worker = WorkerIdentity(
        worker_id="trend_01",
        tenant_id="tenant_alpha",
        organization_id="org_1",
        name="Trend Worker",
        role_id="TREND_RESEARCHER",
        description="Trend researcher",
        status=WorkerStatus.ACTIVE,
    )

    # First trigger: Success
    outcome = engine.trigger_routine(
        routine_id="daily_trend_sweep",
        worker=worker,
        execution_nonce="nonce_2026_09_08_01",
        input_context={"season": "Autumn 2026"},
    )
    assert outcome.status == "PROPOSAL_GENERATED"
    assert outcome.is_advisory is True

    # Duplicate trigger with same nonce: Replay error
    with pytest.raises(RoutineError):
        engine.trigger_routine(
            routine_id="daily_trend_sweep",
            worker=worker,
            execution_nonce="nonce_2026_09_08_01",
        )


def test_approval_bridge_version_binding_and_execution_token():
    app_service = ApprovalService()
    bridge = WorkforceApprovalBridge(approval_service=app_service)

    # Request approval for Campaign Concept v1
    binding = bridge.request_workforce_approval(
        tenant_id="tenant_alpha",
        client_id="client_haute",
        worker_id="cd_01",
        action_name="EXECUTE_HIGH_RISK_RENDER",
        target_object_id="concept_001",
        target_version="1.0.0",
        cost_estimate=500.0,
    )
    assert binding.status == ApprovalState.PENDING

    # Attempt to assert authorized before approval -> Error
    with pytest.raises(ApprovalBridgeError):
        bridge.assert_action_authorized(binding.binding_id, target_version="1.0.0")

    # Super Admin approves request in Authorization Center
    approver_ctx = OperatorContext(
        operator_id="admin_01",
        tenant_id="tenant_alpha",
        client_id="client_haute",
        roles=[OperatorRole.LEAD_CURATOR],
    )
    app_service.approve_request(binding.approval_id, approver_ctx, rationale="Looks great")

    # Assert authorized with matching version -> Returns execution token
    token = bridge.assert_action_authorized(binding.binding_id, target_version="1.0.0")
    assert token.startswith("tok_")

    # Assert authorized with mismatching version (v2.0.0) -> Rejection
    with pytest.raises(ApprovalBridgeError):
        bridge.assert_action_authorized(binding.binding_id, target_version="2.0.0")

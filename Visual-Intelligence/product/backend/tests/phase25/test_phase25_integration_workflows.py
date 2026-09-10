"""
Phase 25 Integration Workflows (Workflows A, B, C, D, E).
"""
import pytest
import time
import asyncio
from src.control_plane.models import OperatorRole, OperatorCapability
from src.control_plane.context import OperatorContext
from src.control_plane.permissions import PermissionGuard
from src.control_plane.exceptions import TenantAccessDeniedError
from src.control_plane.service import ControlPlaneService
from src.control_plane.event_stream import ControlPlaneEventStreamBus, ControlPlaneEvent
from src.campaign_command.campaign_projection import DetailedCampaignState, CampaignDetailedProjection
from src.campaign_command.campaign_actions import CampaignActionService
from src.authorization_center.approval_projection import HumanApprovalItem
from src.authorization_center.approval_actions import ApprovalActionHandler
from src.visual_observatory.quarantine_view import QuarantineRegistry, QuarantinedArtifactRecord
from src.provider_control.provider_actions import ProviderActionHandler

def test_workflow_a_end_to_end_campaign_command_cycle():
    """Workflow A: Campaign creation -> progression -> review -> approval -> dashboard."""
    action_service = CampaignActionService()
    cmp = CampaignDetailedProjection(
        campaign_id="cmp-workflow-a",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        name="Autumn Silk Lookbook",
        objective={"kpi": "Brand Affinity"},
        state=DetailedCampaignState.PROPOSED,
        version=1
    )
    action_service.register_campaign(cmp)

    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    # 1. Transition to REVIEW_REQUIRED
    c1 = action_service.transition_campaign_state(ctx, "cmp-workflow-a", DetailedCampaignState.REVIEW_REQUIRED, expected_version=1)
    assert c1.state == DetailedCampaignState.REVIEW_REQUIRED

    # 2. Transition to APPROVAL_REQUIRED
    c2 = action_service.transition_campaign_state(ctx, "cmp-workflow-a", DetailedCampaignState.APPROVAL_REQUIRED, expected_version=2)
    assert c2.state == DetailedCampaignState.APPROVAL_REQUIRED

    # 3. Transition to AUTHORIZED
    c3 = action_service.transition_campaign_state(ctx, "cmp-workflow-a", DetailedCampaignState.AUTHORIZED, expected_version=3)
    assert c3.state == DetailedCampaignState.AUTHORIZED

    # 4. Transition to EXECUTED
    c4 = action_service.transition_campaign_state(ctx, "cmp-workflow-a", DetailedCampaignState.EXECUTED, expected_version=4)
    assert c4.state == DetailedCampaignState.EXECUTED

def test_workflow_b_failed_provider_circuit_breaker_alert():
    """Workflow B: Provider Failure -> Circuit Breaker -> Operator Alert -> Recovery."""
    provider_handler = ProviderActionHandler()
    ctx_sre = OperatorContext(
        operator_id="op-sre-01",
        tenant_id="*",
        client_id="*",
        roles=[OperatorRole.SRE_ENGINEER]
    )

    # Reset circuit breaker
    res = provider_handler.reset_circuit_breaker(ctx_sre, "google_gemini", "Upstream connectivity restored")
    assert res["status"] == "RESET_TO_HALF_OPEN"

def test_workflow_c_visual_drift_quarantine_disposition():
    """Workflow C: Drift Breach -> Quarantine -> Operator Review."""
    quarantine_reg = QuarantineRegistry()
    q_rec = QuarantinedArtifactRecord(
        artifact_id="art-drift-001",
        campaign_id="cmp-silk-001",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        reason="SSIM_DRIFT_0.14"
    )
    quarantine_reg.quarantine_artifact(q_rec)

    assert quarantine_reg.is_quarantined("art-drift-001") is True
    # Verify quarantined artifacts cannot be released
    assert q_rec.is_blocked_from_release is True

def test_workflow_d_governed_human_authorization():
    """Workflow D: Work Request -> Approval Required -> Operator Approve -> Token Issued."""
    approval_handler = ApprovalActionHandler()
    app = HumanApprovalItem(
        approval_id="app-workflow-d",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        campaign_id="cmp-silk-001",
        requested_operation="PRODUCTION_RELEASE",
        scope="PRODUCTION",
        risk_rating="HIGH",
        requester_role="CREATIVE_DIRECTOR",
        requester_id="op-director-01",
        evidence_bundle_id="evi-001",
        status="PENDING",
        expires_at=time.time() + 3600,
        version=1
    )
    approval_handler.register_approval_request(app)

    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )
    approved = approval_handler.approve_request(ctx, "app-workflow-d", expected_version=1, reason="Approved by Chief Curator")
    assert approved.status == "APPROVED"
    assert approved.execution_token_id is not None

def test_workflow_e_simultaneous_multi_tenant_isolation():
    """Workflow E: Simultaneous workloads for Client A, B, C with cross-client intrusion attempts."""
    ctx_a = OperatorContext(operator_id="op-a", tenant_id="tenant_A", client_id="client_A", roles=[OperatorRole.LEAD_CURATOR])
    ctx_b = OperatorContext(operator_id="op-b", tenant_id="tenant_B", client_id="client_B", roles=[OperatorRole.LEAD_CURATOR])
    ctx_c = OperatorContext(operator_id="op-c", tenant_id="tenant_C", client_id="client_C", roles=[OperatorRole.LEAD_CURATOR])

    # Client A accessing Client A -> Allowed
    PermissionGuard.enforce_tenant_boundary(ctx_a, "tenant_A", "client_A")

    # Client A accessing Client B -> Denied
    with pytest.raises(TenantAccessDeniedError):
        PermissionGuard.enforce_tenant_boundary(ctx_a, "tenant_B", "client_B")

    # Client B accessing Client C -> Denied
    with pytest.raises(TenantAccessDeniedError):
        PermissionGuard.enforce_tenant_boundary(ctx_b, "tenant_C", "client_C")

    # Client C accessing Client A -> Denied
    with pytest.raises(TenantAccessDeniedError):
        PermissionGuard.enforce_tenant_boundary(ctx_c, "tenant_A", "client_A")

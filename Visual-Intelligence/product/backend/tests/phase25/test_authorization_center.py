"""
Phase 25 Human Authorization Center Tests.
"""
import pytest
import time
from src.control_plane.models import OperatorRole
from src.control_plane.context import OperatorContext
from src.control_plane.exceptions import StaleActionConflictError, ControlPlaneError, UnauthorizedOperatorActionError
from src.authorization_center.approval_projection import HumanApprovalItem
from src.authorization_center.approval_actions import ApprovalActionHandler
from src.authorization_center.approval_expiry import ApprovalExpiryEvaluator
from src.authorization_center.approval_service import HumanAuthorizationCenterService

def test_approval_lifecycle_and_execution_token():
    service = HumanAuthorizationCenterService()
    handler = service.action_handler

    app = HumanApprovalItem(
        approval_id="app-100",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        campaign_id="cmp-silk-001",
        requested_operation="RELEASE_CAMPAIGN",
        scope="PRODUCTION",
        risk_rating="HIGH",
        requester_role="CREATIVE_DIRECTOR",
        requester_id="op-director-01",
        evidence_bundle_id="evi-bundle-001",
        status="PENDING",
        expires_at=time.time() + 3600,
        version=1
    )
    handler.register_approval_request(app)

    ctx_curator = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    # Approve
    approved = handler.approve_request(ctx_curator, "app-100", expected_version=1, reason="Quality certified")
    assert approved.status == "APPROVED"
    assert approved.execution_token_id.startswith("tok-")
    assert approved.version == 2

    # Revoke approval
    revoked = handler.revoke_approval(ctx_curator, "app-100", expected_version=2, reason="Client change request")
    assert revoked.status == "REVOKED"
    assert revoked.execution_token_id is None # Execution token cleared
    assert revoked.version == 3

def test_expired_approval_rejection():
    service = HumanAuthorizationCenterService()
    handler = service.action_handler

    app = HumanApprovalItem(
        approval_id="app-expired-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        campaign_id="cmp-silk-001",
        requested_operation="RELEASE",
        scope="PRODUCTION",
        risk_rating="HIGH",
        requester_role="CREATIVE_DIRECTOR",
        requester_id="op-director-01",
        evidence_bundle_id="evi-bundle-001",
        status="PENDING",
        expires_at=time.time() - 10.0, # Expired in past
        version=1
    )
    handler.register_approval_request(app)

    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    # Approving expired request must fail
    with pytest.raises(ControlPlaneError):
        handler.approve_request(ctx, "app-expired-01", expected_version=1)

def test_unauthorized_role_cannot_approve():
    service = HumanAuthorizationCenterService()
    handler = service.action_handler

    app = HumanApprovalItem(
        approval_id="app-200",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        campaign_id="cmp-silk-001",
        requested_operation="RELEASE",
        scope="PRODUCTION",
        risk_rating="HIGH",
        requester_role="CREATIVE_DIRECTOR",
        requester_id="op-director-01",
        evidence_bundle_id="evi-bundle-001",
        status="PENDING",
        expires_at=time.time() + 3600,
        version=1
    )
    handler.register_approval_request(app)

    ctx_sre = OperatorContext(
        operator_id="op-sre-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.SRE_ENGINEER]
    )

    with pytest.raises(UnauthorizedOperatorActionError):
        handler.approve_request(ctx_sre, "app-200", expected_version=1)

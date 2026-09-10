"""
Tests for Phase 27 Review Engine and Approval Bridge.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.campaign_studio.review import StudioReviewEngine
from src.campaign_studio.approval import StudioApprovalBridge, StudioApprovalStatus


def test_multi_dimensional_review():
    engine = StudioReviewEngine()
    campaign_id = "camp_rev_01"
    asset_id = "ast_01"

    critique = engine.evaluate_asset(campaign_id, asset_id)
    assert critique.overall_score >= 0.85
    assert critique.is_passed is True
    assert len(critique.dimension_scores) == 5


def test_approval_bridge_role_enforcement():
    bridge = StudioApprovalBridge()
    campaign_id = "camp_appr_01"
    asset_id = "ast_01"

    req = bridge.create_approval_request(
        campaign_id=campaign_id,
        asset_id=asset_id,
        requested_by="op_staff_01",
        required_role=OperatorRole.CREATIVE_DIRECTOR,
    )
    assert req.status == StudioApprovalStatus.PENDING

    # Unauthorized operator (e.g. STAFF_OPERATOR) attempting approval must be rejected
    unauth_op = OperatorContext(
        operator_id="op_intern_01",
        role=OperatorRole.STAFF_OPERATOR,
        department="Creative Direction",
    )
    with pytest.raises(PermissionError) as exc_info:
        bridge.submit_decision(req.approval_id, unauth_op, StudioApprovalStatus.APPROVED, "Self-approved")
    assert "not authorized to approve" in str(exc_info.value)

    # Authorized operator (CREATIVE_DIRECTOR) succeeds
    auth_op = OperatorContext(
        operator_id="op_cd_01",
        role=OperatorRole.CREATIVE_DIRECTOR,
        department="Creative Direction",
    )
    decided = bridge.submit_decision(req.approval_id, auth_op, StudioApprovalStatus.APPROVED, "Verified color accuracy")
    assert decided.status == StudioApprovalStatus.APPROVED
    assert decided.approver_id == "op_cd_01"

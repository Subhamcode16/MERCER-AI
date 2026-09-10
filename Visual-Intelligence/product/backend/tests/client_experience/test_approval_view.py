"""
Unit tests for Phase 16 Approval Center View.
"""

import pytest
from src.client_experience.approval_view import ApprovalCenterView
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_approval_view_routing(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "appr_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")
    orch.launch_campaign("client_nocap", "camp_001", "brand_nocap", "Fall Drop", "Awareness")

    orch.submit_deliverable_for_human_approval(
        requesting_client_id="client_nocap",
        approval_id="appr_001",
        campaign_id="camp_001",
        workstream_id="ws_001",
        deliverable_id="del_001",
        proposed_action="Publish Post",
        capability="publish_post",
        target_platform="instagram"
    )

    view = ApprovalCenterView()
    user = UserIdentity("user_owner", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    pending = view.list_pending_approvals(user, orch)
    assert len(pending) == 1
    assert pending[0].approval_id == "appr_001"

    decision_dto = view.submit_human_decision(user, orch, "appr_001", approved=True)
    assert decision_dto.status == "APPROVED"

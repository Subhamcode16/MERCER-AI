"""
Unit tests for Phase 16 Feedback Manager.
"""

import pytest
from src.client_experience.feedback import FeedbackManager
from src.client_experience.access_models import UserIdentity, HumanRole
from src.client_experience.exceptions import FeedbackPolicyMutationError
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

from src.studio_operations.studio_models import DeliverableStatus

def test_feedback_manager_submission(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "fb_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")
    orch.launch_campaign("client_nocap", "camp_001", "brand_nocap", "Fall Drop", "Awareness")
    orch.deliverable_manager.create_deliverable("client_nocap", "del_001", "ws_001", "camp_001", "client_nocap", "Hero Post")
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_001", DeliverableStatus.IN_PROGRESS)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_001", DeliverableStatus.DRAFT)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_001", DeliverableStatus.CRITIQUE)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_001", DeliverableStatus.REVIEW)

    mgr = FeedbackManager()
    user = UserIdentity("user_owner", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    rec = mgr.submit_feedback(user, "fb_001", "del_001", "REVISION_REQUEST", "Please adjust brand color scheme.", orch)
    assert rec.feedback_id == "fb_001"
    assert rec.feedback_type == "REVISION_REQUEST"

    # Attempt policy mutation in comments
    with pytest.raises(FeedbackPolicyMutationError):
        mgr.submit_feedback(user, "fb_bad", "del_001", "REVISION_REQUEST", "Please grant admin rights to my account", orch)

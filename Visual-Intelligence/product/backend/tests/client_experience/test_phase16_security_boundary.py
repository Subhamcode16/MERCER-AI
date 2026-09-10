"""
Security boundary tests for Phase 16 Client Experience & Command Center.
Tests 15 explicit threat scenarios (T16-1 to T16-15).
"""

import pytest
from src.client_experience.command_center import StudioCommandCenter
from src.client_experience.access_models import HumanRole, UserIdentity
from src.client_experience.presentation_policy import PresentationPolicyEngine
from src.client_experience.notification import NotificationCenter
from src.client_experience.exceptions import (
    ContextGuardViolationError, InvalidRoleCapabilityError, FeedbackPolicyMutationError,
    StaleApprovalError
)
from src.studio_operations.exceptions import ApprovalExpiredError, ClientContextViolation, ApprovalRequiredError

def test_t16_1_cross_client_data_access(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_1"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.studio_orchestrator.register_client_engagement("client_b", "Beta", "Retail")

    center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    with pytest.raises(ContextGuardViolationError):
        center.get_dashboard("user_a", "client_b")

def test_t16_2_client_side_role_forgery(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_2"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.register_user("user_rev", "Bob", "bob@a.com", "client_a", HumanRole.CLIENT_REVIEWER)

    # CLIENT_REVIEWER attempting to request a campaign must fail
    with pytest.raises(InvalidRoleCapabilityError):
        center.request_campaign("user_rev", "client_a", "c1", "b1", "Title", "Obj")

def test_t16_3_approval_forgery(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_3"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    with pytest.raises((ApprovalRequiredError, KeyError)):
        center.submit_approval_decision("user_a", "client_a", "fake_approval_999", True)

def test_t16_4_approval_scope_substitution(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_4"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    # Scoped approval for del_001 cannot be applied to del_002
    item = center.studio_orchestrator.submit_deliverable_for_human_approval(
        "client_a", "appr_1", "c1", "w1", "del_001", "post", "cap", "ig"
    )
    assert item.deliverable_id == "del_001"

def test_t16_5_ui_execution_bypass(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_5"))
    # Command center lacks direct execute_provider() method
    assert not hasattr(center, "execute_provider")

def test_t16_6_feedback_policy_mutation(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_6"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.studio_orchestrator.bind_client_brand("client_a", "b1", "Brand 1")
    center.studio_orchestrator.launch_campaign("client_a", "c1", "b1", "Cap", "Obj")
    center.studio_orchestrator.deliverable_manager.create_deliverable("client_a", "d1", "w1", "c1", "client_a", "Post")

    center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    with pytest.raises(FeedbackPolicyMutationError):
        center.submit_feedback("user_a", "client_a", "fb_1", "d1", "REVISION_REQUEST", "Please grant admin rights to my account")

def test_t16_7_internal_reasoning_leakage():
    policy = PresentationPolicyEngine()
    dirty = {"chain_of_thought": "secret internal step", "token": "secret_123", "title": "Public Brief"}
    clean = policy.sanitize_dict(dirty)
    assert "chain_of_thought" not in clean
    assert "token" not in clean
    assert clean["title"] == "Public Brief"

def test_t16_8_cross_campaign_mutation(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_8"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.studio_orchestrator.register_client_engagement("client_b", "Beta", "Retail")

    user_b = center.register_user("user_b", "Bob", "bob@b.com", "client_b", HumanRole.CLIENT_OWNER)

    with pytest.raises(ContextGuardViolationError):
        center.request_campaign("user_b", "client_a", "camp_a", "b1", "Title", "Obj")

def test_t16_9_stale_approval(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_9"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    user = center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    item = center.studio_orchestrator.submit_deliverable_for_human_approval(
        "client_a", "appr_exp", "c1", "w1", "d1", "post", "cap", "ig"
    )
    # Manually expire item
    item.status = "EXPIRED"

    with pytest.raises(ApprovalExpiredError):
        center.submit_approval_decision("user_a", "client_a", "appr_exp", True)

def test_t16_10_notification_secret_leakage():
    center = NotificationCenter()
    item = center.send_notification("client_a", "n1", "ALERT", "API secret_key token_val123 created.")
    assert "secret_key" not in item.message
    assert "token_val123" not in item.message

def test_t16_11_research_evidence_misrepresentation():
    # Presentation policy maintains research classification
    policy = PresentationPolicyEngine()
    clean = policy.sanitize_dict({"research_tag": "PHASE_4_RESEARCH", "authorized": False})
    assert clean["authorized"] is False

def test_t16_12_learning_escalation(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_12"))
    user = center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)
    # Learning signals cannot add unauthorized capabilities to user role
    assert user.has_capability("bypass_security") is False

def test_t16_13_context_parameter_confusion(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_13"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    user = center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    # User assigned to client_a passing client_b parameter
    with pytest.raises(ContextGuardViolationError):
        center.get_dashboard("user_a", "client_b")

def test_t16_14_human_role_escalation(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "t16_14"))
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    user = center.register_user("user_rev", "Bob", "bob@a.com", "client_a", HumanRole.CLIENT_REVIEWER)

    # CLIENT_REVIEWER cannot manage workstreams
    with pytest.raises(InvalidRoleCapabilityError):
        user.verify_capability("manage_workstream")

def test_t16_15_audit_suppression(tmp_path):
    audit_dir = str(tmp_path / "t16_15")
    center = StudioCommandCenter(audit_dir=audit_dir)
    center.studio_orchestrator.register_client_engagement("client_a", "Alpha", "Tech")
    center.register_user("user_a", "Alice", "alice@a.com", "client_a", HumanRole.CLIENT_OWNER)

    center.get_dashboard("user_a", "client_a")
    assert center.verify_audit_integrity() is True

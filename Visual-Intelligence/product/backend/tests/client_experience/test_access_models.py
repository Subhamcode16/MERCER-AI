"""
Unit tests for Phase 16 Access Models and Role Capability Allowlists.
"""

import pytest
from src.client_experience.access_models import UserIdentity, HumanRole, ROLE_CAPABILITIES
from src.client_experience.exceptions import InvalidRoleCapabilityError, ClientAccessDeniedError

def test_user_identity_validation():
    user = UserIdentity("user_01", "Alice", "alice@nocap.fashion", "client_nocap", HumanRole.CLIENT_OWNER)
    assert user.user_id == "user_01"
    assert user.role == HumanRole.CLIENT_OWNER
    assert user.has_capability("approve_deliverable") is True

    with pytest.raises(ClientAccessDeniedError):
        UserIdentity("", "Alice", "alice@nocap.fashion", "client_nocap", HumanRole.CLIENT_OWNER)

def test_role_capability_enforcement():
    reviewer = UserIdentity("user_rev", "Bob", "bob@nocap.fashion", "client_nocap", HumanRole.CLIENT_REVIEWER)
    assert reviewer.has_capability("approve_deliverable") is True
    assert reviewer.has_capability("request_campaign") is False

    with pytest.raises(InvalidRoleCapabilityError):
        reviewer.verify_capability("request_campaign")

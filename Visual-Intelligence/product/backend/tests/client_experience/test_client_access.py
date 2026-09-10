"""
Unit tests for Phase 16 Client Access Manager.
"""

import pytest
from src.client_experience.client_access import ClientAccessManager
from src.client_experience.access_models import HumanRole
from src.client_experience.exceptions import ContextGuardViolationError, InvalidRoleCapabilityError

def test_client_access_manager_flow():
    mgr = ClientAccessManager()
    mgr.register_user("user_a", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    user = mgr.authenticate_and_authorize("user_a", "client_nocap", "request_campaign")
    assert user.user_id == "user_a"

    # Cross-client attempt
    with pytest.raises(ContextGuardViolationError):
        mgr.authenticate_and_authorize("user_a", "client_other", "request_campaign")

    # Unauthorized capability
    with pytest.raises(InvalidRoleCapabilityError):
        mgr.authenticate_and_authorize("user_a", "client_nocap", "manage_workstream")

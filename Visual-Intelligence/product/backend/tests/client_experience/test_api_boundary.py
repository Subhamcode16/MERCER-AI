"""
Unit tests for Phase 16 Client Experience API Boundary.
"""

import pytest
from src.client_experience.api_boundary import ClientExperienceAPIBoundary
from src.client_experience.access_models import UserIdentity, HumanRole
from src.client_experience.exceptions import ContextGuardViolationError, InvalidRoleCapabilityError

def test_api_boundary_validation():
    boundary = ClientExperienceAPIBoundary()
    user = UserIdentity("user_a", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    def dummy_handler(x):
        return x * 2

    res = boundary.process_request(user, "client_nocap", "view_dashboard", dummy_handler, 5)
    assert res == 10

    # Context guard violation
    with pytest.raises(ContextGuardViolationError):
        boundary.process_request(user, "client_other", "view_dashboard", dummy_handler, 5)

    # Capability check failure
    with pytest.raises(InvalidRoleCapabilityError):
        boundary.process_request(user, "client_nocap", "manage_workstream", dummy_handler, 5)

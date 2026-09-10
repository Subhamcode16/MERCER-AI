"""
Unit tests for Phase 16 Client Context Guard.
"""

import pytest
from src.client_experience.context_guard import ClientContextGuard
from src.client_experience.access_models import UserIdentity, HumanRole
from src.client_experience.exceptions import ContextGuardViolationError

def test_context_guard_isolation():
    guard = ClientContextGuard()
    user_a = UserIdentity("user_a", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    guard.verify_access(user_a, "client_nocap")

    with pytest.raises(ContextGuardViolationError):
        guard.verify_access(user_a, "client_beta")

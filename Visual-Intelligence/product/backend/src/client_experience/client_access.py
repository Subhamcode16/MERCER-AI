"""
Phase 16 Client Access Manager.
Manages user authentication contexts, role assignments, and capability enforcement.
"""

from typing import Dict, Optional
from src.client_experience.access_models import UserIdentity, HumanRole
from src.client_experience.context_guard import ClientContextGuard
from src.client_experience.exceptions import ClientAccessDeniedError

class ClientAccessManager:
    """Manager validating user identities, role capabilities, and client scopes."""

    def __init__(self, context_guard: Optional[ClientContextGuard] = None):
        self.context_guard = context_guard or ClientContextGuard()
        self._users: Dict[str, UserIdentity] = {}

    def register_user(self, user_id: str, name: str, email: str, assigned_client_id: str, role: HumanRole) -> UserIdentity:
        """Registers a user identity."""
        user = UserIdentity(user_id=user_id, name=name, email=email, assigned_client_id=assigned_client_id, role=role)
        self._users[user_id] = user
        return user

    def authenticate_and_authorize(self, user_id: str, target_client_id: str, required_capability: str) -> UserIdentity:
        """Authenticates user, verifies client scope, and enforces capability check."""
        if user_id not in self._users:
            raise ClientAccessDeniedError(f"User '{user_id}' not found.")
        user = self._users[user_id]

        # 1. Verify client isolation guard
        self.context_guard.verify_access(user, target_client_id)

        # 2. Verify explicit capability allowlist
        user.verify_capability(required_capability)

        return user

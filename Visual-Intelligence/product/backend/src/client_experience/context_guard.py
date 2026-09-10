"""
Phase 16 Client Context Guard.
Enforces server-side fail-closed cross-client isolation (INV-16-003).
"""

from src.client_experience.exceptions import ContextGuardViolationError
from src.client_experience.access_models import UserIdentity

class ClientContextGuard:
    """Guard verifying server-side client isolation boundaries."""

    def verify_access(self, user: UserIdentity, target_client_id: str) -> None:
        """Enforces that a user operates strictly within their assigned client scope."""
        if not user or not target_client_id:
            raise ContextGuardViolationError("User identity and target client ID are required.")

        if user.assigned_client_id != target_client_id:
            raise ContextGuardViolationError(
                f"CROSS-CLIENT VIOLATION: User '{user.user_id}' (client '{user.assigned_client_id}') "
                f"attempted to access target client '{target_client_id}'."
            )

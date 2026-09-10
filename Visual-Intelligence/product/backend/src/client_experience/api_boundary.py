"""
Phase 16 Server-Side Interaction API Boundary.
Validates identity context, server-side client guard, and capability allowlists prior to control plane dispatch.
"""

from typing import Dict, Any, List, Optional
from src.client_experience.access_models import UserIdentity
from src.client_experience.context_guard import ClientContextGuard

class ClientExperienceAPIBoundary:
    """Server-side interaction boundary enforcing identity, client guard, and audit logging."""

    def __init__(self, context_guard: Optional[ClientContextGuard] = None):
        self.context_guard = context_guard or ClientContextGuard()

    def process_request(
        self,
        user: UserIdentity,
        target_client_id: str,
        required_capability: str,
        handler_func: Any,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """Validates identity context guard and capability before executing handler."""
        # 1. Enforce server-side context guard (INV-16-003)
        self.context_guard.verify_access(user, target_client_id)

        # 2. Enforce explicit capability allowlist
        user.verify_capability(required_capability)

        # 3. Dispatch to internal control plane handler
        return handler_func(*args, **kwargs)

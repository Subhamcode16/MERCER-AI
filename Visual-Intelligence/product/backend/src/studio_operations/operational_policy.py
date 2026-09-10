"""
Phase 15 Operational Policy Engine.
Enforces client-specific operational rules while ensuring baseline security restrictions are never weakened.
"""

from typing import Dict, List, Optional
from src.studio_operations.exceptions import OperationalPolicyViolation, ClientContextViolation
from src.studio_operations.studio_models import ClientOperatingPolicy

class StudioOperationalPolicyEngine:
    """Validates operational actions against client operating policies."""

    def validate_action(
        self,
        requesting_client_id: str,
        policy: ClientOperatingPolicy,
        action_name: str,
        target_platform: Optional[str] = None,
        capability: Optional[str] = None
    ) -> bool:
        """Validates if an action is permitted under the client's operating policy."""
        if requesting_client_id != policy.client_id:
            raise ClientContextViolation(
                f"Policy validation failed: context '{requesting_client_id}' != policy client '{policy.client_id}'."
            )

        # Check allowed platforms
        if target_platform and target_platform not in policy.allowed_platforms:
            raise OperationalPolicyViolation(
                f"Platform '{target_platform}' is not permitted by client policy for '{policy.client_id}'."
            )

        # Check allowed capabilities
        if capability and capability not in policy.allowed_capabilities:
            raise OperationalPolicyViolation(
                f"Capability '{capability}' is not permitted by client policy for '{policy.client_id}'."
            )

        return True

    def validate_revision_limit(self, policy: ClientOperatingPolicy, current_revisions: int) -> bool:
        """Enforces revision ceiling."""
        effective_max = min(policy.max_revisions_override, 3)  # Baseline ceiling = 3
        if current_revisions >= effective_max:
            raise OperationalPolicyViolation(
                f"Revision count {current_revisions} exceeds maximum allowed ceiling of {effective_max}."
            )
        return True

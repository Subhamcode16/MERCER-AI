"""
Phase 17 Bounded Autonomy Controller.
Manages explicit autonomy tiers (Tier 0 to Tier 3) governing autonomous operational continuation.
Enforces INV-17-001 & INV-17-003: No tier may bypass Phase 10 Human Authorization.
"""

from typing import Dict, Any, Optional
from src.production_fabric.exceptions import ContinuationBoundaryError, FabricInvariantViolation

class BoundedAutonomyController:
    """Controller enforcing autonomy tier rules and policy boundaries."""

    def __init__(self, client_tiers: Optional[Dict[str, int]] = None):
        self._client_tiers: Dict[str, int] = client_tiers or {}

    def get_tier(self, client_id: str) -> int:
        return self._client_tiers.get(client_id, 1)  # Default Tier 1: Prepare and recommend

    def set_tier(self, client_id: str, tier: int) -> None:
        if tier < 0 or tier > 3:
            raise ContinuationBoundaryError(f"Invalid autonomy tier '{tier}'. Must be 0, 1, 2, or 3.")
        self._client_tiers[client_id] = tier

    def verify_action_permitted(
        self,
        client_id: str,
        action_name: str,
        requires_human_auth: bool
    ) -> bool:
        """Verifies if an action is permitted under the client's autonomy tier."""
        tier = self.get_tier(client_id)

        # If action requires human authorization, NO tier can issue authority
        if requires_human_auth:
            raise ContinuationBoundaryError(
                f"Action '{action_name}' requires explicit Phase 10 Human Authorization. Autonomy Tier {tier} cannot bypass this."
            )

        if tier == 0 and action_name != "OBSERVE":
            raise ContinuationBoundaryError(f"Autonomy Tier 0 permits observation only. Action '{action_name}' rejected.")

        if tier == 1 and action_name not in ("OBSERVE", "PREPARE", "RECOMMEND", "CRITIQUE", "REVIEW"):
            raise ContinuationBoundaryError(f"Autonomy Tier 1 permits prepare/recommend only. Action '{action_name}' rejected.")

        return True

"""
Phase 15/16 Human Access & Role Capability Models.
Strict explicit role allowlists with fail-closed validation and zero wildcard capabilities.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set, List
from src.client_experience.exceptions import InvalidRoleCapabilityError, ClientAccessDeniedError

class HumanRole(str, Enum):
    CLIENT_OWNER = "CLIENT_OWNER"
    CLIENT_EDITOR = "CLIENT_EDITOR"
    CLIENT_REVIEWER = "CLIENT_REVIEWER"
    STUDIO_OPERATOR = "STUDIO_OPERATOR"
    CREATIVE_DIRECTOR = "CREATIVE_DIRECTOR"
    QUALITY_REVIEWER = "QUALITY_REVIEWER"
    OBSERVABILITY_VIEWER = "OBSERVABILITY_VIEWER"

# Explicit capability allowlist per human role - NO WILDCARD CAPABILITIES
ROLE_CAPABILITIES: Dict[HumanRole, Set[str]] = {
    HumanRole.CLIENT_OWNER: {
        "view_dashboard", "request_campaign", "review_deliverable",
        "submit_feedback", "approve_deliverable", "reject_deliverable",
        "view_performance", "view_timeline", "view_brand"
    },
    HumanRole.CLIENT_EDITOR: {
        "view_dashboard", "request_campaign", "review_deliverable",
        "submit_feedback", "view_timeline", "view_brand"
    },
    HumanRole.CLIENT_REVIEWER: {
        "view_dashboard", "review_deliverable", "approve_deliverable",
        "reject_deliverable", "submit_feedback", "view_timeline"
    },
    HumanRole.STUDIO_OPERATOR: {
        "view_dashboard", "view_workforce", "manage_campaign",
        "manage_workstream", "view_timeline", "view_performance", "view_brand"
    },
    HumanRole.CREATIVE_DIRECTOR: {
        "view_dashboard", "view_brand", "create_direction",
        "review_deliverable", "view_timeline", "view_workforce"
    },
    HumanRole.QUALITY_REVIEWER: {
        "view_dashboard", "review_deliverable", "critique_deliverable",
        "view_timeline"
    },
    HumanRole.OBSERVABILITY_VIEWER: {
        "view_dashboard", "view_timeline", "view_performance"
    },
}

@dataclass(frozen=True)
class UserIdentity:
    user_id: str
    name: str
    email: str
    assigned_client_id: str
    role: HumanRole

    def __post_init__(self):
        if not self.user_id or not self.user_id.strip():
            raise ClientAccessDeniedError("user_id cannot be empty.")
        if not self.assigned_client_id or not self.assigned_client_id.strip():
            raise ClientAccessDeniedError("assigned_client_id cannot be empty.")

    def has_capability(self, capability: str) -> bool:
        """Returns True if the capability is explicitly in the role allowlist."""
        allowed = ROLE_CAPABILITIES.get(self.role, set())
        return capability in allowed

    def verify_capability(self, capability: str) -> None:
        """Enforces capability check; raises InvalidRoleCapabilityError if absent."""
        if not self.has_capability(capability):
            raise InvalidRoleCapabilityError(
                f"Role '{self.role.value}' for user '{self.user_id}' lacks required capability '{capability}'."
            )

"""
Phase 25 Role-Based Navigation and Menu Resolver.
"""
from typing import List, Dict, Any
from src.control_plane.models import OperatorRole

MENU_REGISTRY: Dict[str, Dict[str, Any]] = {
    "dashboard": {"label": "Command Center", "path": "/console/dashboard", "roles": set(OperatorRole)},
    "campaigns": {"label": "Campaigns", "path": "/console/campaigns", "roles": {OperatorRole.STUDIO_ADMIN, OperatorRole.LEAD_CURATOR, OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_STRATEGIST, OperatorRole.READ_ONLY_VIEWER}},
    "approvals": {"label": "Authorization Center", "path": "/console/approvals", "roles": {OperatorRole.STUDIO_ADMIN, OperatorRole.LEAD_CURATOR}},
    "intelligence": {"label": "Intelligence Observatory", "path": "/console/intelligence", "roles": set(OperatorRole)},
    "visual": {"label": "Visual Observatory", "path": "/console/visual", "roles": set(OperatorRole)},
    "reliability": {"label": "Reliability & SRE", "path": "/console/reliability", "roles": {OperatorRole.STUDIO_ADMIN, OperatorRole.SRE_ENGINEER, OperatorRole.READ_ONLY_VIEWER}},
    "providers": {"label": "Providers & MCP", "path": "/console/providers", "roles": {OperatorRole.STUDIO_ADMIN, OperatorRole.SRE_ENGINEER}},
    "evidence": {"label": "Evidence Explorer", "path": "/console/evidence", "roles": set(OperatorRole)}
}

class NavigationResolver:
    @staticmethod
    def resolve_navigation_menu(roles: List[OperatorRole]) -> List[Dict[str, Any]]:
        user_roles = set(roles)
        items = []
        for key, conf in MENU_REGISTRY.items():
            if conf["roles"].intersection(user_roles):
                items.append({
                    "id": key,
                    "label": conf["label"],
                    "path": conf["path"]
                })
        return items

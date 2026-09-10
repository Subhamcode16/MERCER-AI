"""
Phase 25 Server-Side Operator Permissions & Capability Engine.
"""
from typing import List, Set, Dict
from src.control_plane.models import OperatorRole, OperatorCapability
from src.control_plane.context import OperatorContext
from src.control_plane.exceptions import UnauthorizedOperatorActionError, TenantAccessDeniedError

ROLE_CAPABILITY_MATRIX: Dict[OperatorRole, Set[OperatorCapability]] = {
    OperatorRole.STUDIO_ADMIN: set(OperatorCapability), # Full administrative capabilities
    OperatorRole.LEAD_CURATOR: {
        OperatorCapability.VIEW_CLIENT,
        OperatorCapability.VIEW_CAMPAIGN,
        OperatorCapability.VIEW_DELIVERABLE,
        OperatorCapability.VIEW_INTELLIGENCE,
        OperatorCapability.VIEW_EVIDENCE,
        OperatorCapability.SUBMIT_FEEDBACK,
        OperatorCapability.REQUEST_APPROVAL,
        OperatorCapability.APPROVE,
        OperatorCapability.REJECT,
        OperatorCapability.REVOKE_APPROVAL,
        OperatorCapability.TRIGGER_REVIEW,
        OperatorCapability.OPERATE_CAMPAIGN,
        OperatorCapability.VIEW_COST
    },
    OperatorRole.CREATIVE_DIRECTOR: {
        OperatorCapability.VIEW_CLIENT,
        OperatorCapability.VIEW_CAMPAIGN,
        OperatorCapability.VIEW_DELIVERABLE,
        OperatorCapability.VIEW_INTELLIGENCE,
        OperatorCapability.VIEW_EVIDENCE,
        OperatorCapability.SUBMIT_FEEDBACK,
        OperatorCapability.REQUEST_APPROVAL,
        OperatorCapability.TRIGGER_REVIEW,
        OperatorCapability.OPERATE_CAMPAIGN
    },
    OperatorRole.BRAND_STRATEGIST: {
        OperatorCapability.VIEW_CLIENT,
        OperatorCapability.VIEW_CAMPAIGN,
        OperatorCapability.VIEW_DELIVERABLE,
        OperatorCapability.VIEW_INTELLIGENCE,
        OperatorCapability.SUBMIT_FEEDBACK,
        OperatorCapability.REQUEST_APPROVAL
    },
    OperatorRole.SRE_ENGINEER: {
        OperatorCapability.VIEW_CLIENT,
        OperatorCapability.VIEW_RELIABILITY,
        OperatorCapability.VIEW_PROVIDER_HEALTH,
        OperatorCapability.VIEW_EVIDENCE,
        OperatorCapability.VIEW_COST,
        OperatorCapability.MANAGE_CIRCUIT_BREAKER,
        OperatorCapability.TRIGGER_RECOVERY_DRILL
    },
    OperatorRole.READ_ONLY_VIEWER: {
        OperatorCapability.VIEW_CLIENT,
        OperatorCapability.VIEW_CAMPAIGN,
        OperatorCapability.VIEW_DELIVERABLE,
        OperatorCapability.VIEW_INTELLIGENCE,
        OperatorCapability.VIEW_RELIABILITY,
        OperatorCapability.VIEW_EVIDENCE
    }
}

class PermissionGuard:
    """Authoritative server-side capability and tenant validation."""

    @staticmethod
    def resolve_capabilities(roles: List[OperatorRole]) -> Set[OperatorCapability]:
        caps: Set[OperatorCapability] = set()
        for r in roles:
            caps.update(ROLE_CAPABILITY_MATRIX.get(r, set()))
        return caps

    @staticmethod
    def enforce_capability(context: OperatorContext, required_capability: OperatorCapability) -> None:
        context.validate()
        user_caps = PermissionGuard.resolve_capabilities(context.roles)
        if required_capability not in user_caps:
            raise UnauthorizedOperatorActionError(
                f"Operator '{context.operator_id}' with roles {[r.value for r in context.roles]} "
                f"lacks required capability: {required_capability.value}"
            )

    @staticmethod
    def enforce_tenant_boundary(context: OperatorContext, target_tenant: str, target_client: str) -> None:
        context.validate()
        # Admin wildcard tenant
        if context.tenant_id == "*":
            return
        if context.tenant_id != target_tenant:
            raise TenantAccessDeniedError(
                f"Cross-tenant access forbidden: Operator tenant '{context.tenant_id}' cannot access target tenant '{target_tenant}'."
            )
        if context.client_id != "*" and context.client_id != target_client:
            raise TenantAccessDeniedError(
                f"Cross-client access forbidden: Operator client '{context.client_id}' cannot access target client '{target_client}'."
            )

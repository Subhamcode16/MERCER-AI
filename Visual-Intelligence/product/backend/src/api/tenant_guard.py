"""
Phase 25 API Tenant Guard Middleware / Dependency.
"""
from fastapi import HTTPException
from src.control_plane.context import OperatorContext
from src.control_plane.permissions import PermissionGuard
from src.control_plane.exceptions import TenantAccessDeniedError

class APITenantGuard:
    @staticmethod
    def verify_tenant_access(context: OperatorContext, requested_tenant: str, requested_client: str) -> None:
        try:
            PermissionGuard.enforce_tenant_boundary(context, requested_tenant, requested_client)
        except TenantAccessDeniedError as e:
            raise HTTPException(status_code=403, detail=str(e))

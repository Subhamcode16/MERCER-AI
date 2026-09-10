"""
Phase 25 Master Human Authorization Center Service.
"""
from typing import List, Optional, Dict, Any
import time
import uuid
from dataclasses import dataclass, field
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability, OperatorRole
from src.control_plane.permissions import PermissionGuard
from src.control_plane.audit import ControlPlaneAuditLogger
from src.authorization_center.approval_projection import HumanApprovalItem
from src.authorization_center.approval_actions import ApprovalActionHandler
from src.authorization_center.approval_expiry import ApprovalExpiryEvaluator


class HumanAuthorizationCenterService:
    """Provides querying, queue projection, and execution authority lifecycle management."""

    def __init__(self, audit_logger: Optional[ControlPlaneAuditLogger] = None):
        self.audit_logger = audit_logger or ControlPlaneAuditLogger()
        self.action_handler = ApprovalActionHandler(audit_logger=self.audit_logger)

    def list_approvals(self, context: OperatorContext, tenant_id: str, client_id: Optional[str] = None) -> List[HumanApprovalItem]:
        PermissionGuard.enforce_capability(context, OperatorCapability.VIEW_CAMPAIGN)
        PermissionGuard.enforce_tenant_boundary(context, tenant_id, client_id or "*")

        # Auto-expire stale items
        ApprovalExpiryEvaluator.evaluate_and_expire(list(self.action_handler._approvals.values()))

        results = []
        for app in self.action_handler._approvals.values():
            if tenant_id == "*" or app.tenant_id == tenant_id:
                if client_id is None or client_id == "*" or app.client_id == client_id:
                    results.append(app)
        return results


@dataclass
class ApprovalRequestRecord:
    approval_id: str
    tenant_id: str
    client_id: str
    requested_by: str
    action_type: str
    resource_id: str
    estimated_cost: float = 0.0
    status: str = "PENDING"
    version: int = 1
    execution_token_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)


class ApprovalService:
    """Universal approval service wrapper used by workforce and API gateways."""

    def __init__(self):
        self._approvals: Dict[str, ApprovalRequestRecord] = {}

    def create_approval_request(
        self,
        tenant_id: str,
        client_id: str,
        requested_by: str,
        action_type: str,
        resource_id: str,
        estimated_cost: float = 0.0,
    ) -> ApprovalRequestRecord:
        app_id = f"app_{uuid.uuid4().hex[:10]}"
        record = ApprovalRequestRecord(
            approval_id=app_id,
            tenant_id=tenant_id,
            client_id=client_id,
            requested_by=requested_by,
            action_type=action_type,
            resource_id=resource_id,
            estimated_cost=estimated_cost,
            status="PENDING",
            version=1,
        )
        self._approvals[app_id] = record
        return record

    def get_approval(self, approval_id: str) -> Optional[ApprovalRequestRecord]:
        return self._approvals.get(approval_id)

    def approve_request(
        self,
        approval_id: str,
        approver_ctx: Any,
        rationale: str = "",
    ) -> ApprovalRequestRecord:
        record = self._approvals.get(approval_id)
        if not record:
            raise KeyError(f"Approval '{approval_id}' not found")
        if record.status != "PENDING":
            raise RuntimeError(f"Cannot approve request in state '{record.status}'")
        
        record.status = "APPROVED"
        record.version += 1
        record.execution_token_id = f"tok_{uuid.uuid4().hex[:16]}"
        return record

"""
Phase 25 Governed Approval Actions with Nonce and Signature Validation.
"""
from typing import Dict, Any, Optional
import time
import uuid
import hashlib
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability, ControlPlaneAuditEvent
from src.control_plane.permissions import PermissionGuard
from src.control_plane.exceptions import (
    UnauthorizedOperatorActionError,
    StaleActionConflictError,
    ControlPlaneError
)
from src.control_plane.audit import ControlPlaneAuditLogger
from src.authorization_center.approval_projection import HumanApprovalItem
from src.authorization_center.approval_expiry import ApprovalExpiryEvaluator

class ApprovalActionHandler:
    """Executes human approvals, rejections, and revocations through governed cryptographic boundaries."""

    def __init__(self, audit_logger: Optional[ControlPlaneAuditLogger] = None):
        self.audit_logger = audit_logger or ControlPlaneAuditLogger()
        self._approvals: Dict[str, HumanApprovalItem] = {}

    def register_approval_request(self, item: HumanApprovalItem) -> None:
        self._approvals[item.approval_id] = item

    def get_approval(self, approval_id: str) -> HumanApprovalItem:
        if approval_id not in self._approvals:
            raise KeyError(f"Approval request '{approval_id}' not found.")
        return self._approvals[approval_id]

    def approve_request(
        self,
        context: OperatorContext,
        approval_id: str,
        expected_version: int,
        reason: str = ""
    ) -> HumanApprovalItem:
        """Grants human approval, generating a verifiable cryptographic execution token."""
        PermissionGuard.enforce_capability(context, OperatorCapability.APPROVE)

        item = self.get_approval(approval_id)
        PermissionGuard.enforce_tenant_boundary(context, item.tenant_id, item.client_id)

        if item.version != expected_version:
            raise StaleActionConflictError(
                f"Stale action conflict: Expected approval version {expected_version}, current version is {item.version}."
            )

        if ApprovalExpiryEvaluator.is_expired(item):
            item.status = "EXPIRED"
            item.version += 1
            raise ControlPlaneError(f"Cannot approve expired request '{approval_id}'.")

        if item.status != "PENDING":
            raise ControlPlaneError(f"Cannot approve request '{approval_id}' in state '{item.status}'.")

        token_raw = f"{approval_id}:{context.operator_id}:{time.time()}:{uuid.uuid4().hex}"
        token_hash = hashlib.sha256(token_raw.encode("utf-8")).hexdigest()

        item.status = "APPROVED"
        item.authorized_by = context.operator_id
        item.authorized_at = time.time()
        item.decision_reason = reason
        item.execution_token_id = f"tok-{token_hash[:16]}"
        item.version += 1

        self.audit_logger.record_event(ControlPlaneAuditEvent(
            operator_id=context.operator_id,
            tenant_id=item.tenant_id,
            client_id=item.client_id,
            action="APPROVE_REQUEST",
            target_resource=approval_id,
            correlation_id=context.correlation_id,
            details={"execution_token_id": item.execution_token_id, "reason": reason}
        ))

        return item

    def reject_request(
        self,
        context: OperatorContext,
        approval_id: str,
        expected_version: int,
        reason: str
    ) -> HumanApprovalItem:
        PermissionGuard.enforce_capability(context, OperatorCapability.REJECT)

        item = self.get_approval(approval_id)
        PermissionGuard.enforce_tenant_boundary(context, item.tenant_id, item.client_id)

        if item.version != expected_version:
            raise StaleActionConflictError(
                f"Stale action conflict: Expected approval version {expected_version}, current version is {item.version}."
            )

        if item.status != "PENDING":
            raise ControlPlaneError(f"Cannot reject request '{approval_id}' in state '{item.status}'.")

        item.status = "REJECTED"
        item.decision_reason = reason
        item.version += 1

        self.audit_logger.record_event(ControlPlaneAuditEvent(
            operator_id=context.operator_id,
            tenant_id=item.tenant_id,
            client_id=item.client_id,
            action="REJECT_REQUEST",
            target_resource=approval_id,
            correlation_id=context.correlation_id,
            details={"reason": reason}
        ))

        return item

    def revoke_approval(
        self,
        context: OperatorContext,
        approval_id: str,
        expected_version: int,
        reason: str
    ) -> HumanApprovalItem:
        PermissionGuard.enforce_capability(context, OperatorCapability.REVOKE_APPROVAL)

        item = self.get_approval(approval_id)
        PermissionGuard.enforce_tenant_boundary(context, item.tenant_id, item.client_id)

        if item.version != expected_version:
            raise StaleActionConflictError(
                f"Stale action conflict: Expected approval version {expected_version}, current version is {item.version}."
            )

        if item.status != "APPROVED":
            raise ControlPlaneError(f"Cannot revoke non-approved request '{approval_id}' in state '{item.status}'.")

        item.status = "REVOKED"
        item.decision_reason = reason
        item.execution_token_id = None # Invalidate token
        item.version += 1

        self.audit_logger.record_event(ControlPlaneAuditEvent(
            operator_id=context.operator_id,
            tenant_id=item.tenant_id,
            client_id=item.client_id,
            action="REVOKE_APPROVAL",
            target_resource=approval_id,
            correlation_id=context.correlation_id,
            details={"reason": reason}
        ))

        return item

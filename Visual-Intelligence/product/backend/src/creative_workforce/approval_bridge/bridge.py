"""
Phase 26 Approval Bridge (Integration with Phase 25 Authorization Center).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from src.authorization_center.approval_service import ApprovalService
from src.control_plane.context import OperatorContext


class ApprovalState(str, Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class ApprovalBridgeError(Exception):
    pass


@dataclass
class VersionedApprovalBinding:
    binding_id: str
    target_object_id: str
    target_version: str
    approval_id: str
    status: ApprovalState = ApprovalState.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkforceApprovalBridge:
    """Bridges workforce high-risk action requests to Phase 25 human authorization service."""

    def __init__(self, approval_service: ApprovalService):
        self.approval_service = approval_service
        self._bindings: Dict[str, VersionedApprovalBinding] = {}

    def request_workforce_approval(
        self,
        tenant_id: str,
        client_id: str,
        worker_id: str,
        action_name: str,
        target_object_id: str,
        target_version: str,
        cost_estimate: float = 0.0,
    ) -> VersionedApprovalBinding:
        # Submit approval request to Phase 25 Authorization Center
        app_req = self.approval_service.create_approval_request(
            tenant_id=tenant_id,
            client_id=client_id,
            requested_by=worker_id,
            action_type=action_name,
            resource_id=f"{target_object_id}@v{target_version}",
            estimated_cost=cost_estimate,
        )

        binding_id = f"vbind_{uuid.uuid4().hex[:12]}"
        binding = VersionedApprovalBinding(
            binding_id=binding_id,
            target_object_id=target_object_id,
            target_version=target_version,
            approval_id=app_req.approval_id,
            status=ApprovalState.PENDING,
        )
        self._bindings[binding_id] = binding
        return binding

    def assert_action_authorized(
        self,
        binding_id: str,
        target_version: str,
    ) -> str:
        """Verifies that approval was granted for the exact object version and returns execution token."""
        binding = self._bindings.get(binding_id)
        if not binding:
            raise ApprovalBridgeError(f"Approval binding '{binding_id}' not found")

        # Check exact version match (v4 approval does not authorize v5)
        if binding.target_version != target_version:
            raise ApprovalBridgeError(
                f"Version mismatch: Approval was bound to version '{binding.target_version}', but current is '{target_version}'"
            )

        app_req = self.approval_service.get_approval(binding.approval_id)
        if not app_req:
            raise ApprovalBridgeError(f"Underlying approval request '{binding.approval_id}' not found")

        if app_req.status != "APPROVED":
            raise ApprovalBridgeError(
                f"Action is not authorized. Approval state is '{app_req.status}' (Requires APPROVED)"
            )

        if not app_req.execution_token_id:
            raise ApprovalBridgeError("Approved request is missing valid execution token")

        return app_req.execution_token_id

"""
Phase 27 Studio Approval Bridge & Governance Integration.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


class StudioApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"


@dataclass
class StudioApprovalRequest:
    approval_id: str
    campaign_id: str
    asset_id: str
    requested_by: str
    status: StudioApprovalStatus
    required_role: OperatorRole
    approver_id: Optional[str] = None
    approver_role: Optional[OperatorRole] = None
    comments: Optional[str] = None
    decided_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class StudioApprovalBridge:
    """Bridges Studio actions to strict Phase 25 governance and human-in-the-loop approvals."""

    def __init__(self):
        self._approvals: Dict[str, StudioApprovalRequest] = {}  # approval_id -> request

    def create_approval_request(
        self,
        campaign_id: str,
        asset_id: str,
        requested_by: str,
        required_role: OperatorRole = OperatorRole.CREATIVE_DIRECTOR,
    ) -> StudioApprovalRequest:
        approval_id = f"appr_{uuid.uuid4().hex[:8]}"
        req = StudioApprovalRequest(
            approval_id=approval_id,
            campaign_id=campaign_id,
            asset_id=asset_id,
            requested_by=requested_by,
            status=StudioApprovalStatus.PENDING,
            required_role=required_role,
        )
        self._approvals[approval_id] = req
        return req

    def submit_decision(
        self,
        approval_id: str,
        operator: OperatorContext,
        decision: StudioApprovalStatus,
        comments: str = "",
    ) -> StudioApprovalRequest:
        req = self._approvals.get(approval_id)
        if not req:
            raise KeyError(f"Approval request '{approval_id}' not found.")

        if req.status != StudioApprovalStatus.PENDING:
            raise ValueError(f"Approval request '{approval_id}' has already been decided: {req.status}")

        # Check authorization: Operator must possess the required role or executive override
        authorized_roles = {req.required_role, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.SUPER_ADMIN}
        if operator.role not in authorized_roles:
            raise PermissionError(
                f"Operator '{operator.operator_id}' with role '{operator.role}' is not authorized to approve. "
                f"Required role: '{req.required_role}'"
            )

        req.status = decision
        req.approver_id = operator.operator_id
        req.approver_role = operator.role
        req.comments = comments
        req.decided_at = datetime.now(timezone.utc)
        return req

    def get_approval(self, approval_id: str) -> Optional[StudioApprovalRequest]:
        return self._approvals.get(approval_id)

    def list_approvals_for_campaign(self, campaign_id: str) -> List[StudioApprovalRequest]:
        return [a for a in self._approvals.values() if a.campaign_id == campaign_id]

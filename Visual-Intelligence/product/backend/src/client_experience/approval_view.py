"""
Phase 16 Approval Center View.
Provides human approval queue projections and delegates approval decisions to Phase 10 authorization pathway.
"""

from typing import List, Dict, Any, Optional
from src.client_experience.workspace_models import ApprovalSummaryDTO
from src.client_experience.access_models import UserIdentity
from src.client_experience.presentation_policy import PresentationPolicyEngine
from src.client_experience.exceptions import UIAuthorizationForgeryError

class ApprovalCenterView:
    """Approval Center managing approval queue projections and Phase 10 authorization routing."""

    def __init__(self, presentation_policy: Optional[PresentationPolicyEngine] = None):
        self.presentation_policy = presentation_policy or PresentationPolicyEngine()

    def list_pending_approvals(self, user: UserIdentity, studio_orchestrator: Any) -> List[ApprovalSummaryDTO]:
        """Lists active pending approval projections for a client."""
        user.verify_capability("review_deliverable")
        client_id = user.assigned_client_id
        items = studio_orchestrator.approval_queue.list_pending_approvals(client_id)
        return [self.presentation_policy.project_approval(item) for item in items]

    def submit_human_decision(
        self,
        user: UserIdentity,
        studio_orchestrator: Any,
        approval_id: str,
        approved: bool,
        reason: str = ""
    ) -> ApprovalSummaryDTO:
        """Submits human approval decision routed through Phase 10 authorization pathway."""
        capability = "approve_deliverable" if approved else "reject_deliverable"
        user.verify_capability(capability)
        client_id = user.assigned_client_id

        # Delegate decision to Phase 15/Phase 10 control plane
        item = studio_orchestrator.record_human_approval_decision(
            requesting_client_id=client_id,
            approval_id=approval_id,
            approved=approved,
            authorizer_id=user.user_id
        )

        return self.presentation_policy.project_approval(item)

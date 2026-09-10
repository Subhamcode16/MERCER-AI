"""
Phase 16 Studio Command Center.
Primary human interaction entry point orchestrating Phase 16 Client Experience over Phase 15 Studio Operations.
"""

from typing import Dict, List, Optional, Any
from src.client_experience.access_models import HumanRole, UserIdentity
from src.client_experience.client_access import ClientAccessManager
from src.client_experience.dashboard import ClientDashboardProjectionEngine
from src.client_experience.campaign_view import CampaignCommandCenterView
from src.client_experience.deliverable_view import DeliverableReviewSurface
from src.client_experience.approval_view import ApprovalCenterView
from src.client_experience.feedback import FeedbackManager
from src.client_experience.workforce_view import WorkforceActivityView
from src.client_experience.timeline import OperationsTimelineEngine
from src.client_experience.performance_view import PerformanceOutcomeView
from src.client_experience.notification import NotificationCenter
from src.client_experience.api_boundary import ClientExperienceAPIBoundary
from src.client_experience.presentation_policy import PresentationPolicyEngine
from src.client_experience.interaction_audit import InteractionAuditLogger
from src.client_experience.workspace_models import (
    ClientWorkspaceDTO, CampaignDTO, DeliverableDTO, ApprovalSummaryDTO,
    WorkforceActivityDTO, TimelineEventDTO, PerformanceSummaryDTO
)
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

class StudioCommandCenter:
    """Primary human interaction control surface for ILYREN Creative Studio."""

    def __init__(
        self,
        studio_orchestrator: Optional[StudioOperationsOrchestrator] = None,
        audit_dir: str = "data/phase16_interaction_ledger"
    ):
        self.studio_orchestrator = studio_orchestrator or StudioOperationsOrchestrator()
        self.access_manager = ClientAccessManager()
        self.presentation_policy = PresentationPolicyEngine()
        self.dashboard_engine = ClientDashboardProjectionEngine(self.presentation_policy)
        self.campaign_view = CampaignCommandCenterView()
        self.deliverable_review = DeliverableReviewSurface(self.presentation_policy)
        self.approval_view = ApprovalCenterView(self.presentation_policy)
        self.feedback_manager = FeedbackManager()
        self.workforce_view = WorkforceActivityView()
        self.timeline_engine = OperationsTimelineEngine()
        self.performance_view = PerformanceOutcomeView()
        self.notification_center = NotificationCenter()
        self.api_boundary = ClientExperienceAPIBoundary()
        self.audit_logger = InteractionAuditLogger(ledger_dir=audit_dir)

    def register_user(self, user_id: str, name: str, email: str, assigned_client_id: str, role: HumanRole) -> UserIdentity:
        """Registers a user identity."""
        user = self.access_manager.register_user(user_id, name, email, assigned_client_id, role)
        self.audit_logger.record_interaction(assigned_client_id, user_id, "USER_REGISTERED", {"user_id": user_id, "role": role.value})
        return user

    def get_dashboard(self, user_id: str, client_id: str) -> ClientWorkspaceDTO:
        """Returns client dashboard projection under access checks."""
        user = self.access_manager.authenticate_and_authorize(user_id, client_id, "view_dashboard")
        dto = self.dashboard_engine.get_dashboard(user, self.studio_orchestrator)
        self.audit_logger.record_interaction(client_id, user_id, "VIEW_DASHBOARD", {"client_id": client_id})
        return dto

    def request_campaign(self, user_id: str, client_id: str, campaign_id: str, brand_id: str, title: str, objective: str) -> CampaignDTO:
        """Submits a campaign launch request."""
        user = self.access_manager.authenticate_and_authorize(user_id, client_id, "request_campaign")
        dto = self.campaign_view.request_campaign(user, self.studio_orchestrator, campaign_id, brand_id, title, objective)
        self.audit_logger.record_interaction(client_id, user_id, "REQUEST_CAMPAIGN", {"campaign_id": campaign_id, "title": title})
        return dto

    def list_deliverables(self, user_id: str, client_id: str, campaign_id: str) -> List[DeliverableDTO]:
        """Lists deliverable review projections."""
        user = self.access_manager.authenticate_and_authorize(user_id, client_id, "review_deliverable")
        return self.deliverable_review.list_deliverables_for_campaign(user, self.studio_orchestrator, campaign_id)

    def list_pending_approvals(self, user_id: str, client_id: str) -> List[ApprovalSummaryDTO]:
        """Lists active pending approval projections."""
        user = self.access_manager.authenticate_and_authorize(user_id, client_id, "review_deliverable")
        return self.approval_view.list_pending_approvals(user, self.studio_orchestrator)

    def submit_approval_decision(self, user_id: str, client_id: str, approval_id: str, approved: bool) -> ApprovalSummaryDTO:
        """Submits explicit human decision routed to Phase 10 authorization pathway."""
        capability = "approve_deliverable" if approved else "reject_deliverable"
        user = self.access_manager.authenticate_and_authorize(user_id, client_id, capability)
        dto = self.approval_view.submit_human_decision(user, self.studio_orchestrator, approval_id, approved)
        self.audit_logger.record_interaction(client_id, user_id, "SUBMIT_APPROVAL_DECISION", {"approval_id": approval_id, "approved": approved})
        return dto

    def submit_feedback(self, user_id: str, client_id: str, feedback_id: str, deliverable_id: str, feedback_type: str, comments: str) -> Dict:
        """Submits structured client feedback."""
        user = self.access_manager.authenticate_and_authorize(user_id, client_id, "submit_feedback")
        record = self.feedback_manager.submit_feedback(user, feedback_id, deliverable_id, feedback_type, comments, self.studio_orchestrator)
        self.audit_logger.record_interaction(client_id, user_id, "SUBMIT_FEEDBACK", {"feedback_id": feedback_id, "type": feedback_type})
        return {"feedback_id": record.feedback_id, "status": "INGESTED", "type": record.feedback_type}

    def verify_audit_integrity(self) -> bool:
        """Verifies integrity of interaction audit chain."""
        return self.audit_logger.verify_integrity()

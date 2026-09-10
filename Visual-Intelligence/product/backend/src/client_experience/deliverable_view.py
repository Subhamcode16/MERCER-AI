"""
Phase 16 Deliverable Review Surface.
Provides deliverable inspection, critique summaries, and review outcome projections.
"""

from typing import List, Dict, Any, Optional
from src.client_experience.workspace_models import DeliverableDTO
from src.client_experience.access_models import UserIdentity
from src.client_experience.presentation_policy import PresentationPolicyEngine

class DeliverableReviewSurface:
    """Surface providing deliverable inspection and review projections."""

    def __init__(self, presentation_policy: Optional[PresentationPolicyEngine] = None):
        self.presentation_policy = presentation_policy or PresentationPolicyEngine()

    def get_deliverable(self, user: UserIdentity, studio_orchestrator: Any, deliverable_id: str) -> DeliverableDTO:
        """Retrieves and projects a deliverable."""
        user.verify_capability("review_deliverable")
        client_id = user.assigned_client_id
        d = studio_orchestrator.deliverable_manager.get_deliverable(client_id, deliverable_id)
        return self.presentation_policy.project_deliverable(d)

    def list_deliverables_for_campaign(self, user: UserIdentity, studio_orchestrator: Any, campaign_id: str) -> List[DeliverableDTO]:
        """Lists deliverable projections under a campaign."""
        user.verify_capability("review_deliverable")
        client_id = user.assigned_client_id
        items = studio_orchestrator.deliverable_manager.list_deliverables_for_campaign(client_id, campaign_id)
        return [self.presentation_policy.project_deliverable(item) for item in items]

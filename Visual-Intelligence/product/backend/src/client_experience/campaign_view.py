"""
Phase 16 Campaign Command Center View.
Provides campaign requests and progress projections.
"""

from typing import List, Dict, Any, Optional
from src.client_experience.workspace_models import CampaignDTO
from src.client_experience.access_models import UserIdentity

class CampaignCommandCenterView:
    """View provider for campaign projections and campaign launch requests."""

    def request_campaign(
        self,
        user: UserIdentity,
        studio_orchestrator: Any,
        campaign_id: str,
        brand_id: str,
        title: str,
        objective: str
    ) -> CampaignDTO:
        """Submits a campaign launch request to Phase 15 Studio Operations."""
        user.verify_capability("request_campaign")
        client_id = user.assigned_client_id

        result = studio_orchestrator.launch_campaign(
            requesting_client_id=client_id,
            campaign_id=campaign_id,
            brand_id=brand_id,
            title=title,
            objective=objective
        )

        return CampaignDTO(
            campaign_id=campaign_id,
            client_id=client_id,
            brand_id=brand_id,
            title=title,
            objective=objective,
            status=result["status"],
            deliverables_count=0,
            created_at=str(result.get("status", "ACTIVE"))
        )

    def list_campaigns(self, user: UserIdentity, studio_orchestrator: Any) -> List[CampaignDTO]:
        """Lists safe campaign projections for a client."""
        user.verify_capability("view_dashboard")
        client_id = user.assigned_client_id
        campaigns = studio_orchestrator.campaign_manager.list_campaigns(client_id)

        dtos = []
        for c in campaigns:
            deliverables = studio_orchestrator.deliverable_manager.list_deliverables_for_campaign(client_id, c.campaign_id)
            dtos.append(CampaignDTO(
                campaign_id=c.campaign_id,
                client_id=c.client_id,
                brand_id=c.brand_id,
                title=c.title,
                objective=c.objective,
                status=c.status.value if hasattr(c.status, "value") else str(c.status),
                deliverables_count=len(deliverables),
                created_at=c.created_at
            ))
        return dtos

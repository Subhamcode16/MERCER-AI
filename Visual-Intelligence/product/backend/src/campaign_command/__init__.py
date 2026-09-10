"""
Phase 25 Campaign Command Center Package.
"""
from src.campaign_command.campaign_projection import DetailedCampaignState, CampaignDetailedProjection
from src.campaign_command.stage_projection import CampaignStageProgression
from src.campaign_command.dependency_view import DependencyNode, DependencyGraphViewer
from src.campaign_command.deliverable_projection import DeliverableDetailProjection
from src.campaign_command.workforce_projection import WorkforceRoleAllocation
from src.campaign_command.timeline_projection import CampaignMilestone, CampaignTimelineProjection
from src.campaign_command.campaign_actions import CampaignActionService

__all__ = [
    "DetailedCampaignState",
    "CampaignDetailedProjection",
    "CampaignStageProgression",
    "DependencyNode",
    "DependencyGraphViewer",
    "DeliverableDetailProjection",
    "WorkforceRoleAllocation",
    "CampaignMilestone",
    "CampaignTimelineProjection",
    "CampaignActionService"
]

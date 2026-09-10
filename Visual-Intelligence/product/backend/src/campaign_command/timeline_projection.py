"""
Phase 25 Campaign Milestone and Timeline Calculations.
"""
from dataclasses import dataclass
from typing import List, Optional
import time

@dataclass
class CampaignMilestone:
    milestone_id: str
    name: str
    target_timestamp: float
    completed_timestamp: Optional[float] = None
    is_completed: bool = False

@dataclass
class CampaignTimelineProjection:
    campaign_id: str
    started_at: float
    target_delivery_at: float
    milestones: List[CampaignMilestone]
    projected_delay_hours: float = 0.0

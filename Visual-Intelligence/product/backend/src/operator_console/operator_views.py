"""
Phase 25 Role-Tailored Operator View Models.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from src.control_plane.models import OperatorRole
from src.control_plane.dto import CampaignSummaryDTO, ApprovalRequestDTO, ReliabilityStatusDTO, VisualObservatoryDTO

@dataclass
class CuratorView:
    pending_approvals: List[ApprovalRequestDTO] = field(default_factory=list)
    active_campaigns: List[CampaignSummaryDTO] = field(default_factory=list)
    recent_reviews_count: int = 0
    urgent_items: List[str] = field(default_factory=list)

@dataclass
class CreativeDirectorView:
    campaigns: List[CampaignSummaryDTO] = field(default_factory=list)
    visual_overview: Optional[VisualObservatoryDTO] = None
    strategy_candidates_count: int = 0
    workforce_utilization_pct: float = 0.0

@dataclass
class SREView:
    reliability: Optional[ReliabilityStatusDTO] = None
    provider_health_summary: Dict[str, str] = field(default_factory=dict)
    active_circuit_breakers: List[str] = field(default_factory=list)
    incident_alerts: List[Dict[str, Any]] = field(default_factory=list)

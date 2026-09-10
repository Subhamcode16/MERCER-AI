"""
Phase 25 Advisory Workforce Recommendations View.
Enforces invariant: Recommendation != Command, EXECUTED = FALSE, REQUIRES HUMAN APPROVAL.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List
import time

@dataclass
class AdvisoryRecommendation:
    recommendation_id: str
    tenant_id: str
    client_id: str
    campaign_id: str
    source_staff_role: str
    recommendation_type: str # ANGLE_PIVOT, PALETTE_SHIFT, COPY_VARIATION, BUDGET_ALLOCATION
    title: str
    description: str
    confidence_score: float
    is_advisory: bool = True
    requires_human_approval: bool = True
    executed: bool = False
    timestamp: float = field(default_factory=time.time)

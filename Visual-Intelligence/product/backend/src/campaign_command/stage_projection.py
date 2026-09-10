"""
Phase 25 Campaign Stage Progression and Status Projection.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class CampaignStageProgression:
    stage_name: str # e.g. "Strategy", "Creative Direction", "Visual Generation", "Critique", "Human Review", "Execution", "Evaluation"
    order: int
    status: str # NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED
    assigned_roles: List[str] = field(default_factory=list)
    deliverables_count: int = 0
    duration_seconds: float = 0.0

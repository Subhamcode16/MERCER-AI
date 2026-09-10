"""
Phase 26 Governed Workforce Learning & Optimization Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


@dataclass
class LearningOptimizationProposal:
    proposal_id: str
    tenant_id: str
    target_skill_id: Optional[str] = None
    target_worker_id: Optional[str] = None
    proposal_type: str = "SKILL_IMPROVEMENT"  # SKILL_IMPROVEMENT, MISSING_SKILL, WORKFLOW_OPTIMIZATION
    recommended_changes: List[str] = field(default_factory=list)
    rationale: str = ""
    is_advisory: bool = True
    status: str = "PROPOSED"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkforceLearningEngine:
    """Proposes governed skill and workflow improvements without mutating security policies."""

    def __init__(self):
        self._proposals: Dict[str, LearningOptimizationProposal] = {}

    def propose_skill_optimization(
        self,
        tenant_id: str,
        skill_id: str,
        failure_patterns: List[str],
        recommended_adjustments: List[str],
    ) -> LearningOptimizationProposal:
        prop_id = f"opt_{uuid.uuid4().hex[:12]}"
        proposal = LearningOptimizationProposal(
            proposal_id=prop_id,
            tenant_id=tenant_id,
            target_skill_id=skill_id,
            proposal_type="SKILL_IMPROVEMENT",
            recommended_changes=recommended_adjustments,
            rationale=f"Identified {len(failure_patterns)} failure patterns in execution telemetry",
            is_advisory=True,
        )
        self._proposals[prop_id] = proposal
        return proposal

    def get_proposal(self, proposal_id: str) -> Optional[LearningOptimizationProposal]:
        return self._proposals.get(proposal_id)

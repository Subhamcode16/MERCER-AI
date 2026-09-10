"""
Phase 19 - Bounded Workforce Evolution Advisor.

Analyzes institutional performance and pattern discovery to issue advisory recommendations
for workforce skill refinement, prompt optimization, or workflow routing.
Guarantees Workforce Evolution != Privilege Escalation.
"""

from typing import Dict, List, Any, Optional
from .knowledge_models import WorkforceRecommendation, InstitutionalPattern
from .exceptions import AuthorityEscalationError, ImmutablePolicyViolationError


class WorkforceEvolutionAdvisor:
    """Generates strictly advisory (NON-EXECUTABLE) workforce evolution proposals."""

    def __init__(self):
        self._recommendations: Dict[str, WorkforceRecommendation] = {}

    def generate_recommendation(
        self,
        target_agent_id: str,
        recommendation_type: str,
        rationale: str,
        suggested_changes: Dict[str, Any],
        evidence_pattern_ids: List[str]
    ) -> WorkforceRecommendation:
        """Create advisory recommendation. Enforces NON-EXECUTABLE invariant."""
        
        # 1. Enforce invariant: Cannot recommend security policy or permission modifications
        for key in ["permissions", "auth_roles", "security_policy", "autonomy_ceiling", "override_authorization"]:
            if key in suggested_changes or key in rationale.lower():
                raise ImmutablePolicyViolationError(
                    f"Workforce evolution cannot modify security policy or authority settings ({key})."
                )

        rec = WorkforceRecommendation(
            target_agent_id=target_agent_id,
            recommendation_type=recommendation_type,
            rationale=rationale,
            suggested_changes=suggested_changes,
            evidence_pattern_ids=evidence_pattern_ids,
            requires_human_approval=True,
            executed=False  # ALWAYS False
        )

        self._recommendations[rec.recommendation_id] = rec
        return rec

    def attempt_execution(self, recommendation_id: str) -> None:
        """Invoking execution from the intelligence layer raises AuthorityEscalationError."""
        raise AuthorityEscalationError(
            "Institutional intelligence cannot execute workforce evolution recommendations. "
            "Execution authority resides strictly in Phase 14 / Phase 3 Authorization system."
        )

    def get_recommendation(self, rec_id: str) -> Optional[WorkforceRecommendation]:
        return self._recommendations.get(rec_id)

    def list_recommendations(self, target_agent_id: Optional[str] = None) -> List[WorkforceRecommendation]:
        if target_agent_id:
            return [r for r in self._recommendations.values() if r.target_agent_id == target_agent_id]
        return list(self._recommendations.values())

"""
Phase 18 Studio Intelligence Dashboard.

Provides safe, secret-free performance, experiment, trend, and workflow projections
for client command center presentation surfaces.
"""

from typing import Dict, Any, List, Optional

from src.studio_intelligence.outcome_store import OutcomeStore
from src.studio_intelligence.intelligence_memory import StudioIntelligenceMemory
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


class StudioIntelligenceDashboard:
    """Synthesizes safe DTO projections for intelligence, performance, and experiments."""

    def __init__(
        self,
        outcome_store: Optional[OutcomeStore] = None,
        memory: Optional[StudioIntelligenceMemory] = None,
    ):
        self.outcome_store = outcome_store or OutcomeStore()
        self.memory = memory or StudioIntelligenceMemory()

    def get_client_intelligence_summary(
        self, requesting_client_id: str, target_client_id: str
    ) -> Dict[str, Any]:
        """Projects client intelligence summary without exposing secrets or CoT reasoning."""
        if requesting_client_id != target_client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot view intelligence summary for '{target_client_id}'."
            )

        observations = self.outcome_store.list_observations(
            requesting_client_id=requesting_client_id,
            target_client_id=target_client_id,
        )

        knowledge_items = self.memory.list_knowledge_items(
            requesting_client_id=requesting_client_id,
            target_client_id=target_client_id,
        )

        total_obs = len(observations)
        avg_impressions = (
            sum(obs.metrics.get("impressions", 0.0) for obs in observations) / total_obs
            if total_obs > 0
            else 0.0
        )
        avg_engagement = (
            sum(obs.metrics.get("engagements", 0.0) for obs in observations) / total_obs
            if total_obs > 0
            else 0.0
        )

        return {
            "client_id": target_client_id,
            "total_observations": total_obs,
            "avg_impressions": round(avg_impressions, 2),
            "avg_engagements": round(avg_engagement, 2),
            "adopted_knowledge_count": len(knowledge_items),
            "knowledge_items": [
                {
                    "item_id": ki.item_id,
                    "title": ki.title,
                    "category": ki.category,
                    "confidence_score": ki.confidence_score,
                }
                for ki in knowledge_items
            ],
        }

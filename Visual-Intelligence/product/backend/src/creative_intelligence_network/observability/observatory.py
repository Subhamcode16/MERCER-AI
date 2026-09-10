"""
Strategic Intelligence Observatory providing higher-order network monitoring.
"""
from typing import Any, Dict, List, Optional
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph
from ..signals.signal_engine import StrategicSignalEngine
from ..recommendations.recommendation_engine import StrategicRecommendationEngine
from ..hypotheses.hypothesis_engine import HypothesisEngine


class StrategicIntelligenceObservatory:
    def __init__(
        self,
        graph: OrganizationalIntelligenceGraph,
        signals: StrategicSignalEngine,
        hypotheses: HypothesisEngine,
        recommendations: StrategicRecommendationEngine,
    ):
        self.graph = graph
        self.signals = signals
        self.hypotheses = hypotheses
        self.recommendations = recommendations

    def get_observatory_snapshot(self, tenant_id: str) -> Dict[str, Any]:
        all_signals = self.signals.list_signals(tenant_id)
        all_hypotheses = self.hypotheses.list_hypotheses(tenant_id)
        all_recs = self.recommendations.list_recommendations(tenant_id)

        return {
            "tenant_id": tenant_id,
            "metrics": {
                "total_entities_in_graph": self.graph.count_entities(tenant_id),
                "total_relationships_in_graph": self.graph.count_relationships(tenant_id),
                "active_signals_count": len(all_signals),
                "active_hypotheses_count": len(all_hypotheses),
                "active_recommendations_count": len(all_recs),
            },
            "signals_by_class": {
                s.signal_class.value: sum(1 for x in all_signals if x.signal_class == s.signal_class)
                for s in all_signals
            },
            "hypotheses_by_status": {
                h.status.value: sum(1 for x in all_hypotheses if x.status == h.status)
                for h in all_hypotheses
            },
            "recommendations_by_status": {
                r.status.value: sum(1 for x in all_recs if x.status == r.status)
                for r in all_recs
            },
        }

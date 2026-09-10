"""
Phase 19 - Multi-Domain Intelligence Synthesis Engine.

Synthesizes high-level creative intelligence proposals by querying institutional memory,
global patterns, and active strategies across creative domains.
"""

from typing import Dict, List, Any, Optional
from .knowledge_graph import InstitutionalKnowledgeGraph
from .strategy_registry import InstitutionalStrategyRegistry
from .pattern_discovery import PatternDiscoveryEngine
from .exceptions import CreativeIntelligenceError


class IntelligenceSynthesisEngine:
    """Synthesizes actionable intelligence insights for creative studio production."""

    def __init__(
        self,
        knowledge_graph: InstitutionalKnowledgeGraph,
        strategy_registry: InstitutionalStrategyRegistry,
        pattern_discovery: PatternDiscoveryEngine
    ):
        self.graph = knowledge_graph
        self.strategies = strategy_registry
        self.patterns = pattern_discovery

    def synthesize_campaign_intelligence(
        self,
        domain: str,
        campaign_brief: Dict[str, Any],
        client_id: str
    ) -> Dict[str, Any]:
        """Synthesize recommendations and pattern matches for a campaign brief."""
        
        # 1. Fetch active domain strategy if available
        active_strategy = None
        try:
            active_strategy = self.strategies.get_active_strategy(domain)
        except Exception:
            pass  # Fallback gracefully if no active baseline

        # 2. Find relevant global patterns for domain
        domain_patterns = self.patterns.list_patterns(domain=domain)
        top_patterns = sorted(domain_patterns, key=lambda p: (p.confidence_score, p.support_count), reverse=True)[:3]

        # 3. Query client-specific historical patterns
        client_history = self.graph.get_client_nodes(client_id)

        # 4. Construct intelligence synthesis package
        synthesis = {
            "client_id": client_id,
            "domain": domain,
            "brief_summary": campaign_brief.get("summary", "Creative Campaign Brief"),
            "active_strategy": {
                "strategy_id": active_strategy.strategy_id,
                "strategy_name": active_strategy.strategy_name,
                "version": active_strategy.version,
                "parameters": active_strategy.parameters
            } if active_strategy else None,
            "recommended_patterns": [
                {
                    "pattern_id": p.pattern_id,
                    "pattern_name": p.pattern_name,
                    "confidence_score": p.confidence_score,
                    "support_count": p.support_count,
                    "abstract_structure": p.abstract_structure
                }
                for p in top_patterns
            ],
            "client_prior_deliverable_count": len(client_history),
            "intelligence_verdict": "RECOMMENDED" if (active_strategy or top_patterns) else "INSUFFICIENT_DATA"
        }

        return synthesis

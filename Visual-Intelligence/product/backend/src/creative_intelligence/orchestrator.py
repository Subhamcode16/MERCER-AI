"""
Phase 19 - Creative Intelligence Orchestrator.

Central facade integrating all Phase 19 components for institutional learning,
provenance tracking, pattern discovery, versioned strategy registry, workforce advice,
and boundary enforcement above Phase 18 Studio Intelligence.
"""

from typing import Dict, List, Any, Optional
from .knowledge_models import (
    GraphNode, GraphEdge, InstitutionalPattern, ValidatedStrategy,
    WorkforceRecommendation, CreativeIntelligenceMetrics
)
from .knowledge_graph import InstitutionalKnowledgeGraph
from .provenance import ProvenanceTracker
from .generalization import ConfidentialityFilter
from .pattern_discovery import PatternDiscoveryEngine
from .institutional_memory import InstitutionalMemory
from .validation import StrategyValidator
from .retirement import StrategyRetirementManager
from .strategy_registry import InstitutionalStrategyRegistry
from .workforce_evolution import WorkforceEvolutionAdvisor
from .intelligence_synthesis import IntelligenceSynthesisEngine
from .intelligence_governance import IntelligenceGovernanceBoundary
from .intelligence_events import IntelligenceEventStream
from .creative_intelligence_ledger import CreativeIntelligenceLedger
from .dashboard import CreativeIntelligenceDashboard
from .exceptions import CreativeIntelligenceError


class CreativeIntelligenceOrchestrator:
    """Orchestrator for the Phase 19 Creative Intelligence Network."""

    def __init__(self):
        self.provenance = ProvenanceTracker()
        self.graph = InstitutionalKnowledgeGraph()
        self.filter = ConfidentialityFilter()
        self.pattern_engine = PatternDiscoveryEngine(self.graph, self.provenance, self.filter)
        self.memory = InstitutionalMemory(self.graph, self.provenance)
        self.validator = StrategyValidator()
        self.retirement_manager = StrategyRetirementManager()
        self.strategies = InstitutionalStrategyRegistry(self.validator, self.retirement_manager)
        self.workforce = WorkforceEvolutionAdvisor()
        self.synthesis = IntelligenceSynthesisEngine(self.graph, self.strategies, self.pattern_engine)
        self.governance = IntelligenceGovernanceBoundary(self.filter)
        self.events = IntelligenceEventStream()
        self.ledger = CreativeIntelligenceLedger()
        self.dashboard = CreativeIntelligenceDashboard(
            self.graph, self.strategies, self.pattern_engine, self.workforce, self.ledger
        )

    def ingest_client_execution(
        self,
        client_id: str,
        execution_id: str,
        domain: str,
        execution_details: Dict[str, Any],
        evidence_hash: str
    ) -> Dict[str, Any]:
        """Ingest client execution, store client artifact, and attempt pattern discovery."""
        # 1. Store client artifact in memory & graph
        artifact_node = self.memory.record_client_artifact(
            client_id=client_id,
            artifact_id=execution_id,
            artifact_type="Deliverable",
            attributes=execution_details,
            evidence_hash=evidence_hash
        )

        # 2. Record event and ledger entry
        self.events.emit("CLIENT_EXECUTION_INGESTED", {"execution_id": execution_id}, client_id=client_id)
        self.ledger.record_entry("CLIENT_EXECUTION_INGESTED", {"client_id": client_id, "execution_id": execution_id})

        # 3. Discover cross-client pattern if high quality
        pattern_name = execution_details.get("pattern_name", f"{domain}_standard_flow")
        discovered_pattern = self.pattern_engine.discover_pattern_from_executions(
            pattern_name=pattern_name,
            domain=domain,
            execution_attributes=execution_details,
            source_client_id=client_id,
            evidence_hash=evidence_hash
        )

        self.events.emit("PATTERN_DISCOVERED", {"pattern_id": discovered_pattern.pattern_id})
        self.ledger.record_entry("PATTERN_DISCOVERED", {"pattern_id": discovered_pattern.pattern_id})

        return {
            "artifact_id": artifact_node.node_id,
            "pattern_id": discovered_pattern.pattern_id,
            "support_count": discovered_pattern.support_count
        }

    def synthesize_intelligence(self, domain: str, campaign_brief: Dict[str, Any], client_id: str) -> Dict[str, Any]:
        """Synthesize recommendations for a campaign brief."""
        synthesis_result = self.synthesis.synthesize_campaign_intelligence(domain, campaign_brief, client_id)
        self.governance.audit_intelligence_output(synthesis_result, is_global=False)
        return synthesis_result

    def propose_and_activate_strategy(
        self,
        strategy_name: str,
        domain: str,
        pattern_id: str,
        parameters: Dict[str, Any],
        empirical_telemetry: Dict[str, Any]
    ) -> ValidatedStrategy:
        """Propose, validate empirically, and activate institutional strategy."""
        strat = self.strategies.propose_strategy(strategy_name, domain, pattern_id, parameters)
        self.strategies.validate_and_register(strat.strategy_id, empirical_telemetry)
        active_strat = self.strategies.activate_strategy(strat.strategy_id)

        self.events.emit("STRATEGY_ACTIVATED", {"strategy_id": active_strat.strategy_id, "domain": domain})
        self.ledger.record_entry("STRATEGY_ACTIVATED", {"strategy_id": active_strat.strategy_id, "domain": domain})

        return active_strat

    def recommend_workforce_evolution(
        self,
        target_agent_id: str,
        recommendation_type: str,
        rationale: str,
        suggested_changes: Dict[str, Any],
        evidence_pattern_ids: List[str]
    ) -> WorkforceRecommendation:
        """Issue advisory workforce evolution proposal."""
        rec = self.workforce.generate_recommendation(
            target_agent_id=target_agent_id,
            recommendation_type=recommendation_type,
            rationale=rationale,
            suggested_changes=suggested_changes,
            evidence_pattern_ids=evidence_pattern_ids
        )

        self.events.emit("RECOMMENDATION_GENERATED", {"recommendation_id": rec.recommendation_id})
        self.ledger.record_entry("RECOMMENDATION_GENERATED", {"recommendation_id": rec.recommendation_id})

        return rec

    def get_dashboard_metrics(self) -> CreativeIntelligenceMetrics:
        return self.dashboard.get_metrics()

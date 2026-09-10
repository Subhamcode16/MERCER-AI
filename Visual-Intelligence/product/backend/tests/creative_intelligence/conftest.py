"""
Pytest configuration and shared fixtures for Phase 19 Creative Intelligence test suite.
"""

import pytest
from src.creative_intelligence.orchestrator import CreativeIntelligenceOrchestrator
from src.creative_intelligence.knowledge_graph import InstitutionalKnowledgeGraph
from src.creative_intelligence.provenance import ProvenanceTracker
from src.creative_intelligence.generalization import ConfidentialityFilter
from src.creative_intelligence.pattern_discovery import PatternDiscoveryEngine
from src.creative_intelligence.strategy_registry import InstitutionalStrategyRegistry
from src.creative_intelligence.workforce_evolution import WorkforceEvolutionAdvisor
from src.creative_intelligence.creative_intelligence_ledger import CreativeIntelligenceLedger


@pytest.fixture
def orchestrator():
    """Provides a fresh CreativeIntelligenceOrchestrator instance."""
    return CreativeIntelligenceOrchestrator()


@pytest.fixture
def knowledge_graph():
    return InstitutionalKnowledgeGraph()


@pytest.fixture
def provenance_tracker():
    return ProvenanceTracker()


@pytest.fixture
def confidentiality_filter():
    return ConfidentialityFilter()


@pytest.fixture
def pattern_discovery(knowledge_graph, provenance_tracker, confidentiality_filter):
    return PatternDiscoveryEngine(knowledge_graph, provenance_tracker, confidentiality_filter)


@pytest.fixture
def strategy_registry():
    return InstitutionalStrategyRegistry()


@pytest.fixture
def workforce_advisor():
    return WorkforceEvolutionAdvisor()


@pytest.fixture
def ledger():
    return CreativeIntelligenceLedger()

"""
Tests for KnowledgeStore and TrendIntelligenceEngine.
"""

from src.agentic_work import KnowledgeStore, TrendIntelligenceEngine


def test_trend_intelligence_intake():
    ks = KnowledgeStore()
    engine = TrendIntelligenceEngine(knowledge_store=ks)

    obs = engine.capture_trend_observation(
        source_domain="vogue.com",
        category="PALETTE",
        attributes={"color": "warm ivory"},
    )

    assert obs.observation_id is not None
    assert obs.trust_marker == "UNTRUSTED_EXTERNAL_OBSERVATION"
    assert len(ks.query_by_category("PALETTE")) == 1

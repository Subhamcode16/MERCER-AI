"""
Unit tests for StudioIntelligenceMemory multi-client isolation.
"""

import pytest
from src.studio_intelligence.outcome_models import IntelligenceKnowledgeItem
from src.studio_intelligence.intelligence_memory import StudioIntelligenceMemory
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


def test_intelligence_memory_isolation():
    memory = StudioIntelligenceMemory()
    item = IntelligenceKnowledgeItem(
        item_id="item_nocap_1",
        client_id="client_nocap",
        category="CREATIVE_PATTERN",
        title="Bold Minimalist Urban Copy",
        content="Short punchy hooks perform best.",
        confidence_score=0.95,
        source_signal_ids=["sig_1"],
    )

    with pytest.raises(CrossClientIntelligenceViolation):
        memory.store_knowledge_item(requesting_client_id="client_beta", item=item)

    memory.store_knowledge_item(requesting_client_id="client_nocap", item=item)

    with pytest.raises(CrossClientIntelligenceViolation):
        memory.get_knowledge_item(requesting_client_id="client_beta", item_id="item_nocap_1")

    res = memory.get_knowledge_item(requesting_client_id="client_nocap", item_id="item_nocap_1")
    assert res is not None
    assert res.title == "Bold Minimalist Urban Copy"

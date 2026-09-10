"""
Phase 14 Test Self Critique Engine
----------------------------------
Tests SelfCritiqueEngine evaluation dimensions and non-authoritative output signals.
"""

import pytest
from src.creative_workforce import (
    SelfCritiqueEngine,
    CreativeCollaborationProtocol,
    ContextBinding,
)

def test_self_critique_evaluation():
    engine = SelfCritiqueEngine()
    protocol = CreativeCollaborationProtocol()
    binding = ContextBinding("nocap", "brand", "cmp-1", "m-1", "t-1", "designer-01")

    art = protocol.create_artifact("Campaign Post", "POST", {"text": "NOCAP September Launch"}, binding)
    critique = engine.evaluate_artifact(art)

    assert critique.critique_id.startswith("crit-")
    assert critique.is_authoritative is False
    assert "visual_quality" in critique.criteria_scores

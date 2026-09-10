"""
Phase 14 Test Creative Direction
--------------------------------
Tests CreativeDirectionSynthesizer brief generation.
"""

import pytest
from src.creative_workforce import (
    CreativeDirectionSynthesizer,
    VisualDNAManager,
    TrendIntelligenceEngine,
)

def test_creative_direction_synthesis():
    vdna_mgr = VisualDNAManager()
    trend_engine = TrendIntelligenceEngine()
    synth = CreativeDirectionSynthesizer()

    profile = vdna_mgr.extract_visual_dna("nocap", ["#000000"], ["Inter"])
    obs = trend_engine.collect_observation("https://trends.wiki", "streetwear", "Asymmetric layouts")

    brief = synth.synthesize_direction("NOCAP Autumn", profile, [obs])
    assert brief.brief_id.startswith("cdb-")
    assert brief.campaign_title == "NOCAP Autumn"
    assert len(brief.creative_pillars) >= 3

"""
Phase 14 Test Visual DNA
------------------------
Tests VisualDNAManager extraction and profile comparison.
"""

import pytest
from src.creative_workforce import VisualDNAManager

def test_visual_dna_extraction_and_comparison():
    mgr = VisualDNAManager()
    profile_a = mgr.extract_visual_dna("nocap", ["#000000", "#FFFFFF"], ["Inter"])
    profile_b = mgr.extract_visual_dna("luxury", ["#000000", "#D4AF37"], ["Didot"])

    cmp_res = mgr.compare_dna(profile_a, profile_b)
    assert "affinity_score" in cmp_res
    assert cmp_res["affinity_score"] > 0.0

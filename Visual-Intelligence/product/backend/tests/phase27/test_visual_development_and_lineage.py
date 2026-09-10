"""
Tests for Phase 27 Visual Development Pipeline & Cryptographic Lineage Graph.
"""
import pytest
from src.campaign_studio.visual_development import VisualDevelopmentPipeline
from src.campaign_studio.asset_lineage import AssetLineageGraph


def test_visual_dna_compilation_and_draft_generation():
    pipeline = VisualDevelopmentPipeline()
    campaign_id = "camp_vis_01"
    direction_id = "dir_mono_01"

    dna_tokens = pipeline.compile_visual_dna(campaign_id, direction_id)
    assert len(dna_tokens) >= 4
    assert any(t.token_name == "raking_monolithic_late_sun" for t in dna_tokens)

    drafts = pipeline.generate_asset_drafts(campaign_id, direction_id, count=4)
    assert len(drafts) == 4
    assert drafts[0].is_hero is True
    assert drafts[0].channel == "E-commerce Hero"


def test_cryptographic_lineage_graph_integrity():
    graph = AssetLineageGraph()
    campaign_id = "camp_lin_01"
    asset_id = "ast_hero_01"

    nodes = graph.build_standard_asset_lineage(
        campaign_id=campaign_id,
        mission_id="mis_01",
        direction_id="dir_01",
        dna_id="dna_01",
        prompt_id="prm_01",
        model_id="mdl_01",
        render_id="rnd_01",
        approval_id="app_01",
        delivery_id="del_01",
        asset_id=asset_id,
    )
    assert len(nodes) == 9
    assert graph.verify_lineage_integrity(asset_id) is True

    # Tampering with a node in the trace should fail verification
    trace = graph.get_lineage_trace(asset_id)
    assert len(trace) == 9
    trace[4].metadata["prompt_id"] = "TAMPERED_PROMPT"
    assert graph.verify_lineage_integrity(asset_id) is False

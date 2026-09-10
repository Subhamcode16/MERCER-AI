"""
Tests for Phase 28 Outcome Normalization and Version Linkage.
"""
import pytest
from src.creative_learning.outcome_normalization import OutcomeNormalizer
from src.creative_learning.outcome_linkage import OutcomeLinkageGraph


def test_outcome_normalization_multi_metric():
    normalizer = OutcomeNormalizer()
    campaign_id = "camp_norm_01"

    raw_metrics = {
        "impressions": 200000,
        "clicks": 6000,
        "conversions": 480,
        "avg_dwell_sec": 18.5,
    }
    metrics = normalizer.normalize_feed(campaign_id, "ShopifyStorefront", raw_metrics)
    metric_map = {m.metric_name: m for m in metrics}

    assert metric_map["IMPRESSIONS"].normalized_value == 200000.0
    assert metric_map["CTR"].normalized_value == 0.03
    assert metric_map["CONVERSION_RATE"].normalized_value == 0.08
    assert metric_map["AVG_DWELL_TIME_SEC"].normalized_value == 18.5
    assert "Correlational" in metric_map["CTR"].attribution_model


def test_outcome_linkage_to_exact_launched_asset_version():
    graph = OutcomeLinkageGraph()
    campaign_id = "camp_link_01"
    asset_id = "ast_hero_01"

    node = graph.link_outcome(
        campaign_id=campaign_id,
        direction_id="dir_01",
        asset_id=asset_id,
        asset_version=1,
        channel="E-commerce Hero",
        metric_ids=["met_01", "met_02"],
        production_release_version=1,
    )
    assert node.asset_version == 1
    assert node.channel == "E-commerce Hero"

    linked = graph.get_linkage_for_asset(asset_id)
    assert len(linked) == 1
    assert linked[0].linkage_id == node.linkage_id

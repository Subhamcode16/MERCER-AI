"""
Tests for Phase 28 Epistemic Attribution and Counterfactual Modeling.
"""
import pytest
from src.creative_learning.attribution import (
    AttributionEngine,
    EvidenceCausalStatus,
)
from src.creative_learning.counterfactuals import (
    CounterfactualEngine,
    CounterfactualState,
)


def test_attribution_confounder_detection_and_epistemic_qualification():
    engine = AttributionEngine()
    assessment = engine.evaluate_attribution(
        campaign_id="camp_att_01",
        asset_id="ast_01",
        raw_lift=18.5,
        is_controlled_ab_test=False,
    )
    assert assessment.causal_status == EvidenceCausalStatus.CONFOUNDED
    assert len(assessment.detected_confounders) >= 1
    assert "Outcome ≠ Causation" in assessment.epistemic_disclaimer


def test_counterfactual_tree_unknown_preservation():
    engine = CounterfactualEngine()
    tree = engine.build_counterfactual_tree(
        campaign_id="camp_cf_01",
        chosen_decision="Selected Monolithic Limestone",
        observed_outcome="CTR: 3.4%",
        unselected_alternatives=["Vibrant Cyber Neon", "Pastel Botanical"],
    )
    assert len(tree.alternative_branches) == 2
    for branch in tree.alternative_branches:
        assert branch.state == CounterfactualState.COUNTERFACTUAL_UNKNOWN
        assert branch.estimated_outcome_range is None
        assert "Unknown Must Survive" in branch.epistemic_warning

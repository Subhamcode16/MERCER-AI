"""
Phase 28 Adversarial Validation Test Suite.
Tests defense against poisoned feeds, manipulated attribution, fake experiments, and causal language injection.
"""
import pytest
from src.creative_learning.outcome_ingestion import OutcomeIngestionPipeline
from src.creative_learning.attribution import AttributionEngine, EvidenceCausalStatus
from src.creative_learning.learning_governance import LearningGovernanceEngine
from src.creative_learning.hypotheses import LearningHypothesisStore
from src.creative_learning.counterfactuals import CounterfactualEngine, CounterfactualState


def test_adversarial_poisoned_outcome_payload():
    pipeline = OutcomeIngestionPipeline()
    feed = pipeline.ingest_feed(
        campaign_id="camp_adv_01",
        source_platform="CompromisedAnalytics",
        metrics_payload={"impressions": -500, "conversions": 999999999},
        source_signature="MOCK_INJECTION_POISONED_PAYLOAD",
    )
    assert feed.is_verified is False


def test_adversarial_causal_language_injection():
    gov = LearningGovernanceEngine()
    injections = [
        "This visual style proves causality across all customer demographics.",
        "Guarantees success and caused 100% of sales lift.",
        "Universally true for all clients globally without exception.",
    ]
    for inj in injections:
        eval_res = gov.evaluate_learning_claim(inj)
        assert eval_res.is_compliant is False


def test_adversarial_fabricated_counterfactual_rejection():
    engine = CounterfactualEngine()
    tree = engine.build_counterfactual_tree("c1", "Decision A", "Observed A", ["Alternative B", "Alternative C"])
    for b in tree.alternative_branches:
        assert b.state == CounterfactualState.COUNTERFACTUAL_UNKNOWN
        assert b.estimated_outcome_range is None

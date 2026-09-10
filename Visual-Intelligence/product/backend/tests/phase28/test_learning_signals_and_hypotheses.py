"""
Tests for Phase 28 Learning Signals and Hypothesis Management.
"""
import pytest
from src.creative_learning.learning_signals import (
    LearningSignalGenerator,
    LearningSignalType,
)
from src.creative_learning.hypotheses import (
    LearningHypothesisStore,
    HypothesisScope,
)


def test_learning_signal_classification():
    gen = LearningSignalGenerator()
    
    # Positive signal
    sig_pos = gen.evaluate_signal("camp_01", "token:raking_sun", "CTR", 0.042, 0.030, sample_size=1500)
    assert sig_pos.signal_type == LearningSignalType.POSITIVE_SIGNAL
    assert sig_pos.delta_percentage == 40.0
    assert sig_pos.confidence >= 0.75

    # Insufficient evidence for tiny sample
    sig_tiny = gen.evaluate_signal("camp_01", "token:raking_sun", "CTR", 0.050, 0.020, sample_size=40)
    assert sig_tiny.signal_type == LearningSignalType.INSUFFICIENT_EVIDENCE
    assert sig_tiny.confidence == 0.3


def test_hypothesis_creation_and_contradiction_updating():
    store = LearningHypothesisStore()
    hyp = store.create_hypothesis(
        statement="Raking late sun lighting increases high-tailoring dwell time by +25%",
        originating_campaigns=["camp_01"],
        supporting_evidence=["Observed +40% CTR and +18s dwell time in Autumn launch."],
        scope=HypothesisScope.BRAND,
        confidence=0.88,
    )
    assert hyp.status == "PROVISIONAL"
    assert len(hyp.contradicting_evidence) == 0

    # Add contradicting evidence
    updated = store.add_contradicting_evidence(
        hyp.hypothesis_id,
        "Spring Lookbook testing showed zero dwell time delta in natural soft diffused light.",
    )
    assert len(updated.contradicting_evidence) == 1
    assert updated.confidence < 0.88

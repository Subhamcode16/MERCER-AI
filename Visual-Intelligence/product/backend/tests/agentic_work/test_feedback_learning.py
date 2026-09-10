"""
Tests for FeedbackEngine and LearningEngine.
"""

from src.agentic_work import FeedbackEngine, LearningEngine, AdaptiveStatus


def test_feedback_and_learning_flow():
    fb = FeedbackEngine()
    learn = LearningEngine()

    sig = fb.create_signal(
        workflow_id="wf1",
        source="CRITIC_FEEDBACK",
        category="PROMPT_TEMPLATE",
        observed_failure="Color clash",
        expected_behavior="Warm neutral",
        correction="Enforce neutral palette rule",
        confidence=0.85,
    )

    change = learn.ingest_signal(sig)
    assert change is not None
    assert change.status == AdaptiveStatus.ACTIVE

    rolled_back = learn.rollback_change(change.change_id)
    assert rolled_back is True
    assert change.status == AdaptiveStatus.ROLLED_BACK

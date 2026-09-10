"""
Phase 9 — Persistent Feedback Engine Unit Tests
"""

import shutil
import tempfile
import pytest

from src.agentic_work.memory_models import FeedbackRecord, FeedbackSource
from src.agentic_work.persistent_feedback import (
    PersistentFeedbackEngine,
    DuplicateFeedbackError,
)


@pytest.fixture
def temp_feedback_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_feedback_replay_defense(temp_feedback_dir):
    engine = PersistentFeedbackEngine(base_dir=temp_feedback_dir)

    fb = FeedbackRecord(
        feedback_id="fb_101",
        workflow_id="wf_01",
        source=FeedbackSource.USER,
        category="TYPOGRAPHY",
        target_role="DESIGNER",
        rating=0.4,
        comments="Typography hierarchy needs improvement",
        defect_code="WEAK_TYPOGRAPHY",
    )

    engine.record_feedback(fb)

    # Re-recording same feedback_id must fail with DuplicateFeedbackError
    with pytest.raises(DuplicateFeedbackError):
        engine.record_feedback(fb)


def test_feedback_n_threshold_aggregation(temp_feedback_dir):
    engine = PersistentFeedbackEngine(base_dir=temp_feedback_dir, aggregation_threshold=3)

    # Initially 0 patterns
    assert len(engine.aggregate_learning_patterns()) == 0

    # Add 2 feedback records (under threshold)
    for i in range(1, 3):
        fb = FeedbackRecord(
            feedback_id=f"fb_{i}",
            workflow_id=f"wf_{i}",
            source=FeedbackSource.CRITIC_SYSTEM,
            category="CRITIQUE_DEFECT",
            target_role="DESIGNER",
            rating=0.3,
            comments="Typography alignment issue",
            defect_code="DEFECT_TYPO_ALIGN",
        )
        engine.record_feedback(fb)

    assert len(engine.aggregate_learning_patterns()) == 0

    # Add 3rd feedback record (reaching N=3 threshold)
    fb3 = FeedbackRecord(
        feedback_id="fb_3",
        workflow_id="wf_3",
        source=FeedbackSource.CRITIC_SYSTEM,
        category="CRITIQUE_DEFECT",
        target_role="DESIGNER",
        rating=0.2,
        comments="Typography alignment issue",
        defect_code="DEFECT_TYPO_ALIGN",
    )
    engine.record_feedback(fb3)

    patterns = engine.aggregate_learning_patterns()
    assert len(patterns) == 1
    p = patterns[0]
    assert p.target_role == "DESIGNER"
    assert p.trigger_defect_code == "DEFECT_TYPO_ALIGN"
    assert p.occurrence_count == 3
    assert len(p.supporting_feedback_ids) == 3

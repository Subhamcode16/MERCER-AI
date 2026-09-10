"""
Tests for CritiqueEngine and ReviewEngine.
"""

from src.agentic_work import CritiqueEngine, ReviewEngine


def test_critique_engine_detects_color_defect():
    critique = CritiqueEngine()
    output_defective = {
        "color_palette": {"accent_tint": "#FF0000"},
        "has_defect": True,
    }
    res = critique.evaluate_output("t4_design", output_defective)

    assert res.passed is False
    assert res.score < 0.50
    assert len(res.findings) > 0


def test_review_engine_evaluates_package():
    reviewer = ReviewEngine()
    res = reviewer.perform_review("wf1", {"artifacts": []}, [{"passed": True}])

    assert res.approved is True
    assert res.is_authoritative is False

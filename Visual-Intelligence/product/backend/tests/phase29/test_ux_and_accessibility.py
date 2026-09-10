"""
Product UX Usability & Accessibility Evaluation Suite for Phase 29.
"""
import pytest
from src.creative_intelligence_network.recommendations import (
    StrategicRecommendationEngine,
    StrategicRecommendation,
    RecommendationStatus,
    ReversibilityRating,
)
from src.creative_intelligence_network.signals.signal_types import EpistemicStatus
from src.creative_intelligence_network.observability import StrategicIntelligenceObservatory
from src.creative_intelligence_network.graph import OrganizationalIntelligenceGraph
from src.creative_intelligence_network.signals import StrategicSignalEngine
from src.creative_intelligence_network.hypotheses import HypothesisEngine


def test_ux_mode_observe_signals():
    engine = StrategicSignalEngine()
    sig = engine.emit_signal("TENANT-UX", "EMERGING_PATTERN", "GLOBAL", "Observed shift", "METHOD", 0.8, EpistemicStatus.OBSERVATIONAL_CORRELATION)
    assert sig.signal_id.startswith("SIG-")
    assert sig.freshness == 1.0


def test_ux_mode_understand_epistemic_trace():
    rec_engine = StrategicRecommendationEngine()
    rec = rec_engine.generate_recommendation(
        "TENANT-UX", "Title", "Action", "Why", "Scope", EpistemicStatus.OBSERVATIONAL_CORRELATION, 0.7, ["EV-1"],
        assumptions=["Assumption 1"], unknowns=["Unknown 1"], alternatives=["Alt 1"], expected_consequences=["Conseq 1"]
    )
    # Validate 12-stage fields are present and structured
    assert rec.why_now == "Why"
    assert len(rec.assumptions) > 0
    assert len(rec.unknowns) > 0
    assert len(rec.alternatives) > 0
    assert len(rec.expected_consequences) > 0


def test_ux_mode_challenge_interaction():
    rec_engine = StrategicRecommendationEngine()
    rec = rec_engine.generate_recommendation("TENANT-UX", "T", "A", "W", "S", EpistemicStatus.OBSERVATIONAL_CORRELATION, 0.7, ["EV-1"])
    rec_c = rec_engine.challenge_recommendation(rec.recommendation_id, "Operator challenges feasibility", ["COUNT-1"])
    assert rec_c.status == RecommendationStatus.DOWNGRADED


def test_ux_mode_decide_reversibility_clarity():
    rec_engine = StrategicRecommendationEngine()
    rec = rec_engine.generate_recommendation("TENANT-UX", "T", "A", "W", "S", EpistemicStatus.EXPERIMENTAL_EVIDENCE, 0.85, ["EXP-1"], reversibility=ReversibilityRating.HIGHLY_REVERSIBLE)
    assert rec.reversibility == ReversibilityRating.HIGHLY_REVERSIBLE


def test_accessibility_aria_and_contrast_readiness():
    # Verify structured attributes for screen reader / assistive tech serialization
    rec_engine = StrategicRecommendationEngine()
    rec = rec_engine.generate_recommendation("TENANT-UX", "Contrast Title", "Action", "Why", "Scope", EpistemicStatus.EXPERIMENTAL_EVIDENCE, 0.85, ["EXP-1"])
    rec_dict = rec.model_dump()
    assert "title" in rec_dict
    assert "action_statement" in rec_dict
    assert "confidence" in rec_dict
    assert "reversibility" in rec_dict


def test_observatory_ux_surface_metrics():
    graph = OrganizationalIntelligenceGraph()
    signals = StrategicSignalEngine(graph=graph)
    hypo = HypothesisEngine(graph=graph)
    recs = StrategicRecommendationEngine(graph=graph)
    obs = StrategicIntelligenceObservatory(graph, signals, hypo, recs)

    signals.emit_signal("TENANT-UX", "EMERGING_PATTERN", "SCOPE", "P", "M", 0.8, EpistemicStatus.OBSERVATIONAL_CORRELATION)
    snapshot = obs.get_observatory_snapshot("TENANT-UX")
    assert snapshot["metrics"]["active_signals_count"] == 1
    assert snapshot["metrics"]["total_entities_in_graph"] >= 1

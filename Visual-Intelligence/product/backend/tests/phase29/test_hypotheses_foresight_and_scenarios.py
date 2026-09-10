"""
Unit & Integration Tests for Hypotheses, Foresight Scenarios, Opportunities & Risks.
"""
import pytest
from src.creative_intelligence_network.hypotheses import (
    HypothesisEngine,
    HypothesisStatus,
    StrategicHypothesis,
)
from src.creative_intelligence_network.foresight import (
    ForesightEngine,
    ScenarioArchetype,
)
from src.creative_intelligence_network.opportunities import (
    OpportunityEngine,
    OpportunityTier,
)
from src.creative_intelligence_network.risks import (
    RiskEngine,
    RiskSeverity,
)


def test_hypothesis_lifecycle_transitions():
    engine = HypothesisEngine()
    hypo = engine.propose_hypothesis(
        tenant_id="TENANT-LUXE",
        statement="Asymmetric product framing boosts luxury brand retention by 15%",
        scope="LUXURY_JEWELRY",
        falsification_criteria="Drop in 3-second hook retention below 25%",
        origin_signals=["SIG-001"],
        initial_confidence=0.60,
    )

    assert hypo.status == HypothesisStatus.PROPOSED
    assert hypo.confidence == 0.60

    # Transition to TESTABLE
    hypo = engine.transition_status(
        hypothesis_id=hypo.hypothesis_id,
        new_status=HypothesisStatus.TESTABLE,
        reason="Experiment setup validated",
        tenant_id="TENANT-LUXE",
    )
    assert hypo.status == HypothesisStatus.TESTABLE

    # Transition to SUPPORTED with evidence
    hypo = engine.transition_status(
        hypothesis_id=hypo.hypothesis_id,
        new_status=HypothesisStatus.SUPPORTED,
        reason="A/B experiment confirmed 18% lift",
        evidence_ref="EXP-AB-01",
        tenant_id="TENANT-LUXE",
    )
    assert hypo.status == HypothesisStatus.SUPPORTED
    assert "EXP-AB-01" in hypo.supporting_evidence


def test_hypothesis_model_confidence_invariant():
    engine = HypothesisEngine()
    hypo = engine.propose_hypothesis(
        tenant_id="TENANT-LUXE",
        statement="Statement without experimental evidence",
        scope="GENERAL",
        falsification_criteria="CTR drop",
        initial_confidence=0.99,
    )

    # Invariant: Attempting to mark SUPPORTED without supporting evidence reverts to UNKNOWN
    hypo = engine.transition_status(
        hypothesis_id=hypo.hypothesis_id,
        new_status=HypothesisStatus.SUPPORTED,
        reason="Model claims high confidence",
        tenant_id="TENANT-LUXE",
    )
    assert hypo.status == HypothesisStatus.UNKNOWN


def test_5_scenario_foresight_matrix():
    engine = ForesightEngine()
    matrix = engine.construct_scenario_matrix(
        tenant_id="TENANT-LUXE",
        scope="AUTUMN_WINTER_CAMPAIGN",
        topic="Minimalist Monochrome Creative Shift",
        initiating_signals=["SIG-V01", "SIG-V02"],
        base_assumptions=["Macro consumer luxury spend remains resilient"],
    )

    assert len(matrix) == 5
    assert ScenarioArchetype.BASELINE in matrix
    assert ScenarioArchetype.UPSIDE in matrix
    assert ScenarioArchetype.DOWNSIDE in matrix
    assert ScenarioArchetype.DISRUPTION in matrix
    assert ScenarioArchetype.UNKNOWN in matrix

    # Verify uncertainty preservation in UNKNOWN archetype
    unknown_scenario = matrix[ScenarioArchetype.UNKNOWN]
    assert unknown_scenario.uncertainty_score >= 0.90
    assert len(unknown_scenario.leading_indicators) > 0


def test_opportunity_and_risk_intelligence():
    opp_engine = OpportunityEngine()
    risk_engine = RiskEngine()

    opp = opp_engine.register_opportunity(
        tenant_id="TENANT-LUXE",
        title="TikTok Luxury Storytelling Format",
        description="Pioneering cinematic micro-vlogs for luxury handbags",
        scope="SOCIAL_VIDEO",
        tier=OpportunityTier.EXPERIMENT_REQUIRED,
        expected_upside="Estimated +25% organic shares",
        decision_required="Allocate $15k exploratory experiment budget",
    )
    assert opp.tier == OpportunityTier.EXPERIMENT_REQUIRED

    risk = risk_engine.register_risk(
        tenant_id="TENANT-LUXE",
        title="Ad Fatigue in Monochromatic Visuals",
        description="Repeated exposure to grayscale ads causes 30% CTR drop after day 10",
        scope="VISUAL_CREATIVE",
        severity=RiskSeverity.HIGH,
        mitigation_options=["Implement dynamic accent color rotation every 7 days"],
        escalation_required=True,
    )
    assert risk.severity == RiskSeverity.HIGH
    assert risk.escalation_required is True

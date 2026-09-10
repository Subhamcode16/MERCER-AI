"""
Unit & Integration Tests for Strategic Recommendations, Quality Contracts, Bridge & Decision Memory.
"""
import pytest
from src.creative_intelligence_network.recommendations import (
    StrategicRecommendationEngine,
    RecommendationStatus,
    ReversibilityRating,
    RecommendationQualityContract,
)
from src.creative_intelligence_network.signals.signal_types import EpistemicStatus
from src.creative_intelligence_network.bridge import (
    IntelligenceToCampaignBridge,
    HumanDecisionRecord,
)
from src.creative_intelligence_network.decision_memory import (
    StrategicDecisionMemoryStore,
    DecisionQualityGrade,
)


def test_recommendation_generation_and_quality_audit():
    engine = StrategicRecommendationEngine()
    
    rec = engine.generate_recommendation(
        tenant_id="TENANT-LUXE",
        title="Pivot to Kinetic Pacing on Instagram Reels",
        action_statement="Increase transition cut rate from 4.0s to 1.8s for Gen-Z segment.",
        why_now="CTR has dropped 22% on slow-paced creative over the past 14 days.",
        scope="INSTAGRAM_REELS",
        epistemic_status=EpistemicStatus.EXPERIMENTAL_EVIDENCE,
        initial_confidence=0.88,
        supporting_evidence=["EXP-CUT-01", "EXP-CUT-02"],
        reversibility=ReversibilityRating.HIGHLY_REVERSIBLE,
        proposed_experiment="Run 50/50 split test on 10k impressions",
    )

    assert rec.status == RecommendationStatus.PROPOSED
    assert rec.confidence == 0.88
    assert rec.provenance_hash != ""


def test_recommendation_quality_contract_downgrades():
    engine = StrategicRecommendationEngine()

    # Case 1: High contradiction ratio triggers automatic confidence downgrade
    rec_conflicted = engine.generate_recommendation(
        tenant_id="TENANT-LUXE",
        title="Controversial Layout Shift",
        action_statement="Adopt brutalist wireframe styling across all brand assets.",
        why_now="Single trend report showed spike.",
        scope="GLOBAL",
        epistemic_status=EpistemicStatus.OBSERVATIONAL_CORRELATION,
        initial_confidence=0.90,
        supporting_evidence=["EV-01"],
        contradicting_evidence=["EV-COUNT-01", "EV-COUNT-02"],  # Contradictions exceed support!
    )

    assert rec_conflicted.status == RecommendationStatus.DOWNGRADED
    assert rec_conflicted.confidence < 0.60


def test_recommendation_challenge_workflow():
    engine = StrategicRecommendationEngine()
    rec = engine.generate_recommendation(
        tenant_id="TENANT-LUXE",
        title="Expand Brand into Mass Fast-Fashion Channels",
        action_statement="Launch Meta dynamic ads targeting discount shoppers.",
        why_now="Potential short-term volume growth.",
        scope="META_ADS",
        epistemic_status=EpistemicStatus.OBSERVATIONAL_CORRELATION,
        initial_confidence=0.70,
        supporting_evidence=["EV-VOL-01"],
    )

    # Human operator challenges recommendation
    rec_challenged = engine.challenge_recommendation(
        recommendation_id=rec.recommendation_id,
        operator_notes="Dilutes luxury heritage prestige and risks 40% VIP customer churn.",
        new_counterevidence=["VIP-CHURN-REPORT-2026", "BRAND-EQUITY-SURVEY"],
        tenant_id="TENANT-LUXE",
    )

    assert rec_challenged.status == RecommendationStatus.DOWNGRADED
    assert "Dilutes luxury heritage prestige" in rec_challenged.challenge_notes[0]
    assert rec_challenged.confidence < 0.50


def test_intelligence_to_campaign_bridge_and_decision_memory():
    bridge = IntelligenceToCampaignBridge()
    memory_store = StrategicDecisionMemoryStore()
    engine = StrategicRecommendationEngine()

    rec = engine.generate_recommendation(
        tenant_id="TENANT-LUXE",
        title="Launch Micro-Drop Capsule Campaign",
        action_statement="Deploy 3 limited-run silk scarf designs on Friday 6 PM.",
        why_now="VIP engagement spikes during Friday evening time window.",
        scope="VIP_CAPSULE",
        epistemic_status=EpistemicStatus.EXPERIMENTAL_EVIDENCE,
        initial_confidence=0.85,
        supporting_evidence=["EXP-VIP-DROP-01"],
        reversibility=ReversibilityRating.MODERATELY_REVERSIBLE,
    )

    # Invariant: Unauthorized role cannot approve strategic campaign execution
    with pytest.raises(PermissionError):
        bridge.record_human_decision_and_create_campaign(
            tenant_id="TENANT-LUXE",
            decision_maker="junior_intern",
            decision_maker_role="ANALYST_READONLY",
            recommendation=rec,
            operator_rationale="Looks good",
        )

    # Authorized Human Operator Approves Decision
    decision = bridge.record_human_decision_and_create_campaign(
        tenant_id="TENANT-LUXE",
        decision_maker="sarah_creative_director",
        decision_maker_role="CAMPAIGN_DIRECTOR",
        recommendation=rec,
        operator_rationale="Strong experiment backing and zero brand equity conflict.",
    )

    assert decision.resulting_campaign_id is not None
    assert rec.status == RecommendationStatus.ACCEPTED

    # Record Decision Memory
    memory_record = memory_store.record_decision_memory(
        decision=decision,
        decision_quality_grade=DecisionQualityGrade.HIGH_RIGOR_EVIDENCE_BOUND,
    )
    assert memory_record.decision_quality_grade == DecisionQualityGrade.HIGH_RIGOR_EVIDENCE_BOUND

    # Subsequent Outcome Update (6 weeks later)
    updated_memory = memory_store.update_subsequent_outcome(
        record_id=memory_record.record_id,
        metrics={"sell_through_rate": 0.94, "roas": 3.82},
        outcome_alignment="ALIGNED",
        retrospective_learnings=["Friday 6 PM VIP release window confirmed as high-velocity."],
        tenant_id="TENANT-LUXE",
    )
    assert updated_memory.outcome_alignment == "ALIGNED"
    assert updated_memory.subsequent_outcome_metrics["roas"] == 3.82

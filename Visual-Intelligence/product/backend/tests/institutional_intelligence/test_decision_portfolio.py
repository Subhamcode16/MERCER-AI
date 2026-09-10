"""
Tests for Strategic Decisions and Decision Portfolio (Phase 30).
"""
import pytest
from datetime import datetime, timedelta, timezone
from src.institutional_intelligence.types import (
    ThreatID,
    GovernanceInvariantViolation,
    utc_now,
)
from src.institutional_intelligence.decisions.models import (
    StrategicDecision,
    DecisionAlternative,
    HumanDecisionCapture,
    DecisionQualityAssessment,
    OutcomeQualityAssessment,
)
from src.institutional_intelligence.portfolio.service import (
    DecisionPortfolioService,
    DecisionAttentionScore,
)


def test_strategic_decision_lifecycle_and_hash():
    decision = StrategicDecision(
        tenant_id="tenant_01",
        strategic_objective_id="obj_123",
        decision_question="Should we launch digital atelier in Q3?",
        owner="human_director_42",
        evidence_set=["ev_report_q2"],
        alternatives=[
            DecisionAlternative(title="Launch in Q3", description="Immediate launch"),
            DecisionAlternative(title="Defer to Q4", description="Wait for market stabilization")
        ],
        uncertainty=0.4
    )
    initial_hash = decision.calculate_record_hash()
    assert initial_hash != ""
    assert decision.status == "DRAFT"

    capture = HumanDecisionCapture(
        decision_maker="human_director_42",
        authorization_token="AUTH_SIGNATURE_VALID_001",
        selected_alternative_id=decision.alternatives[0].alternative_id,
        rejected_alternative_ids=[decision.alternatives[1].alternative_id],
        rationale="Strong competitor whitespace in Q3.",
        authorization_scope="CAMPAIGN_PREPARATION_ONLY"
    )
    decision.record_human_decision(capture, actor="human_director_42")
    assert decision.status == "DECIDED"
    assert decision.human_decision.signature_hash != ""
    assert len(decision.amendments) == 1


def test_t30_006_cannot_decide_on_superseded_or_invalidated_decision():
    decision = StrategicDecision(
        tenant_id="tenant_01",
        strategic_objective_id="obj_123",
        decision_question="Outdated question",
        owner="human_director_42"
    )
    decision.supersede("dec_999", actor="human_director_42", rationale="Superseded by new direction")
    assert decision.status == "SUPERSEDED"

    capture = HumanDecisionCapture(
        decision_maker="human_director_42",
        authorization_token="AUTH_TOKEN_TEST",
        selected_alternative_id="alt_1",
        rationale="Test",
        authorization_scope="TEST"
    )
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        decision.record_human_decision(capture, actor="human_director_42")
    assert excinfo.value.threat_id == ThreatID.T30_006


def test_decision_and_outcome_quality_separation():
    # Invariant: Decision Quality != Outcome Quality
    dq = DecisionQualityAssessment(
        evidence_sufficiency=0.9,
        reasoning_quality=0.85,
        alternative_consideration=0.9,
        composite_decision_quality=0.88
    )
    oq = OutcomeQualityAssessment(
        observed_business_result=0.3,  # Outcome was poor due to external macroeconomic crash
        objective_progress=0.4,
        evaluation_notes="High quality decision made under uncertainty; macroeconomic shock affected outcome."
    )
    decision = StrategicDecision(
        tenant_id="tenant_01",
        strategic_objective_id="obj_123",
        decision_question="Enter new emerging region?",
        owner="human_director_42",
        decision_quality=dq,
        outcome_quality=oq
    )
    assert decision.decision_quality.composite_decision_quality == 0.88
    assert decision.outcome_quality.observed_business_result == 0.3


def test_portfolio_service_attention_ranking():
    svc = DecisionPortfolioService(tenant_id="tenant_01")
    
    d1 = StrategicDecision(
        decision_id="dec_urgent",
        tenant_id="tenant_01",
        strategic_objective_id="obj_1",
        decision_question="Urgent launch decision",
        owner="human_1",
        deadline=utc_now() + timedelta(days=1),
        uncertainty=0.8,
        evidence_set=[]  # Lacks evidence -> high attention
    )
    d2 = StrategicDecision(
        decision_id="dec_future",
        tenant_id="tenant_01",
        strategic_objective_id="obj_2",
        decision_question="Future long term direction",
        owner="human_2",
        deadline=utc_now() + timedelta(days=60),
        uncertainty=0.2,
        evidence_set=["ev_1", "ev_2"]
    )
    svc.add_decision(d1)
    svc.add_decision(d2)

    ranked = svc.rank_attention_queue()
    assert len(ranked) == 2
    assert ranked[0].decision_id == "dec_urgent"
    assert ranked[0].attention_score > ranked[1].attention_score


def test_t30_005_portfolio_ranking_does_not_grant_budget():
    svc = DecisionPortfolioService(tenant_id="tenant_01")
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        svc.assert_budget_boundary(actor="ai_strategy_worker", requested_budget=50000.0)
    assert excinfo.value.threat_id == ThreatID.T30_005


def test_t30_017_cross_tenant_decision_insertion_blocked():
    svc = DecisionPortfolioService(tenant_id="tenant_A")
    d_foreign = StrategicDecision(
        tenant_id="tenant_B",
        strategic_objective_id="obj_b",
        decision_question="Foreign tenant question",
        owner="human_b"
    )
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        svc.add_decision(d_foreign)
    assert excinfo.value.threat_id == ThreatID.T30_017

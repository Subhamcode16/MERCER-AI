"""
Tests for the 6 Core Integration Workflows (A through F) (Phase 30).
"""
import pytest
from src.institutional_intelligence.types import (
    StrategicHorizon,
    StrategicCadenceType,
    WorkerRole,
    EpistemicStatus,
)
from src.institutional_intelligence.objectives.models import StrategicObjective
from src.institutional_intelligence.decisions.models import (
    StrategicDecision,
    DecisionAlternative,
    HumanDecisionCapture,
)
from src.institutional_intelligence.initiatives.models import StrategicInitiative
from src.institutional_intelligence.portfolio.service import DecisionPortfolioService
from src.institutional_intelligence.assumptions.monitor import StrategicAssumption, AssumptionMonitor
from src.institutional_intelligence.drift.detector import StrategicDriftDetector
from src.institutional_intelligence.review.engine import StrategicReviewEngine
from src.institutional_intelligence.bridge.bridges import StrategicExecutionBridge
from src.institutional_intelligence.cadence.engine import StrategicCadenceEngine
from src.institutional_intelligence.prioritization.queue import AttentionQueueItem, IntelligenceAttentionQueue


def test_workflow_a_strategic_review():
    tenant_id = "tenant_wf_a"
    # 1. Objective
    obj = StrategicObjective(tenant_id=tenant_id, owner="human_dir", creation_authority="AUTH_A", title="European Expansion", description="Desc", scope="EUROPE")
    # 2. Portfolio Decision
    decision = StrategicDecision(tenant_id=tenant_id, strategic_objective_id=obj.objective_id, decision_question="Enter Milan Market?", owner="human_dir", alternatives=[DecisionAlternative(title="Open Milan Boutique", description="D")])
    # 3. Drift Detection
    detector = StrategicDriftDetector(tenant_id=tenant_id)
    drift = detector.detect_drift("DRIFT", decision.decision_id, "Market Rent Rise", "Rents up 20%", 0.7, ["ev_rent"])
    # 4. Review Engine
    review_engine = StrategicReviewEngine(tenant_id=tenant_id)
    brief = review_engine.generate_review(
        title="Milan Entry Strategy Review",
        changes=["Rents up 20%"],
        material_points=["High visibility location"],
        uncertainties=["Q4 consumer confidence"],
        contradictions=[],
        attention_decisions=[decision.decision_id],
        initiative_updates=[],
        opportunities=["Pop-up store alternative"],
        risks=["High overhead fixed leases"],
        expired_assumptions=[],
        scenarios=["Base Case"],
        human_actions=["Decide on pop-up vs lease"],
        unknowns=["Competitor popup timeline"],
        evidence_provenance=["ev_rent"],
        recommendation="Pursue pop-up boutique before long term lease."
    )
    # 5. Human Decision
    capture = HumanDecisionCapture(
        decision_maker="human_dir",
        authorization_token="AUTH_TOKEN_MILAN_2026",
        selected_alternative_id=decision.alternatives[0].alternative_id,
        rationale="Approved with pop-up contingency.",
        authorization_scope="MILAN_POPUP_PREPARATION"
    )
    decision.record_human_decision(capture, actor="human_dir")
    assert decision.status == "DECIDED"
    assert brief.brief_hash != ""


def test_workflow_b_decision_to_campaign():
    tenant_id = "tenant_wf_b"
    bridge = StrategicExecutionBridge(tenant_id=tenant_id)
    # Decision -> Authorized Initiative -> Campaign Proposal -> Human Approval -> Execution
    init = StrategicInitiative(tenant_id=tenant_id, strategic_objective_id="obj_b", title="Atelier Launch Initiative", description="D", owner="human_b", authorized_scope="ATELIER_CAMPAIGN")
    proposal = bridge.create_campaign_proposal(init.initiative_id, "dec_atelier_01", "Spring Atelier Campaign", "DIGITAL_AND_PRINT")
    assert proposal.is_human_approved is False

    approved = bridge.approve_proposal_by_human(proposal.proposal_id, approver_actor="human_b", auth_token="AUTH_HUMAN_SIGN_SECURE_TOKEN_01")
    assert approved.is_human_approved is True

    exec_res = bridge.execute_campaign(proposal.proposal_id, caller_agent="agent_campaign")
    assert exec_res["status"] == "FORWARDED_TO_EXECUTION_GATEWAY"


def test_workflow_c_outcome_to_strategy():
    tenant_id = "tenant_wf_c"
    bridge = StrategicExecutionBridge(tenant_id=tenant_id)
    record = bridge.ingest_phase28_outcome(
        campaign_id="cmp_101",
        initiative_id="init_101",
        metrics={"conversion_rate": 0.042, "roas": 3.8},
        learning="High visual affinity for raw silk textures in European demographics."
    )
    assert record.observed_metrics["roas"] == 3.8
    assert "silk textures" in record.phase28_learning_summary


def test_workflow_d_continuous_intelligence():
    tenant_id = "tenant_wf_d"
    cadence = StrategicCadenceEngine(tenant_id=tenant_id)
    queue = IntelligenceAttentionQueue(tenant_id=tenant_id)

    cad_rec = cadence.run_cadence_preparation(
        cadence_type=StrategicCadenceType.DAILY_PREPARATION,
        changes=["New textile trend emerging"],
        contradictions=[],
        assumption_updates=[]
    )
    item = AttentionQueueItem(
        tenant_id=tenant_id,
        category="EMERGING_SIGNAL",
        title="Emerging Raw Silk Trend",
        summary="Organic searches up 45%",
        urgency=0.8,
        strategic_impact=0.75
    )
    queue.enqueue(item)
    prioritized = queue.list_prioritized()
    assert len(prioritized) == 1
    assert prioritized[0].composite_priority > 50.0


def test_workflow_e_strategic_risk_escalation():
    tenant_id = "tenant_wf_e"
    detector = StrategicDriftDetector(tenant_id=tenant_id)
    risk_drift = detector.detect_drift(
        drift_type="OUTCOME_EXPECTATION_DIVERGENCE",
        target_id="init_supply_chain",
        title="Raw Material Cost Spike",
        divergence_summary="Fabric supplier prices surged 35%",
        severity=0.92,
        evidence_ids=["ev_supplier_invoice_q3"]
    )
    assert risk_drift.severity >= 0.90
    assert len(detector.list_active_drift_signals()) == 1


def test_workflow_f_strategic_drift_recovery():
    tenant_id = "tenant_wf_f"
    monitor = AssumptionMonitor(tenant_id=tenant_id)
    asm = StrategicAssumption(tenant_id=tenant_id, statement="Supplier contract locked for 12 months")
    monitor.register_assumption(asm, actor_role="STRATEGY_WORKER")
    
    # Contradiction triggers recovery
    asm.record_contradiction("ev_supplier_breach", "Supplier terminated contract early", "auditor_1")
    assert asm.status == "CONTRADICTED"

    init = StrategicInitiative(tenant_id=tenant_id, strategic_objective_id="obj_1", title="Production Run", description="D", owner="human_dir", authorized_scope="ORIGINAL")
    init.pause_initiative(actor="human_dir", reason="Contradicted supplier assumption - pausing for supplier renegotiation")
    assert init.is_paused is True

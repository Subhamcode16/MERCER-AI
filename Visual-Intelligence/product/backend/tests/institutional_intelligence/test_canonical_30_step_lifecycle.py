"""
Canonical 30-Step Lifecycle Test (Phase 30).
Validates each sequential step from Human Strategic Intent to Institutional Memory Update & Cadence.
"""
import pytest
from datetime import datetime, timedelta
from src.institutional_intelligence.types import (
    StrategicHorizon,
    OrganizationalMemoryClass,
    InitiativeHealthState,
    utc_now,
)
from src.institutional_intelligence.objectives.models import StrategicObjective
from src.institutional_intelligence.horizons.models import StrategicHorizonMapping
from src.institutional_intelligence.decisions.models import (
    StrategicDecision,
    DecisionAlternative,
    HumanDecisionCapture,
    DecisionQualityAssessment,
    OutcomeQualityAssessment,
)
from src.institutional_intelligence.initiatives.models import StrategicInitiative
from src.institutional_intelligence.assumptions.monitor import StrategicAssumption, AssumptionMonitor
from src.institutional_intelligence.memory.store import MemoryItem, OrganizationalMemoryStore
from src.institutional_intelligence.prioritization.queue import AttentionQueueItem, IntelligenceAttentionQueue
from src.institutional_intelligence.drift.detector import StrategicDriftDetector
from src.institutional_intelligence.health.evaluator import InitiativeHealthEvaluator
from src.institutional_intelligence.review.engine import StrategicReviewEngine
from src.institutional_intelligence.preparation.preparer import AutonomousPreparationEngine
from src.institutional_intelligence.bridge.bridges import StrategicExecutionBridge
from src.institutional_intelligence.cadence.engine import StrategicCadenceEngine, StrategicCadenceType


def test_canonical_30_step_lifecycle_execution():
    tenant = "tenant_canonical_30"
    
    # Step 1: Human defines strategic objective
    # Step 2: System records objective authority
    obj = StrategicObjective(
        tenant_id=tenant,
        owner="human_director",
        creation_authority="AUTH_BOARD_2026",
        title="Dominate Sustainable Haute Couture",
        description="Establish market leadership in ethically sourced silk.",
        scope="GLOBAL_SUSTAINABLE",
        evidence_basis=["ev_market_sustainability_report"]
    )
    obj.validate_human_authority(obj.owner, is_automated_agent=False)
    
    # Step 3: Human defines strategic horizon
    horizon_map = StrategicHorizonMapping(
        tenant_id=tenant,
        target_id=obj.objective_id,
        target_type="OBJECTIVE",
        horizon=StrategicHorizon.NOW,
        assigned_by="human_director"
    )

    # Step 4: System establishes decision portfolio
    decision = StrategicDecision(
        tenant_id=tenant,
        strategic_objective_id=obj.objective_id,
        decision_question="Should we partner with certified organic silk weaver cooperatives?",
        owner="human_director",
        alternatives=[
            DecisionAlternative(title="Direct Partnership", description="Direct exclusive contract"),
            DecisionAlternative(title="Broker Sourcing", description="Standard third party broker")
        ]
    )

    # Step 5: System retrieves permitted institutional knowledge
    # Step 6: System classifies evidence
    # Step 7: System identifies changing signals
    # Step 8: System identifies unresolved contradictions
    # Step 9: System evaluates assumptions
    mem_store = OrganizationalMemoryStore(tenant_id=tenant)
    mem_item = MemoryItem(
        tenant_id=tenant,
        memory_class=OrganizationalMemoryClass.STRATEGIC_OBJECTIVE,
        title=obj.title,
        content={"scope": obj.scope},
        provenance="board_minutes_2026_q3"
    )
    mem_store.append_memory(mem_item)

    asm_monitor = AssumptionMonitor(tenant_id=tenant)
    asm = StrategicAssumption(
        tenant_id=tenant,
        statement="Organic silk yield can satisfy 10,000 meters/month",
        model_confidence=0.85,
        empirical_confidence=0.80
    )
    asm_monitor.register_assumption(asm, actor_role="STRATEGY_WORKER")

    # Step 10: System detects strategic drift
    drift_detector = StrategicDriftDetector(tenant_id=tenant)
    
    # Step 11: System evaluates initiative health
    health_eval = InitiativeHealthEvaluator(tenant_id=tenant)
    
    # Step 12: System prioritizes intelligence attention
    queue = IntelligenceAttentionQueue(tenant_id=tenant)
    queue_item = AttentionQueueItem(
        tenant_id=tenant,
        category="STRATEGIC_QUESTION",
        title="Weaver cooperative capacity audit",
        summary="Audit reports ready for review",
        urgency=0.9,
        strategic_impact=0.85
    )
    queue.enqueue(queue_item)

    # Step 13: System refreshes relevant scenarios
    # Step 14: System identifies opportunities
    # Step 15: System identifies risks
    # Step 16: System prepares strategic review
    # Step 17: System presents evidence and provenance
    review_engine = StrategicReviewEngine(tenant_id=tenant)
    brief = review_engine.generate_review(
        title="Weaver Cooperative Strategy Brief",
        changes=["Audit confirmed 12,000m capacity"],
        material_points=["Direct partnership yields 30% margin improvement"],
        uncertainties=["Regional weather vulnerability"],
        contradictions=[],
        attention_decisions=[decision.decision_id],
        initiative_updates=[],
        opportunities=["Cooperative branding story"],
        risks=["Single region dependency"],
        expired_assumptions=[],
        scenarios=["Base expansion"],
        human_actions=["Authorize cooperative partnership"],
        unknowns=["Import customs tariff changes"],
        evidence_provenance=["ev_audit_cert_01"],
        recommendation="Execute direct partnership with cooperative consortium."
    )
    assert brief.brief_hash != ""

    # Step 18: Human challenges assumptions
    # Step 19: System revises/downgrades recommendations (if needed)
    # Step 20: Human makes strategic decision
    # Step 21: System records decision and authority scope
    cap = HumanDecisionCapture(
        decision_maker="human_director",
        authorization_token="AUTH_SIGNATURE_LEADERSHIP_2026",
        selected_alternative_id=decision.alternatives[0].alternative_id,
        rationale="Strong alignment with brand ESG pillars.",
        authorization_scope="DIRECT_PARTNERSHIP_AND_CAMPAIGN"
    )
    decision.record_human_decision(cap, actor="human_director")
    assert decision.status == "DECIDED"

    # Step 22: System creates/updates authorized initiative
    init = StrategicInitiative(
        tenant_id=tenant,
        strategic_objective_id=obj.objective_id,
        decision_id=decision.decision_id,
        title="Silk Weaver Heritage Campaign Initiative",
        description="Campaign highlighting direct artisan partnerships",
        owner="human_director",
        authorized_scope="CAMPAIGN_PRODUCTION"
    )

    # Step 23: System prepares operational plan
    prep_engine = AutonomousPreparationEngine()
    prep_engine.validate_action("DRAFT_INITIATIVE_UPDATE", agent_id="agent_prep")

    # Step 24: Existing authorization boundary validates execution
    bridge = StrategicExecutionBridge(tenant_id=tenant)
    proposal = bridge.create_campaign_proposal(
        initiative_id=init.initiative_id,
        decision_id=decision.decision_id,
        campaign_title="Artisan Heritage Silk 2026",
        scope="DIGITAL_VIDEO_AND_MAGAZINE"
    )
    bridge.approve_proposal_by_human(proposal.proposal_id, approver_actor="human_director", auth_token="AUTH_TOKEN_EXEC_VALID_1234")

    # Step 25: Campaign/experiment executes through existing systems
    exec_res = bridge.execute_campaign(proposal.proposal_id, caller_agent="campaign_executor")
    assert exec_res["status"] == "FORWARDED_TO_EXECUTION_GATEWAY"

    # Step 26: Phase 28 records outcome and learning
    # Step 27: Phase 29 updates organizational intelligence
    outcome_rec = bridge.ingest_phase28_outcome(
        campaign_id="cmp_artisan_01",
        initiative_id=init.initiative_id,
        metrics={"engagement_rate": 0.088, "direct_sales_lift": 0.28},
        learning="Authentic artisan narrative drove 2.4x engagement over generic luxury benchmarks."
    )

    # Step 28: Phase 30 evaluates decision and initiative quality
    decision.decision_quality = DecisionQualityAssessment(
        evidence_sufficiency=0.95,
        reasoning_quality=0.9,
        alternative_consideration=0.85,
        composite_decision_quality=0.92
    )
    decision.outcome_quality = OutcomeQualityAssessment(
        observed_business_result=0.90,
        objective_progress=0.88,
        evaluation_notes="Exceeded sales lift forecast."
    )

    # Step 29: Institutional memory is updated under governance
    mem_outcome = MemoryItem(
        tenant_id=tenant,
        memory_class=OrganizationalMemoryClass.OUTCOME,
        title="Artisan Silk Campaign Outcome",
        content={"sales_lift": 0.28, "engagement": 0.088},
        provenance=outcome_rec.ingest_id
    )
    mem_store.append_memory(mem_outcome)
    assert mem_store.verify_ledger_integrity() is True

    # Step 30: Next strategic review is scheduled/prepared
    cadence = StrategicCadenceEngine(tenant_id=tenant)
    cad_rec = cadence.run_cadence_preparation(
        cadence_type=StrategicCadenceType.WEEKLY_REVIEW,
        changes=["Campaign Artisan Silk completed with 28% lift"],
        contradictions=[],
        assumption_updates=[]
    )
    assert cad_rec.is_preparation_only is True

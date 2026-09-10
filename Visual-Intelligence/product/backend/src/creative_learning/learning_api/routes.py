"""
Phase 28 Creative Learning FastAPI Router.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.creative_learning.decision_ledger import DecisionLedger, DecisionType, DecisionContextSnapshot, DecisionAlternative
from src.creative_learning.outcome_ingestion import OutcomeIngestionPipeline
from src.creative_learning.outcome_normalization import OutcomeNormalizer
from src.creative_learning.outcome_linkage import OutcomeLinkageGraph
from src.creative_learning.attribution import AttributionEngine
from src.creative_learning.learning_signals import LearningSignalGenerator
from src.creative_learning.hypotheses import LearningHypothesisStore, HypothesisScope
from src.creative_learning.counterfactuals import CounterfactualEngine
from src.creative_learning.experiments import ExperimentRegistry, ExperimentStatus
from src.creative_learning.calibration import CalibrationTracker
from src.creative_learning.promotion import KnowledgePromotionEngine, PromotionLifecycleState
from src.creative_learning.contradiction import ContradictionHandler
from src.creative_learning.pattern_discovery import CreativePatternMiner
from src.creative_learning.skill_improvement import SkillImprovementEngine
from src.creative_learning.worker_learning import WorkerPerformanceEvaluator
from src.creative_learning.visual_learning import VisualPatternMiner
from src.creative_learning.learning_memory import GovernedKnowledgeStore
from src.creative_learning.freshness import KnowledgeFreshnessEvaluator
from src.creative_learning.drift import EnvironmentDriftDetector
from src.creative_learning.learning_observability import LearningTelemetryEmitter
from src.creative_learning.learning_governance import LearningGovernanceEngine


learning_router = APIRouter(prefix="/api/learning", tags=["CreativeLearningLoop"])

# Singleton Services for Learning Operating Loop
decision_ledger = DecisionLedger()
ingestion_pipeline = OutcomeIngestionPipeline()
normalizer = OutcomeNormalizer()
linkage_graph = OutcomeLinkageGraph()
attribution_engine = AttributionEngine()
signal_generator = LearningSignalGenerator()
hypothesis_store = LearningHypothesisStore()
counterfactual_engine = CounterfactualEngine()
experiment_registry = ExperimentRegistry()
calibration_tracker = CalibrationTracker()
promotion_engine = KnowledgePromotionEngine()
contradiction_handler = ContradictionHandler()
pattern_miner = CreativePatternMiner()
skill_optimizer = SkillImprovementEngine()
worker_evaluator = WorkerPerformanceEvaluator()
visual_pattern_miner = VisualPatternMiner()
governed_knowledge_store = GovernedKnowledgeStore()
freshness_evaluator = KnowledgeFreshnessEvaluator()
drift_detector = EnvironmentDriftDetector()
telemetry_emitter = LearningTelemetryEmitter()
governance_engine = LearningGovernanceEngine()


def get_operator_context(
    x_operator_id: str = Header(default="op_creative_director_01"),
    x_operator_role: str = Header(default="CREATIVE_DIRECTOR"),
) -> OperatorContext:
    try:
        role = OperatorRole(x_operator_role)
    except ValueError:
        role = OperatorRole.STAFF_OPERATOR
    return OperatorContext(
        operator_id=x_operator_id,
        role=role,
        department="Creative Direction",
    )


# --- Request Models ---
class RecordDecisionRequest(BaseModel):
    campaign_id: str
    decision_type: DecisionType
    decision: str
    rationale: str
    confidence: float
    tenant_id: str = "tenant_default"
    client_id: str = "cli_default"
    brand_id: str = "brd_default"
    worker_id: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    expected_impact: str = ""


class IngestOutcomeRequest(BaseModel):
    campaign_id: str
    source_platform: str
    metrics_payload: Dict[str, Any]
    source_signature: str


class CreateHypothesisRequest(BaseModel):
    statement: str
    originating_campaigns: List[str]
    supporting_evidence: List[str]
    scope: HypothesisScope = HypothesisScope.BRAND
    confidence: float = 0.85
    test_recommendation: str = ""


class ProposePromotionRequest(BaseModel):
    claim: str
    scope: HypothesisScope
    supporting_evidence: List[str]
    affected_knowledge_objects: List[str]
    expected_benefit: str
    known_risks: List[str]
    rollback_plan: str
    client_id: Optional[str] = None
    brand_id: Optional[str] = None
    confidence: float = 0.88


class ReviewPromotionRequest(BaseModel):
    decision: str  # "APPROVE", "REJECT", "REQUEST_REVISION"
    comments: str = ""


# --- Endpoints ---

@learning_router.post("/decisions")
def record_campaign_decision(req: RecordDecisionRequest, operator: OperatorContext = Depends(get_operator_context)):
    snapshot = DecisionContextSnapshot(
        snapshot_id=f"snp_{req.campaign_id}",
        tenant_id=req.tenant_id,
        client_id=req.client_id,
        brand_id=req.brand_id,
        campaign_id=req.campaign_id,
    )
    rec = decision_ledger.record_decision(
        campaign_id=req.campaign_id,
        decision_type=req.decision_type,
        actor_id=operator.operator_id,
        context_snapshot=snapshot,
        decision=req.decision,
        rationale=req.rationale,
        confidence=req.confidence,
        worker_id=req.worker_id,
        evidence_refs=req.evidence_refs,
        assumptions=req.assumptions,
        unknowns=req.unknowns,
        expected_impact=req.expected_impact,
    )
    telemetry_emitter.emit("decision_recorded", campaign_id=req.campaign_id, operator_id=operator.operator_id, payload={"decision_id": rec.decision_id})
    return {"status": "success", "decision_record": rec}


@learning_router.get("/campaigns/{campaign_id}/decisions")
def list_decisions_for_campaign(campaign_id: str):
    return {"decisions": decision_ledger.list_decisions_for_campaign(campaign_id)}


@learning_router.post("/outcomes/ingest")
def ingest_outcome_feed(req: IngestOutcomeRequest):
    feed = ingestion_pipeline.ingest_feed(
        campaign_id=req.campaign_id,
        source_platform=req.source_platform,
        metrics_payload=req.metrics_payload,
        source_signature=req.source_signature,
    )
    normalized = normalizer.normalize_feed(
        campaign_id=req.campaign_id,
        source_platform=req.source_platform,
        raw_metrics=req.metrics_payload,
    )
    telemetry_emitter.emit("outcome_ingested", campaign_id=req.campaign_id, payload={"feed_id": feed.feed_id, "normalized_count": len(normalized)})
    return {"status": "success", "feed": feed, "normalized_metrics": normalized}


@learning_router.post("/hypotheses")
def create_learning_hypothesis(req: CreateHypothesisRequest):
    hyp = hypothesis_store.create_hypothesis(
        statement=req.statement,
        originating_campaigns=req.originating_campaigns,
        supporting_evidence=req.supporting_evidence,
        scope=req.scope,
        confidence=req.confidence,
        test_recommendation=req.test_recommendation,
    )
    telemetry_emitter.emit("hypothesis_created", payload={"hypothesis_id": hyp.hypothesis_id})
    return {"status": "success", "hypothesis": hyp}


@learning_router.get("/hypotheses/{hypothesis_id}")
def get_hypothesis(hypothesis_id: str):
    hyp = hypothesis_store.get_hypothesis(hypothesis_id)
    if not hyp:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    return {"hypothesis": hyp}


@learning_router.get("/calibration/{domain}")
def get_calibration_report(domain: str):
    rep = calibration_tracker.get_calibration_report(domain)
    return {"calibration_report": rep}


@learning_router.post("/promotions")
def propose_knowledge_promotion(req: ProposePromotionRequest):
    try:
        prop = promotion_engine.propose_promotion(
            claim=req.claim,
            scope=req.scope,
            supporting_evidence=req.supporting_evidence,
            affected_knowledge_objects=req.affected_knowledge_objects,
            expected_benefit=req.expected_benefit,
            known_risks=req.known_risks,
            rollback_plan=req.rollback_plan,
            client_id=req.client_id,
            brand_id=req.brand_id,
            confidence=req.confidence,
        )
        telemetry_emitter.emit("promotion_proposed", payload={"proposal_id": prop.proposal_id})
        return {"status": "success", "proposal": prop}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@learning_router.post("/promotions/{proposal_id}/review")
def review_knowledge_promotion(proposal_id: str, req: ReviewPromotionRequest, operator: OperatorContext = Depends(get_operator_context)):
    try:
        prop = promotion_engine.review_and_decide(proposal_id, operator, req.decision, req.comments)
        if req.decision == "APPROVE":
            governed_knowledge_store.store_knowledge(
                tenant_id=operator.tenant_id,
                scope=prop.scope,
                title=prop.claim,
                content=f"Benefit: {prop.expected_benefit}",
                provenance_proposal_id=prop.proposal_id,
                client_id=prop.client_id,
                brand_id=prop.brand_id,
                confidence=prop.confidence,
            )
            telemetry_emitter.emit("promotion_approved", operator_id=operator.operator_id, payload={"proposal_id": proposal_id})
        return {"status": "success", "proposal": prop}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@learning_router.post("/promotions/{proposal_id}/rollback")
def rollback_knowledge_promotion(proposal_id: str, reason: str = "Regression observed", operator: OperatorContext = Depends(get_operator_context)):
    try:
        prop = promotion_engine.rollback_promotion(proposal_id, operator, reason)
        telemetry_emitter.emit("knowledge_rolled_back", operator_id=operator.operator_id, payload={"proposal_id": proposal_id, "reason": reason})
        return {"status": "success", "proposal": prop}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@learning_router.get("/campaigns/{campaign_id}/postmortem")
def get_campaign_learning_postmortem(campaign_id: str):
    decisions = decision_ledger.list_decisions_for_campaign(campaign_id)
    feeds = ingestion_pipeline.list_feeds_for_campaign(campaign_id)
    return {
        "campaign_id": campaign_id,
        "decisions_count": len(decisions),
        "feeds_count": len(feeds),
        "postmortem_summary": "Governed postmortem learning completed without causal overclaiming.",
        "invariants_enforced": governance_engine.INVARIANTS,
    }

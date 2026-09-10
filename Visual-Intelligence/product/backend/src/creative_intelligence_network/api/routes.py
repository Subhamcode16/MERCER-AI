"""
REST API Routes for Phase 29: ILYREN Creative Intelligence Network.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..graph.intelligence_graph import OrganizationalIntelligenceGraph
from ..signals.signal_engine import StrategicSignalEngine
from ..signals.signal_types import SignalClass, EpistemicStatus
from ..hypotheses.hypothesis_engine import HypothesisEngine
from ..hypotheses.hypothesis_types import HypothesisStatus
from ..foresight.foresight_engine import ForesightEngine
from ..recommendations.recommendation_engine import StrategicRecommendationEngine
from ..recommendations.recommendation_models import ReversibilityRating
from ..bridge.campaign_bridge import IntelligenceToCampaignBridge
from ..observability.observatory import StrategicIntelligenceObservatory
from ..cross_client.abstraction_pipeline import CrossClientAbstractionPipeline, CrossClientAbstractionRequest
from ..external.external_ingest import ExternalIntelligenceIngest
from ..external.trust_model import SourceReliability


router = APIRouter(prefix="/api/v1/intelligence", tags=["Creative Intelligence Network"])

# Global Service Instances
_graph = OrganizationalIntelligenceGraph()
_signals = StrategicSignalEngine(graph=_graph)
_hypotheses = HypothesisEngine(graph=_graph)
_foresight = ForesightEngine(graph=_graph)
_recommendations = StrategicRecommendationEngine(graph=_graph)
_bridge = IntelligenceToCampaignBridge(graph=_graph)
_observatory = StrategicIntelligenceObservatory(_graph, _signals, _hypotheses, _recommendations)
_cross_client = CrossClientAbstractionPipeline(graph=_graph)
_external = ExternalIntelligenceIngest(graph=_graph)


class SignalQueryRequest(BaseModel):
    tenant_id: str
    signal_class: Optional[SignalClass] = None


class EmitSignalRequest(BaseModel):
    tenant_id: str
    signal_class: SignalClass
    scope: str
    observed_pattern: str
    method: str
    confidence: float
    epistemic_status: EpistemicStatus
    supporting_evidence: Optional[List[str]] = None


class ProposeHypothesisRequest(BaseModel):
    tenant_id: str
    statement: str
    scope: str
    falsification_criteria: str
    origin_signals: Optional[List[str]] = None


class GenerateForesightRequest(BaseModel):
    tenant_id: str
    scope: str
    topic: str
    initiating_signals: List[str]
    base_assumptions: List[str]


class GenerateRecommendationRequest(BaseModel):
    tenant_id: str
    title: str
    action_statement: str
    why_now: str
    scope: str
    epistemic_status: EpistemicStatus
    initial_confidence: float
    supporting_evidence: List[str]
    reversibility: ReversibilityRating = ReversibilityRating.MODERATELY_REVERSIBLE


class ChallengeRecommendationRequest(BaseModel):
    tenant_id: str
    operator_notes: str
    new_counterevidence: Optional[List[str]] = None


class RecordDecisionRequest(BaseModel):
    tenant_id: str
    decision_maker: str
    decision_maker_role: str
    recommendation_id: str
    operator_rationale: str
    is_experiment: bool = False


# Endpoints

@router.post("/signals/query")
async def query_signals(req: SignalQueryRequest):
    return _signals.list_signals(req.tenant_id, req.signal_class)


@router.post("/signals/emit")
async def emit_signal(req: EmitSignalRequest):
    sig = _signals.emit_signal(
        tenant_id=req.tenant_id,
        signal_class=req.signal_class,
        scope=req.scope,
        observed_pattern=req.observed_pattern,
        method=req.method,
        confidence=req.confidence,
        epistemic_status=req.epistemic_status,
        supporting_evidence=req.supporting_evidence,
    )
    return sig


@router.get("/signals/{signal_id}")
async def get_signal(signal_id: str, tenant_id: str):
    sig = _signals.get_signal(signal_id, tenant_id=tenant_id)
    if not sig:
        raise HTTPException(status_code=404, detail="Signal not found or access denied")
    return sig


@router.post("/hypotheses")
async def propose_hypothesis(req: ProposeHypothesisRequest):
    hypo = _hypotheses.propose_hypothesis(
        tenant_id=req.tenant_id,
        statement=req.statement,
        scope=req.scope,
        falsification_criteria=req.falsification_criteria,
        origin_signals=req.origin_signals,
    )
    return hypo


@router.get("/hypotheses/{hypothesis_id}")
async def get_hypothesis(hypothesis_id: str, tenant_id: str):
    hypo = _hypotheses.get_hypothesis(hypothesis_id, tenant_id=tenant_id)
    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found or access denied")
    return hypo


@router.post("/foresight")
async def generate_foresight(req: GenerateForesightRequest):
    matrix = _foresight.construct_scenario_matrix(
        tenant_id=req.tenant_id,
        scope=req.scope,
        topic=req.topic,
        initiating_signals=req.initiating_signals,
        base_assumptions=req.base_assumptions,
    )
    return matrix


@router.post("/recommendations")
async def generate_recommendation(req: GenerateRecommendationRequest):
    rec = _recommendations.generate_recommendation(
        tenant_id=req.tenant_id,
        title=req.title,
        action_statement=req.action_statement,
        why_now=req.why_now,
        scope=req.scope,
        epistemic_status=req.epistemic_status,
        initial_confidence=req.initial_confidence,
        supporting_evidence=req.supporting_evidence,
        reversibility=req.reversibility,
    )
    return rec


@router.post("/recommendations/{recommendation_id}/challenge")
async def challenge_recommendation(recommendation_id: str, req: ChallengeRecommendationRequest):
    rec = _recommendations.challenge_recommendation(
        recommendation_id=recommendation_id,
        operator_notes=req.operator_notes,
        new_counterevidence=req.new_counterevidence,
        tenant_id=req.tenant_id,
    )
    return rec


@router.post("/decisions")
async def record_decision(req: RecordDecisionRequest):
    rec = _recommendations.get_recommendation(req.recommendation_id, tenant_id=req.tenant_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    try:
        dec = _bridge.record_human_decision_and_create_campaign(
            tenant_id=req.tenant_id,
            decision_maker=req.decision_maker,
            decision_maker_role=req.decision_maker_role,
            recommendation=rec,
            operator_rationale=req.operator_rationale,
            is_experiment=req.is_experiment,
        )
        return dec
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("/observatory")
async def get_observatory(tenant_id: str):
    return _observatory.get_observatory_snapshot(tenant_id)

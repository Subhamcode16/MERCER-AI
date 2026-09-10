"""
FastAPI Routes for Phase 30 Institutional Intelligence.
Distinguishes between read, derive, propose, approve, and execute operations.
"""
from fastapi import APIRouter, HTTPException, Depends, Header, status
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

from ..types import StrategicHorizon, WorkerRole, ThreatID, GovernanceInvariantViolation
from ..objectives.models import StrategicObjective
from ..horizons.models import StrategicHorizonMapping, HorizonPortfolioView
from ..decisions.models import StrategicDecision, HumanDecisionCapture
from ..portfolio.service import DecisionPortfolioService, DecisionAttentionScore
from ..initiatives.models import StrategicInitiative
from ..commitments.models import StrategicCommitment
from ..assumptions.monitor import StrategicAssumption, AssumptionMonitor
from ..memory.store import MemoryItem, OrganizationalMemoryStore
from ..prioritization.queue import AttentionQueueItem, IntelligenceAttentionQueue
from ..cadence.engine import StrategicCadenceEngine, CadenceExecutionRecord
from ..operating_rooms.room import StrategicOperatingRoom, OperatingRoomParticipant
from ..drift.detector import StrategicDriftDetector, DriftSignal
from ..health.evaluator import InitiativeHealthEvaluator, InitiativeHealthReport
from ..review.engine import StrategicReviewEngine, StrategicBrief
from ..preparation.preparer import AutonomousPreparationEngine
from ..bridge.bridges import StrategicExecutionBridge, CampaignProposalFromStrategy
from ..workers.registry import WorkerRegistry
from ..external.defense import ExternalIntelligenceDefense, IngestedSignal
from ..cross_client.isolation import MultiTenantIsolationBoundary
from ..governance.gate import GovernancePolicyGate
from ..authorization.boundary import HumanDecisionBoundaryService
from ..observability.telemetry import StrategicTelemetryEngine, StrategicAuditEvent
from ..rollback.manager import StrategicRollbackManager

router = APIRouter(prefix="/institutional-intelligence", tags=["Institutional Intelligence (Phase 30)"])

# In-memory tenant instances
_objectives_db: Dict[str, StrategicObjective] = {}
_initiatives_db: Dict[str, StrategicInitiative] = {}
_rooms_db: Dict[str, StrategicOperatingRoom] = {}
_memory_stores: Dict[str, OrganizationalMemoryStore] = {}
_portfolio_services: Dict[str, DecisionPortfolioService] = {}
_assumption_monitors: Dict[str, AssumptionMonitor] = {}
_attention_queues: Dict[str, IntelligenceAttentionQueue] = {}
_cadence_engines: Dict[str, StrategicCadenceEngine] = {}
_drift_detectors: Dict[str, StrategicDriftDetector] = {}
_health_evaluators: Dict[str, InitiativeHealthEvaluator] = {}
_review_engines: Dict[str, StrategicReviewEngine] = {}
_bridges: Dict[str, StrategicExecutionBridge] = {}
_auth_services: Dict[str, HumanDecisionBoundaryService] = {}
_telemetry_engines: Dict[str, StrategicTelemetryEngine] = {}
_rollback_managers: Dict[str, StrategicRollbackManager] = {}
_worker_registries: Dict[str, WorkerRegistry] = {}


def get_tenant_id(x_tenant_id: Optional[str] = Header("default_tenant")) -> str:
    return x_tenant_id or "default_tenant"


def get_services(tenant_id: str):
    if tenant_id not in _memory_stores:
        _memory_stores[tenant_id] = OrganizationalMemoryStore(tenant_id)
        _portfolio_services[tenant_id] = DecisionPortfolioService(tenant_id)
        _assumption_monitors[tenant_id] = AssumptionMonitor(tenant_id)
        _attention_queues[tenant_id] = IntelligenceAttentionQueue(tenant_id)
        _cadence_engines[tenant_id] = StrategicCadenceEngine(tenant_id)
        _drift_detectors[tenant_id] = StrategicDriftDetector(tenant_id)
        _health_evaluators[tenant_id] = InitiativeHealthEvaluator(tenant_id)
        _review_engines[tenant_id] = StrategicReviewEngine(tenant_id)
        _bridges[tenant_id] = StrategicExecutionBridge(tenant_id)
        _auth_services[tenant_id] = HumanDecisionBoundaryService(tenant_id)
        _telemetry_engines[tenant_id] = StrategicTelemetryEngine(tenant_id)
        _rollback_managers[tenant_id] = StrategicRollbackManager(tenant_id)
        _worker_registries[tenant_id] = WorkerRegistry(tenant_id)

    return {
        "memory": _memory_stores[tenant_id],
        "portfolio": _portfolio_services[tenant_id],
        "assumptions": _assumption_monitors[tenant_id],
        "queue": _attention_queues[tenant_id],
        "cadence": _cadence_engines[tenant_id],
        "drift": _drift_detectors[tenant_id],
        "health": _health_evaluators[tenant_id],
        "review": _review_engines[tenant_id],
        "bridge": _bridges[tenant_id],
        "auth": _auth_services[tenant_id],
        "telemetry": _telemetry_engines[tenant_id],
        "rollback": _rollback_managers[tenant_id],
        "workers": _worker_registries[tenant_id]
    }


# Objectives
@router.post("/objectives/propose", response_model=StrategicObjective)
def propose_objective(obj: StrategicObjective, tenant_id: str = Depends(get_tenant_id)):
    obj.tenant_id = tenant_id
    obj.validate_human_authority(obj.owner, is_automated_agent=False)
    _objectives_db[obj.objective_id] = obj
    return obj


@router.get("/objectives", response_model=List[StrategicObjective])
def list_objectives(tenant_id: str = Depends(get_tenant_id)):
    return [o for o in _objectives_db.values() if o.tenant_id == tenant_id]


# Decisions & Portfolio
@router.post("/decisions/propose", response_model=StrategicDecision)
def propose_decision(decision: StrategicDecision, tenant_id: str = Depends(get_tenant_id)):
    decision.tenant_id = tenant_id
    svc = get_services(tenant_id)["portfolio"]
    decision.calculate_record_hash()
    svc.add_decision(decision)
    return decision


@router.post("/decisions/{decision_id}/approve", response_model=StrategicDecision)
def approve_decision(decision_id: str, capture: HumanDecisionCapture, tenant_id: str = Depends(get_tenant_id)):
    svc = get_services(tenant_id)["portfolio"]
    decision = svc.get_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    decision.record_human_decision(capture, actor=capture.decision_maker)
    return decision


@router.get("/decision-portfolio/prioritized", response_model=List[DecisionAttentionScore])
def get_prioritized_portfolio(tenant_id: str = Depends(get_tenant_id)):
    svc = get_services(tenant_id)["portfolio"]
    return svc.rank_attention_queue()


# Assumptions
@router.post("/assumptions/propose", response_model=StrategicAssumption)
def register_assumption(assumption: StrategicAssumption, tenant_id: str = Depends(get_tenant_id)):
    assumption.tenant_id = tenant_id
    svc = get_services(tenant_id)["assumptions"]
    svc.register_assumption(assumption, actor_role="STRATEGY_WORKER")
    return assumption


@router.get("/assumptions/scan", response_model=Dict[str, List[StrategicAssumption]])
def scan_assumptions(tenant_id: str = Depends(get_tenant_id)):
    svc = get_services(tenant_id)["assumptions"]
    return svc.scan_for_staleness_and_contradictions()


# Memory
@router.post("/memory/append", response_model=MemoryItem)
def append_memory(item: MemoryItem, tenant_id: str = Depends(get_tenant_id)):
    item.tenant_id = tenant_id
    svc = get_services(tenant_id)["memory"]
    return svc.append_memory(item)


# Reviews & Briefs
@router.post("/reviews/derive", response_model=StrategicBrief)
def generate_strategic_review(
    title: str,
    changes: List[str],
    recommendation: str,
    tenant_id: str = Depends(get_tenant_id)
):
    svc = get_services(tenant_id)["review"]
    return svc.generate_review(
        title=title,
        changes=changes,
        material_points=["Focus on core product brand equity"],
        uncertainties=["Q4 supply chain shifts"],
        contradictions=[],
        attention_decisions=[],
        initiative_updates=[],
        opportunities=["Expand digital showroom"],
        risks=["Competitor pricing pressure"],
        expired_assumptions=[],
        scenarios=["Macro expansion scenario"],
        human_actions=["Approve showroom initiative"],
        unknowns=["Impact of new regional import tax"],
        evidence_provenance=["doc_market_2026_q3"],
        recommendation=recommendation
    )


# Bridge Execution
@router.post("/bridges/propose-campaign", response_model=CampaignProposalFromStrategy)
def propose_campaign(initiative_id: str, decision_id: str, title: str, scope: str, tenant_id: str = Depends(get_tenant_id)):
    bridge = get_services(tenant_id)["bridge"]
    return bridge.create_campaign_proposal(initiative_id, decision_id, title, scope)


@router.post("/bridges/{proposal_id}/approve", response_model=CampaignProposalFromStrategy)
def approve_campaign_proposal(proposal_id: str, approver: str, token: str, tenant_id: str = Depends(get_tenant_id)):
    bridge = get_services(tenant_id)["bridge"]
    return bridge.approve_proposal_by_human(proposal_id, approver, token)


@router.post("/bridges/{proposal_id}/execute")
def execute_campaign_through_gateway(proposal_id: str, caller_agent: str = "CAMPAIGN_WORKER", tenant_id: str = Depends(get_tenant_id)):
    bridge = get_services(tenant_id)["bridge"]
    try:
        return bridge.execute_campaign(proposal_id, caller_agent)
    except GovernanceInvariantViolation as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

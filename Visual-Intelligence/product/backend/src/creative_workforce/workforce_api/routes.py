"""
Phase 26 Workforce API Gateway Handlers.
"""
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, Header, Query
from pydantic import BaseModel, Field

from src.control_plane.context import OperatorContext
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus
from src.creative_workforce.worker_registry.registry import WorkerRegistry
from src.creative_workforce.worker_lifecycle.lifecycle_engine import WorkerLifecycleManager
from src.creative_workforce.skill_registry.models import SkillDefinition, SkillRiskClass, SkillStatus
from src.creative_workforce.skill_registry.registry import SkillRegistry
from src.creative_workforce.campaign_rooms.room_manager import CampaignRoomManager, CampaignRoom
from src.creative_workforce.handoffs.handoff_service import HandoffService
from src.creative_workforce.routines.routine_engine import RoutineEngine, WorkforceRoutine, RoutineTriggerType
from src.creative_workforce.workforce_activity.activity_stream import WorkforceActivityLogger, WorkforceEventType


router = APIRouter(prefix="/workforce", tags=["creative_workforce"])


# Pydantic Request Models
class CreateWorkerRequest(BaseModel):
    worker_id: str
    name: str
    role_id: str
    description: str
    tenant_id: str = "tenant_alpha"
    organization_id: str = "org_default"


class UpdateWorkerStatusRequest(BaseModel):
    status: WorkerStatus
    reason: str = ""


class CreateSkillRequest(BaseModel):
    skill_id: str
    version: str
    purpose: str
    required_capabilities: List[str] = []
    risk_class: SkillRiskClass = SkillRiskClass.LOW


class CreateCampaignRoomRequest(BaseModel):
    name: str
    campaign_id: str
    client_id: str
    tenant_id: str = "tenant_alpha"
    participants: Dict[str, str] = {}


class CreateHandoffRequest(BaseModel):
    room_id: str
    sender_worker_id: str
    recipient_worker_id: str
    purpose: str
    requested_action: str = ""
    input_artifacts: List[Dict[str, Any]] = []


class CreateRoutineRequest(BaseModel):
    routine_id: str
    name: str
    worker_id: str
    skill_id: str
    tenant_id: str = "tenant_alpha"
    client_id: str = "client_haute"
    trigger_type: RoutineTriggerType = RoutineTriggerType.MANUAL


class RunRoutineRequest(BaseModel):
    worker_id: str
    execution_nonce: str
    input_context: Dict[str, Any] = {}


# Core Service Container
class WorkforceAPIServices:
    def __init__(
        self,
        worker_registry: WorkerRegistry,
        skill_registry: SkillRegistry,
        room_manager: CampaignRoomManager,
        handoff_service: HandoffService,
        routine_engine: RoutineEngine,
        activity_logger: WorkforceActivityLogger,
    ):
        self.worker_registry = worker_registry
        self.skill_registry = skill_registry
        self.room_manager = room_manager
        self.handoff_service = handoff_service
        self.routine_engine = routine_engine
        self.activity_logger = activity_logger


_SERVICES: Optional[WorkforceAPIServices] = None


def set_workforce_api_services(services: WorkforceAPIServices):
    global _SERVICES
    _SERVICES = services


def get_workforce_api_services() -> WorkforceAPIServices:
    if not _SERVICES:
        raise RuntimeError("WorkforceAPIServices have not been initialized")
    return _SERVICES


@router.post("/workers")
async def create_worker(req: CreateWorkerRequest):
    svc = get_workforce_api_services()
    worker = WorkerIdentity(
        worker_id=req.worker_id,
        tenant_id=req.tenant_id,
        organization_id=req.organization_id,
        name=req.name,
        role_id=req.role_id,
        description=req.description,
        status=WorkerStatus.ACTIVE,
    )
    svc.worker_registry.register_worker(worker)
    return {"status": "SUCCESS", "worker": worker}


@router.get("/workers")
async def list_workers(tenant_id: str = "tenant_alpha"):
    svc = get_workforce_api_services()
    workers = svc.worker_registry.list_workers(tenant_id=tenant_id)
    return {"workers": workers, "count": len(workers)}


@router.get("/workers/{worker_id}")
async def get_worker(worker_id: str, tenant_id: str = "tenant_alpha"):
    svc = get_workforce_api_services()
    worker = svc.worker_registry.get_worker(worker_id, tenant_id=tenant_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker '{worker_id}' not found")
    return {"worker": worker}


@router.patch("/workers/{worker_id}/status")
async def update_worker_status(worker_id: str, req: UpdateWorkerStatusRequest, tenant_id: str = "tenant_alpha"):
    svc = get_workforce_api_services()
    worker = svc.worker_registry.get_worker(worker_id, tenant_id=tenant_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker '{worker_id}' not found")
    
    updated = WorkerLifecycleManager.transition(worker, req.status, reason=req.reason)
    svc.worker_registry.update_worker(updated)
    return {"status": "SUCCESS", "worker": updated}


@router.post("/skills")
async def create_skill(req: CreateSkillRequest):
    svc = get_workforce_api_services()
    skill = SkillDefinition(
        skill_id=req.skill_id,
        version=req.version,
        purpose=req.purpose,
        required_capabilities=req.required_capabilities,
        risk_class=req.risk_class,
    )
    svc.skill_registry.register_skill(skill)
    return {"status": "SUCCESS", "skill": skill}


@router.get("/skills")
async def list_skills():
    svc = get_workforce_api_services()
    skills = svc.skill_registry.list_skills()
    return {"skills": skills, "count": len(skills)}


@router.post("/campaign-rooms")
async def create_campaign_room(req: CreateCampaignRoomRequest):
    svc = get_workforce_api_services()
    room = svc.room_manager.create_room(
        tenant_id=req.tenant_id,
        client_id=req.client_id,
        campaign_id=req.campaign_id,
        name=req.name,
        initial_participants=req.participants,
    )
    return {"status": "SUCCESS", "room": room}


@router.get("/campaign-rooms/{room_id}")
async def get_campaign_room(room_id: str, tenant_id: str = "tenant_alpha"):
    svc = get_workforce_api_services()
    room = svc.room_manager.get_room(room_id, tenant_id=tenant_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Campaign room '{room_id}' not found")
    return {"room": room}


@router.post("/campaign-rooms/{room_id}/handoffs")
async def create_room_handoff(room_id: str, req: CreateHandoffRequest, tenant_id: str = "tenant_alpha", client_id: str = "client_haute"):
    svc = get_workforce_api_services()
    handoff = svc.handoff_service.create_handoff(
        room_id=room_id,
        tenant_id=tenant_id,
        client_id=client_id,
        sender_worker_id=req.sender_worker_id,
        recipient_worker_id=req.recipient_worker_id,
        purpose=req.purpose,
        input_artifacts=req.input_artifacts,
        requested_action=req.requested_action,
    )
    return {"status": "SUCCESS", "handoff": handoff}


@router.post("/routines")
async def create_routine(req: CreateRoutineRequest):
    svc = get_workforce_api_services()
    routine = WorkforceRoutine(
        routine_id=req.routine_id,
        tenant_id=req.tenant_id,
        client_id=req.client_id,
        name=req.name,
        worker_id=req.worker_id,
        skill_id=req.skill_id,
        trigger_type=req.trigger_type,
    )
    svc.routine_engine.register_routine(routine)
    return {"status": "SUCCESS", "routine": routine}


@router.post("/routines/{routine_id}/run")
async def run_routine(routine_id: str, req: RunRoutineRequest, tenant_id: str = "tenant_alpha"):
    svc = get_workforce_api_services()
    worker = svc.worker_registry.get_worker(req.worker_id, tenant_id=tenant_id)
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker '{req.worker_id}' not found")
    
    outcome = svc.routine_engine.trigger_routine(
        routine_id=routine_id,
        worker=worker,
        execution_nonce=req.execution_nonce,
        input_context=req.input_context,
    )
    return {"status": "SUCCESS", "outcome": outcome}


@router.get("/activity")
async def get_workforce_activity(tenant_id: str = "tenant_alpha", client_id: Optional[str] = None):
    svc = get_workforce_api_services()
    events = svc.activity_logger.query_events(tenant_id=tenant_id, client_id=client_id)
    return {"events": events, "count": len(events)}


@router.get("/health")
async def get_workforce_health():
    return {
        "status": "HEALTHY",
        "workforce_layer": "READY",
        "governance_mode": "FAIL_CLOSED",
    }

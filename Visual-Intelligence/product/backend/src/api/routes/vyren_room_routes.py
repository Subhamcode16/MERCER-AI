"""
FastAPI Routes for VYREN Room & Agentic Orchestration.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.vyren_room.room_service import RoomService
from src.orchestrator.vyren_orchestrator import VyrenOrchestrator
from src.agent_runtime.errors.exceptions import TenantTraversalError, PromptInjectionDetectedError

router = APIRouter(prefix="/api/v1/rooms", tags=["VYREN Room"])

_room_service = RoomService()
_orchestrator = VyrenOrchestrator(room_service=_room_service)


class CreateRoomRequest(BaseModel):
    title: str
    campaign_id: Optional[str] = None


class SendMessageRequest(BaseModel):
    content: str
    user_name: Optional[str] = "Elena Vance"


class RecordDecisionRequest(BaseModel):
    chosen_option_id: str
    decided_by: str = "Elena Vance"


def get_tenant_id(x_tenant_id: Optional[str] = Header("tenant_default")) -> str:
    return x_tenant_id or "tenant_default"


@router.post("/")
async def create_room(req: CreateRoomRequest, tenant_id: str = Depends(get_tenant_id)):
    """Initialize a collaborative Room."""
    room = _room_service.create_room(tenant_id=tenant_id, title=req.title, campaign_id=req.campaign_id)
    return {"success": True, "room": room.dict()}


@router.get("/{room_id}")
async def get_room(room_id: str, tenant_id: str = Depends(get_tenant_id)):
    """Retrieve full room state, message thread, and active artifacts."""
    try:
        room = _room_service.get_room(room_id=room_id, tenant_id=tenant_id)
        return {"success": True, "room": room.dict()}
    except TenantTraversalError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{room_id}/messages")
async def send_room_message(
    room_id: str,
    req: SendMessageRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """Post message and trigger orchestrator turn."""
    try:
        response_msg = await _orchestrator.process_user_turn(
            room_id=room_id,
            tenant_id=tenant_id,
            user_prompt=req.content,
            user_name=req.user_name
        )
        return {"success": True, "message": response_msg.dict()}
    except PromptInjectionDetectedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TenantTraversalError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{room_id}/decisions/{decision_id}")
async def record_human_decision(
    room_id: str,
    decision_id: str,
    req: RecordDecisionRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """Confirm a human decision gate inside the room."""
    try:
        decision = _room_service.record_decision(
            room_id=room_id,
            tenant_id=tenant_id,
            decision_id=decision_id,
            chosen_option_id=req.chosen_option_id,
            decided_by=req.decided_by
        )
        return {"success": True, "decision": decision.dict()}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TenantTraversalError as e:
        raise HTTPException(status_code=403, detail=str(e))

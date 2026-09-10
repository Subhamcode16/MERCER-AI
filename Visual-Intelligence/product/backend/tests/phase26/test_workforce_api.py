"""
Phase 26 Unit Tests: Workforce API Gateway Endpoints.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.creative_workforce.worker_registry.registry import WorkerRegistry
from src.creative_workforce.skill_registry.registry import SkillRegistry
from src.creative_workforce.campaign_rooms.room_manager import CampaignRoomManager
from src.creative_workforce.capability_binding.manifest import CapabilityResolver
from src.creative_workforce.handoffs.handoff_service import HandoffService
from src.creative_workforce.routines.routine_engine import RoutineEngine
from src.creative_workforce.workforce_activity.activity_stream import WorkforceActivityLogger
from src.creative_workforce.workforce_api.routes import (
    router,
    WorkforceAPIServices,
    set_workforce_api_services,
)


@pytest.fixture
def client():
    resolver = CapabilityResolver()
    worker_reg = WorkerRegistry()
    skill_reg = SkillRegistry()
    room_mgr = CampaignRoomManager()
    handoff_svc = HandoffService(capability_resolver=resolver)
    routine_eng = RoutineEngine(capability_resolver=resolver)
    act_logger = WorkforceActivityLogger()

    services = WorkforceAPIServices(
        worker_registry=worker_reg,
        skill_registry=skill_reg,
        room_manager=room_mgr,
        handoff_service=handoff_svc,
        routine_engine=routine_eng,
        activity_logger=act_logger,
    )
    set_workforce_api_services(services)

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_api_worker_endpoints(client):
    # 1. Create worker
    res = client.post(
        "/workforce/workers",
        json={
            "worker_id": "cd_01",
            "name": "Elena Rostova",
            "role_id": "CREATIVE_DIRECTOR",
            "description": "Lead CD",
            "tenant_id": "tenant_alpha",
            "organization_id": "org_luxury",
        },
    )
    assert res.status_code == 200
    assert res.json()["worker"]["worker_id"] == "cd_01"

    # 2. Get worker
    res = client.get("/workforce/workers/cd_01?tenant_id=tenant_alpha")
    assert res.status_code == 200
    assert res.json()["worker"]["name"] == "Elena Rostova"

    # 3. Update worker status to PAUSED
    res = client.patch(
        "/workforce/workers/cd_01/status?tenant_id=tenant_alpha",
        json={"status": "PAUSED", "reason": "System pause"},
    )
    assert res.status_code == 200
    assert res.json()["worker"]["status"] == "PAUSED"


def test_api_campaign_room_and_skills(client):
    # 1. Create skill
    res = client.post(
        "/workforce/skills",
        json={
            "skill_id": "creative_direction",
            "version": "1.0.0",
            "purpose": "Creative concept development",
            "required_capabilities": ["creative_direction.create"],
        },
    )
    assert res.status_code == 200

    # 2. Create campaign room
    res = client.post(
        "/workforce/campaign-rooms",
        json={
            "name": "Autumn Campaign Room",
            "campaign_id": "C-2026-AUTUMN",
            "client_id": "client_haute",
            "tenant_id": "tenant_alpha",
        },
    )
    assert res.status_code == 200
    room_id = res.json()["room"]["room_id"]

    # 3. Get room
    res = client.get(f"/workforce/campaign-rooms/{room_id}?tenant_id=tenant_alpha")
    assert res.status_code == 200
    assert res.json()["room"]["name"] == "Autumn Campaign Room"


def test_api_health_endpoint(client):
    res = client.get("/workforce/health")
    assert res.status_code == 200
    assert res.json()["status"] == "HEALTHY"

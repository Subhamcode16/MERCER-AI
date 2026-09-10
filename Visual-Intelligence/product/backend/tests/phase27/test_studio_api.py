"""
Tests for Phase 27 Studio API Endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.campaign_studio.studio_api import studio_router

app = FastAPI()
app.include_router(studio_router)
client = TestClient(app)


def test_studio_api_full_flow():
    # 1. Create client
    r_client = client.post("/api/studio/clients", json={
        "client_id": "cli_api_01",
        "name": "Aethelgard Luxury",
        "industry": "Haute Couture",
    })
    assert r_client.status_code == 200
    assert r_client.json()["client"]["client_id"] == "cli_api_01"

    # 2. Create campaign
    r_camp = client.post(
        "/api/studio/campaigns",
        json={
            "campaign_id": "camp_api_01",
            "client_id": "cli_api_01",
            "brand_id": "brd_api_01",
            "title": "Winter Monolith Launch",
        },
        headers={"x-operator-id": "op_cd_01", "x-operator-role": "CREATIVE_DIRECTOR"},
    )
    assert r_camp.status_code == 200
    assert r_camp.json()["campaign"]["status"] == "INTAKE_DISCOVERY"

    # 3. Discovery Intake
    r_disc = client.post("/api/studio/discovery/intake", json={
        "campaign_id": "camp_api_01",
        "raw_inputs": {"season": "Winter 2026"},
    })
    assert r_disc.status_code == 200
    assert len(r_disc.json()["pending_questions"]) >= 1

    # 4. Synthesize Intelligence
    r_intel = client.post("/api/studio/intelligence/synthesize?campaign_id=camp_api_01&brand_name=Aethelgard")
    assert r_intel.status_code == 200
    assert "hypotheses" in r_intel.json()["intelligence"]

    # 5. Generate Directions & Select
    r_dirs = client.post("/api/studio/directions/generate?campaign_id=camp_api_01")
    assert r_dirs.status_code == 200
    dir_id = r_dirs.json()["directions"][0]["direction_id"]

    r_sel = client.post(f"/api/studio/directions/{dir_id}/select?campaign_id=camp_api_01")
    assert r_sel.status_code == 200
    assert r_sel.json()["selected_direction"]["is_selected"] is True

    # 6. Generate Visual Drafts
    r_vis = client.post(f"/api/studio/visuals/generate?campaign_id=camp_api_01&direction_id={dir_id}")
    assert r_vis.status_code == 200
    drafts = r_vis.json()["drafts"]
    assert len(drafts) >= 1
    asset_id = drafts[0]["asset_id"]

    # 7. Review Asset
    r_rev = client.post(f"/api/studio/reviews/{asset_id}?campaign_id=camp_api_01")
    assert r_rev.status_code == 200
    assert r_rev.json()["critique"]["is_passed"] is True

    # 8. Request Approval & Decide
    r_app_req = client.post(
        f"/api/studio/approvals/request?campaign_id=camp_api_01&asset_id={asset_id}",
        headers={"x-operator-id": "op_cd_01", "x-operator-role": "CREATIVE_DIRECTOR"},
    )
    assert r_app_req.status_code == 200
    appr_id = r_app_req.json()["approval_request"]["approval_id"]

    r_app_dec = client.post(
        "/api/studio/approvals/decide",
        json={"approval_id": appr_id, "decision": "APPROVED", "comments": "Production Approved"},
        headers={"x-operator-id": "op_cd_01", "x-operator-role": "CREATIVE_DIRECTOR"},
    )
    assert r_app_dec.status_code == 200
    assert r_app_dec.json()["approval"]["status"] == "APPROVED"

    # 9. Get State Projection
    r_proj = client.get("/api/studio/projections/camp_api_01")
    assert r_proj.status_code == 200
    assert r_proj.json()["projection"]["campaign_id"] == "camp_api_01"

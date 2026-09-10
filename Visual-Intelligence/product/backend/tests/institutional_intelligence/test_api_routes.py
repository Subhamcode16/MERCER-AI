"""
Tests for Institutional Intelligence FastAPI Endpoints (Phase 30).
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.institutional_intelligence.api.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_api_propose_and_list_objectives():
    payload = {
        "tenant_id": "tenant_api_test",
        "owner": "human_ceo",
        "creation_authority": "AUTH_BOARD_SECRET",
        "title": "Global ESG Luxury Dominance",
        "description": "Expand sustainable handloom initiatives globally",
        "scope": "GLOBAL_ESG",
        "time_horizon": "NOW",
        "priority": 10
    }
    resp = client.post("/institutional-intelligence/objectives/propose", json=payload, headers={"x-tenant-id": "tenant_api_test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Global ESG Luxury Dominance"
    assert data["is_human_authorized"] is True

    # List
    list_resp = client.get("/institutional-intelligence/objectives", headers={"x-tenant-id": "tenant_api_test"})
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert len(items) >= 1


def test_api_propose_decision_and_get_portfolio():
    payload = {
        "tenant_id": "tenant_api_test",
        "strategic_objective_id": "obj_api_test_01",
        "decision_question": "Enter US West Coast Market?",
        "owner": "human_vp_strategy",
        "alternatives": [
            {"title": "Open LA Flagship", "description": "Beverly Hills flagship store"},
            {"title": "Wholesale Department Store Partnership", "description": "Partner with Saks/Nordstrom"}
        ],
        "uncertainty": 0.5
    }
    resp = client.post("/institutional-intelligence/decisions/propose", json=payload, headers={"x-tenant-id": "tenant_api_test"})
    assert resp.status_code == 200
    dec = resp.json()
    assert dec["decision_id"] != ""

    # Check prioritized portfolio
    port_resp = client.get("/institutional-intelligence/decision-portfolio/prioritized", headers={"x-tenant-id": "tenant_api_test"})
    assert port_resp.status_code == 200
    scores = port_resp.json()
    assert len(scores) >= 1


def test_api_assumptions_and_scanning():
    payload = {
        "tenant_id": "tenant_api_test",
        "statement": "Raw fabric transit times remain under 10 days.",
        "model_confidence": 0.8,
        "empirical_confidence": 0.75
    }
    resp = client.post("/institutional-intelligence/assumptions/propose", json=payload, headers={"x-tenant-id": "tenant_api_test"})
    assert resp.status_code == 200

    scan_resp = client.get("/institutional-intelligence/assumptions/scan", headers={"x-tenant-id": "tenant_api_test"})
    assert scan_resp.status_code == 200
    res = scan_resp.json()
    assert "active" in res


def test_api_bridge_proposal_approval_and_execution():
    # 1. Propose campaign
    prop_resp = client.post(
        "/institutional-intelligence/bridges/propose-campaign?initiative_id=init_api_01&decision_id=dec_api_01&title=Spring%20Silk&scope=DIGITAL",
        headers={"x-tenant-id": "tenant_api_test"}
    )
    assert prop_resp.status_code == 200
    prop_data = prop_resp.json()
    prop_id = prop_data["proposal_id"]

    # 2. Try executing before human approval (must fail with 403)
    exec_fail = client.post(
        f"/institutional-intelligence/bridges/{prop_id}/execute?caller_agent=agent_bot",
        headers={"x-tenant-id": "tenant_api_test"}
    )
    assert exec_fail.status_code == 403

    # 3. Approve by human
    appr_resp = client.post(
        f"/institutional-intelligence/bridges/{prop_id}/approve?approver=human_lead&token=AUTH_SECURE_TOKEN_2026_VALID",
        headers={"x-tenant-id": "tenant_api_test"}
    )
    assert appr_resp.status_code == 200

    # 4. Execute after human approval
    exec_success = client.post(
        f"/institutional-intelligence/bridges/{prop_id}/execute?caller_agent=agent_bot",
        headers={"x-tenant-id": "tenant_api_test"}
    )
    assert exec_success.status_code == 200
    assert exec_success.json()["status"] == "FORWARDED_TO_EXECUTION_GATEWAY"

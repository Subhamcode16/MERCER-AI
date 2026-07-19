import pytest
from fastapi.testclient import TestClient
from main import app
import os
import json

client = TestClient(app)

def test_analyze_product():
    response = client.post("/api/analyze/product", json={
        "image_url": "mock_url",
        "provider": "gemini"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "product_dna" in data
    assert data["product_dna"]["material"]["value"] == "Silk"

def test_create_campaign():
    response = client.post("/api/campaign/create", json={
        "project_id": "proj_123",
        "product_id": "prod_456",
        "creative_objective": "luxury_editorial",
        "assets_requested": ["hero_image", "product_closeup", "lifestyle"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == "proj_123"
    assert len(data["execution"]["asset_states"]) == 3
    assert data["execution"]["asset_states"][0]["status"] == "pending"
    return data["id"] # return campaign_id for next tests

def test_submit_feedback():
    # 1. First create campaign
    response = client.post("/api/campaign/create", json={
        "project_id": "proj_123",
        "product_id": "prod_456",
        "creative_objective": "luxury_editorial",
        "assets_requested": ["hero_image"]
    })
    campaign_id = response.json()["id"]

    # 2. Submit feedback on the asset
    fb_response = client.post(f"/api/campaign/{campaign_id}/assets/hero_image/feedback", json={
        "category": "Lighting",
        "severity": 4,
        "desired_outcome": "More dramatic shadows"
    })
    
    assert fb_response.status_code == 200
    fb_data = fb_response.json()
    assert fb_data["status"] == "feedback_logged"
    
    # 3. Verify it was written to file
    feedback_file = os.path.join("data", "feedback_log.json")
    assert os.path.exists(feedback_file)
    with open(feedback_file, "r") as f:
        logs = json.load(f)
        assert len(logs) > 0
        latest = logs[-1]
        assert latest["campaign_id"] == campaign_id
        assert latest["asset_type"] == "hero_image"
        assert latest["feedback"]["severity"] == 4

    # 4. Verify campaign state updated to rejected
    camp_response = client.get(f"/api/campaign/{campaign_id}")
    camp_data = camp_response.json()
    hero_asset = next(a for a in camp_data["execution"]["asset_states"] if a["type"] == "hero_image")
    assert hero_asset["status"] == "rejected"

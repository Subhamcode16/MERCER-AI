"""
Tests for Phase 28 Learning API Endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.creative_learning.learning_api import learning_router

app = FastAPI()
app.include_router(learning_router)
client = TestClient(app)


def test_learning_api_endpoints_flow():
    # 1. Record decision
    r_dec = client.post(
        "/api/learning/decisions",
        json={
            "campaign_id": "camp_api_28",
            "decision_type": "VISUAL_DIRECTION",
            "decision": "Selected Monolithic Limestone Setting",
            "rationale": "Amplifies garment architectural silhouette",
            "confidence": 0.94,
        },
        headers={"x-operator-id": "op_cd_01", "x-operator-role": "CREATIVE_DIRECTOR"},
    )
    assert r_dec.status_code == 200
    assert r_dec.json()["status"] == "success"

    # 2. List decisions for campaign
    r_list_dec = client.get("/api/learning/campaigns/camp_api_28/decisions")
    assert r_list_dec.status_code == 200
    assert len(r_list_dec.json()["decisions"]) >= 1

    # 3. Ingest outcome feed
    r_feed = client.post(
        "/api/learning/outcomes/ingest",
        json={
            "campaign_id": "camp_api_28",
            "source_platform": "ShopifyStorefront",
            "metrics_payload": {"impressions": 500000, "clicks": 18000, "conversions": 1400},
            "source_signature": "sig_verified_shop_1122",
        },
    )
    assert r_feed.status_code == 200
    assert len(r_feed.json()["normalized_metrics"]) >= 2

    # 4. Create hypothesis
    r_hyp = client.post(
        "/api/learning/hypotheses",
        json={
            "statement": "Architectural limestone plinth enhances luxury outerwear conversion.",
            "originating_campaigns": ["camp_api_28"],
            "supporting_evidence": ["Observed 7.7% conversion rate on Shopify."],
            "scope": "BRAND",
            "confidence": 0.91,
        },
    )
    assert r_hyp.status_code == 200
    hyp_id = r_hyp.json()["hypothesis"]["hypothesis_id"]

    # 5. Get hypothesis
    r_get_hyp = client.get(f"/api/learning/hypotheses/{hyp_id}")
    assert r_get_hyp.status_code == 200
    assert r_get_hyp.json()["hypothesis"]["confidence"] == 0.91

    # 6. Propose promotion & review
    r_prop = client.post(
        "/api/learning/promotions",
        json={
            "claim": "Architectural limestone plinth preset enhances luxury outerwear conversion.",
            "scope": "BRAND",
            "supporting_evidence": ["Shopify 7.7% CVR"],
            "affected_knowledge_objects": ["Preset:Outerwear_2026"],
            "expected_benefit": "+15% conversion lift",
            "known_risks": ["Cold tone bias"],
            "rollback_plan": "Revert to studio grey",
            "brand_id": "brd_01",
        },
    )
    assert r_prop.status_code == 200
    prop_id = r_prop.json()["proposal"]["proposal_id"]

    r_review = client.post(
        f"/api/learning/promotions/{prop_id}/review",
        json={"decision": "APPROVE", "comments": "Approved for brand dossier"},
        headers={"x-operator-id": "op_cd_01", "x-operator-role": "CREATIVE_DIRECTOR"},
    )
    assert r_review.status_code == 200
    assert r_review.json()["proposal"]["state"] == "PROMOTED"

    # 7. Calibration Report
    r_cal = client.get("/api/learning/calibration/VISUAL_QUALITY")
    assert r_cal.status_code == 200
    assert len(r_cal.json()["calibration_report"]["buckets"]) == 5

    # 8. Postmortem Summary
    r_pm = client.get("/api/learning/campaigns/camp_api_28/postmortem")
    assert r_pm.status_code == 200
    assert r_pm.json()["campaign_id"] == "camp_api_28"

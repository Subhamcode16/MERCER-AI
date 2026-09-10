"""
Unit & Integration Tests for Phase 29 REST API Router & Observability Snapshot.
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.creative_intelligence_network.api.routes import router
from src.creative_intelligence_network.signals.signal_types import SignalClass, EpistemicStatus
from src.creative_intelligence_network.recommendations.recommendation_models import ReversibilityRating

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_api_emit_and_query_signals():
    emit_payload = {
        "tenant_id": "API-TENANT-1",
        "signal_class": SignalClass.EMERGING_PATTERN.value,
        "scope": "GLOBAL",
        "observed_pattern": "Rising preference for dark aesthetic in winter drop",
        "method": "API_INGESTION",
        "confidence": 0.85,
        "epistemic_status": EpistemicStatus.OBSERVATIONAL_CORRELATION.value,
        "supporting_evidence": ["API-EV-01"],
    }
    emit_resp = client.post("/api/v1/intelligence/signals/emit", json=emit_payload)
    assert emit_resp.status_code == 200
    data = emit_resp.json()
    assert data["signal_id"].startswith("SIG-")
    sig_id = data["signal_id"]

    # Query signal by ID
    get_resp = client.get(f"/api/v1/intelligence/signals/{sig_id}?tenant_id=API-TENANT-1")
    assert get_resp.status_code == 200
    assert get_resp.json()["signal_id"] == sig_id

    # List signals for tenant
    list_resp = client.post("/api/v1/intelligence/signals/query", json={"tenant_id": "API-TENANT-1"})
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1


def test_api_propose_hypothesis_and_generate_foresight():
    hypo_payload = {
        "tenant_id": "API-TENANT-1",
        "statement": "Dark aesthetic increases conversion velocity by 11%",
        "scope": "WINTER_DROP",
        "falsification_criteria": "CTR drop below baseline",
        "origin_signals": ["SIG-TEST-01"],
    }
    hypo_resp = client.post("/api/v1/intelligence/hypotheses", json=hypo_payload)
    assert hypo_resp.status_code == 200
    hypo_data = hypo_resp.json()
    assert hypo_data["hypothesis_id"].startswith("HYP-")

    foresight_payload = {
        "tenant_id": "API-TENANT-1",
        "scope": "WINTER_DROP",
        "topic": "Dark Aesthetic Direction",
        "initiating_signals": ["SIG-TEST-01"],
        "base_assumptions": ["Customer cohort is active"],
    }
    foresight_resp = client.post("/api/v1/intelligence/foresight", json=foresight_payload)
    assert foresight_resp.status_code == 200
    matrix = foresight_resp.json()
    assert "BASELINE" in matrix
    assert "UNKNOWN" in matrix


def test_api_recommendation_lifecycle_and_decision():
    rec_payload = {
        "tenant_id": "API-TENANT-1",
        "title": "Adopt Dark Aesthetic in Winter Drop",
        "action_statement": "Switch hero banner palette to dark charcoal and deep indigo",
        "why_now": "Engagement velocity higher by 18%",
        "scope": "HERO_BANNER",
        "epistemic_status": EpistemicStatus.EXPERIMENTAL_EVIDENCE.value,
        "initial_confidence": 0.88,
        "supporting_evidence": ["EXP-API-01"],
        "reversibility": ReversibilityRating.MODERATELY_REVERSIBLE.value,
    }
    rec_resp = client.post("/api/v1/intelligence/recommendations", json=rec_payload)
    assert rec_resp.status_code == 200
    rec_data = rec_resp.json()
    rec_id = rec_data["recommendation_id"]

    # Challenge recommendation
    challenge_payload = {
        "tenant_id": "API-TENANT-1",
        "operator_notes": "Ensure accessibility contrast ratios pass WCAG AA standards",
        "new_counterevidence": ["WCAG-COMPLIANCE-REPORT"],
    }
    challenge_resp = client.post(f"/api/v1/intelligence/recommendations/{rec_id}/challenge", json=challenge_payload)
    assert challenge_resp.status_code == 200
    assert challenge_resp.json()["status"] == "DOWNGRADED"

    # Human Decision Execution
    decision_payload = {
        "tenant_id": "API-TENANT-1",
        "decision_maker": "marcus_lead",
        "decision_maker_role": "CAMPAIGN_DIRECTOR",
        "recommendation_id": rec_id,
        "operator_rationale": "Approved after ensuring WCAG contrast compliance",
        "is_experiment": True,
    }
    decision_resp = client.post("/api/v1/intelligence/decisions", json=decision_payload)
    assert decision_resp.status_code == 200
    assert decision_resp.json()["resulting_experiment_id"] is not None


def test_api_observatory_snapshot():
    obs_resp = client.get("/api/v1/intelligence/observatory?tenant_id=API-TENANT-1")
    assert obs_resp.status_code == 200
    data = obs_resp.json()
    assert "metrics" in data
    assert data["metrics"]["active_signals_count"] >= 1

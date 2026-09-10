"""
Unit tests for StudioIntelligenceDashboard projections and secret-stripping.
"""

import pytest
from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.outcome_store import OutcomeStore
from src.studio_intelligence.intelligence_dashboard import StudioIntelligenceDashboard
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


def test_intelligence_dashboard_projection_and_isolation():
    store = OutcomeStore()
    obs = OutcomeObservation(
        observation_id="obs_dash_1",
        client_id="client_nocap",
        campaign_id="camp_1",
        deliverable_id="deliv_1",
        work_item_id="item_1",
        platform="instagram",
        metrics={"impressions": 10000.0, "engagements": 600.0},
        raw_payload={"secret_key": "DO_NOT_EXPOSE"},
    )
    store.store_observation(requesting_client_id="client_nocap", observation=obs)

    dashboard = StudioIntelligenceDashboard(outcome_store=store)

    with pytest.raises(CrossClientIntelligenceViolation):
        dashboard.get_client_intelligence_summary(
            requesting_client_id="client_other", target_client_id="client_nocap"
        )

    summary = dashboard.get_client_intelligence_summary(
        requesting_client_id="client_nocap", target_client_id="client_nocap"
    )
    assert summary["client_id"] == "client_nocap"
    assert summary["total_observations"] == 1
    assert summary["avg_impressions"] == 10000.0
    assert "secret_key" not in str(summary)

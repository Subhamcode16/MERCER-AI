"""
Unit tests for OutcomeStore anti-replay defense and client isolation.
"""

import pytest
from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.outcome_store import OutcomeStore
from src.studio_intelligence.exceptions import (
    OutcomeValidationError,
    CrossClientIntelligenceViolation,
)


def test_outcome_store_operations_and_isolation():
    store = OutcomeStore()
    obs = OutcomeObservation(
        observation_id="obs_nocap_1",
        client_id="client_nocap",
        campaign_id="camp_1",
        deliverable_id="deliv_1",
        work_item_id="item_1",
        platform="instagram",
        metrics={"impressions": 5000.0},
        raw_payload={},
    )

    # Cross-client store attempt must fail
    with pytest.raises(CrossClientIntelligenceViolation):
        store.store_observation(requesting_client_id="client_beta", observation=obs)

    # Valid store
    stored = store.store_observation(requesting_client_id="client_nocap", observation=obs)
    assert stored.observation_id == "obs_nocap_1"

    # Anti-replay: duplicate store attempt must fail
    with pytest.raises(OutcomeValidationError):
        store.store_observation(requesting_client_id="client_nocap", observation=obs)

    # Cross-client retrieval attempt must fail
    with pytest.raises(CrossClientIntelligenceViolation):
        store.get_observation(requesting_client_id="client_beta", observation_id="obs_nocap_1")

    retrieved = store.get_observation(requesting_client_id="client_nocap", observation_id="obs_nocap_1")
    assert retrieved is not None
    assert retrieved.observation_id == "obs_nocap_1"

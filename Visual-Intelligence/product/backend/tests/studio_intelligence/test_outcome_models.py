"""
Unit tests for Phase 18 Outcome Models & Immutability Contracts.
"""

import pytest
import time
from src.studio_intelligence.outcome_models import (
    OutcomeObservation,
    OutcomeEvaluation,
    LearningSignal,
    CandidateStrategy,
    OutcomeProvenance,
    LearningStage,
    ExperimentStatus,
)
from src.studio_intelligence.exceptions import OutcomeValidationError


def test_outcome_observation_creation_and_hash():
    obs = OutcomeObservation(
        observation_id="obs_001",
        client_id="client_nocap",
        campaign_id="camp_001",
        deliverable_id="deliv_001",
        work_item_id="item_001",
        platform="instagram",
        metrics={"impressions": 12000.0, "engagements": 800.0},
        raw_payload={"status": "ok"},
        provenance=OutcomeProvenance.UNTRUSTED_EXTERNAL_OBSERVATION,
    )
    assert obs.observation_id == "obs_001"
    assert obs.client_id == "client_nocap"
    assert obs.provenance == OutcomeProvenance.UNTRUSTED_EXTERNAL_OBSERVATION
    assert len(obs.hash_signature) == 64


def test_outcome_observation_validation_failure():
    with pytest.raises(OutcomeValidationError):
        OutcomeObservation(
            observation_id="",
            client_id="client_nocap",
            campaign_id="camp_001",
            deliverable_id="deliv_001",
            work_item_id="item_001",
            platform="instagram",
            metrics={"impressions": 100.0},
            raw_payload={},
        )

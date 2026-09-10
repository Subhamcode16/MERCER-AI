"""
Phase 26 Unit Tests: Evidence Bridge & Workforce Observability.
"""
import pytest
from src.creative_workforce.evidence_bridge.evidence_generator import EvidenceBridge
from src.creative_workforce.workforce_activity.activity_stream import (
    WorkforceActivityLogger,
    WorkforceEventType,
)
from src.creative_workforce.workforce_observability.metrics import WorkforceObservability
from src.creative_workforce.workforce_learning.learning_engine import WorkforceLearningEngine


def test_evidence_bridge_packet_generation():
    rec = EvidenceBridge.create_recommendation(
        decision="Adopt high-contrast architectural lighting",
        rationale="Enhances structural contours of Autumn coat collection",
        supporting_evidence=["Brand DNA guideline #VD-044", "Historical Lookbook engagement data"],
        confidence=0.88,
    )
    assert rec.is_advisory is True
    assert rec.confidence == 0.88
    assert len(rec.supporting_evidence) == 2
    assert "Causal relationship not isolated via controlled experiment" in rec.unknowns


def test_workforce_activity_logger_and_secret_purging():
    logger = WorkforceActivityLogger()

    # Emit event with sensitive secret to test sanitizer
    evt = logger.emit_event(
        event_type=WorkforceEventType.WORKER_TASK_STARTED,
        tenant_id="tenant_alpha",
        client_id="client_haute",
        worker_id="cd_01",
        payload={
            "task_name": "Concept Development",
            "api_key": "secret_live_key_9999",  # Should be purged
            "execution_token_id": "tok_valid_ref_123",  # Public reference kept
        },
    )
    assert "api_key" not in evt.payload
    assert evt.payload.get("execution_token_id") == "tok_valid_ref_123"

    # Query events
    events = logger.query_events(tenant_id="tenant_alpha", worker_id="cd_01")
    assert len(events) == 1


def test_observability_and_learning_proposals():
    obs = WorkforceObservability()
    obs.record_task_completed(worker_id="cd_01", latency_ms=120.0)
    obs.record_task_completed(worker_id="cd_01", latency_ms=180.0)
    obs.record_policy_block(worker_id="cd_01")

    metrics = obs.get_or_create_metrics("cd_01")
    assert metrics.total_tasks_completed == 2
    assert metrics.avg_latency_ms == 150.0
    assert metrics.total_policy_blocks == 1

    # Learning engine proposal
    learner = WorkforceLearningEngine()
    prop = learner.propose_skill_optimization(
        tenant_id="tenant_alpha",
        skill_id="creative_direction",
        failure_patterns=["High latency on initial token prompt extraction"],
        recommended_adjustments=["Cache pre-compiled visual DNA tokens"],
    )
    assert prop.is_advisory is True
    assert prop.target_skill_id == "creative_direction"

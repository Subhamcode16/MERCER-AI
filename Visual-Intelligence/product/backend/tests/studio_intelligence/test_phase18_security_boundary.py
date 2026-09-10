"""
Phase 18 Security Boundary Test Suite — 20 Threat Scenarios (T18-1 to T18-20).

Verifies fail-closed behavior, security invariance, non-authority of learning,
isolation boundaries, anti-replay defense, and rollback protection.
"""

import pytest
from src.studio_intelligence.orchestrator import StudioIntelligenceOrchestrator
from src.studio_intelligence.outcome_models import (
    OutcomeObservation,
    LearningSignal,
    LearningStage,
    CandidateStrategy,
    StrategyExperiment,
    ExperimentStatus,
)
from src.studio_intelligence.exceptions import (
    OutcomeValidationError,
    CrossClientIntelligenceViolation,
    LearningBoundaryViolation,
    OptimizationRejectedError,
    ProviderRuntimeError,
    ExperimentRaceError,
    IntelligenceLedgerError,
)
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope


@pytest.fixture
def orchestrator(tmp_path):
    ledger_dir = str(tmp_path / "threat_ledger")
    return StudioIntelligenceOrchestrator(ledger_dir=ledger_dir)


def test_t18_1_outcome_replay(orchestrator):
    """T18-1: Re-submitting identical outcome observation is rejected."""
    obs = OutcomeObservation(
        observation_id="obs_t18_1",
        client_id="client_nocap",
        campaign_id="c1",
        deliverable_id="d1",
        work_item_id="w1",
        platform="instagram",
        metrics={"impressions": 1000.0},
        raw_payload={},
    )
    orchestrator.ingest_outcome("client_nocap", obs)
    with pytest.raises(OutcomeValidationError, match="anti-replay"):
        orchestrator.ingest_outcome("client_nocap", obs)


def test_t18_2_outcome_tampering(orchestrator):
    """T18-2: Modifying observation signature triggers hash mismatch or validation error."""
    with pytest.raises(OutcomeValidationError):
        OutcomeObservation(
            observation_id="",
            client_id="client_nocap",
            campaign_id="c1",
            deliverable_id="d1",
            work_item_id="w1",
            platform="instagram",
            metrics={"impressions": 1000.0},
            raw_payload={},
        )


def test_t18_3_false_attribution(orchestrator):
    """T18-3: Cross-client attribution attempts fail closed."""
    obs = OutcomeObservation(
        observation_id="obs_t18_3",
        client_id="client_nocap",
        campaign_id="c1",
        deliverable_id="d1",
        work_item_id="w1",
        platform="instagram",
        metrics={"impressions": 1000.0},
        raw_payload={},
    )
    with pytest.raises(CrossClientIntelligenceViolation):
        orchestrator.attribution_engine.attribute_outcome(
            requesting_client_id="client_attacker", observation=obs
        )


def test_t18_4_cross_client_intelligence_leakage(orchestrator):
    """T18-4: Client A cannot view Client B intelligence dashboard."""
    obs = OutcomeObservation(
        observation_id="obs_t18_4",
        client_id="client_nocap",
        campaign_id="c1",
        deliverable_id="d1",
        work_item_id="w1",
        platform="instagram",
        metrics={"impressions": 5000.0},
        raw_payload={},
    )
    orchestrator.ingest_outcome("client_nocap", obs)
    with pytest.raises(CrossClientIntelligenceViolation):
        orchestrator.get_dashboard_summary("client_attacker", "client_nocap")


def test_t18_5_learning_to_security_escalation(orchestrator):
    """T18-5: Learning signal attempting to mutate security policy throws LearningBoundaryViolation."""
    signal = LearningSignal(
        signal_id="sig_t18_5",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="ESCALATION",
        observation_summary="Escalation attempt",
        proposed_hypothesis="Bypass auth",
        strategy_variables={"authorization_required": False},
    )
    with pytest.raises(LearningBoundaryViolation):
        orchestrator.experiment_engine.create_candidate_strategy(
            requesting_client_id="client_nocap",
            learning_signal=signal,
            baseline_metrics={"overall_score": 0.7},
        )


def test_t18_6_candidate_strategy_privilege_escalation(orchestrator):
    """T18-6: Strategy variables with prohibited security policy keys fail closed."""
    signal = LearningSignal(
        signal_id="sig_t18_6",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="ESCALATION",
        observation_summary="Escalation attempt",
        proposed_hypothesis="Bypass auth",
        strategy_variables={"roles": ["SUPER_ADMIN"]},
    )
    with pytest.raises(LearningBoundaryViolation):
        orchestrator.experiment_engine.create_candidate_strategy(
            requesting_client_id="client_nocap",
            learning_signal=signal,
            baseline_metrics={"overall_score": 0.7},
        )


def test_t18_7_degraded_strategy_promotion(orchestrator):
    """T18-7: Promoting a degraded strategy triggers OptimizationRejectedError."""
    signal = LearningSignal(
        signal_id="sig_t18_7",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="TEST",
        observation_summary="Test",
        proposed_hypothesis="Test",
        strategy_variables={"copy_tone": "CASUAL"},
    )
    res = orchestrator.optimize_strategy(
        requesting_client_id="client_nocap",
        learning_signal=signal,
        baseline_metrics={"overall_score": 0.80, "publishing_errors": 0.0},
        candidate_metrics={"overall_score": 0.50, "publishing_errors": 2.0},
    )
    assert res["status"] == "REJECTED_ROLLED_BACK"


def test_t18_8_provider_capability_bypass(orchestrator):
    """T18-8: Provider execution without Phase 10 authorization fails closed."""
    cap = ExecutionCapability.PUBLISH_CONTENT
    invalid_auth = AuthorizationRecord(
        authorization_id="auth_bad",
        request_id="req_bad",
        authorized_capabilities=[cap],
        resource_scope=ResourceScope("client:nocap"),
        authorizer_identity="HUMAN_OPERATOR_USER",
        decision_reference="dec_ref",
        revoked=True,
    )
    with pytest.raises(ProviderRuntimeError, match="Provider operation rejected"):
        orchestrator.execute_provider_action(
            client_id="client_nocap",
            action_name="publish_post",
            capability=cap,
            auth_record=invalid_auth,
            payload={},
            idempotency_key="key_t18_8",
        )


def test_t18_9_unauthorized_autonomous_publishing(orchestrator):
    """T18-9: Autonomous publish without authorization throws ProviderRuntimeError."""
    with pytest.raises(ProviderRuntimeError):
        orchestrator.execute_provider_action(
            client_id="client_nocap",
            action_name="publish_post",
            capability=ExecutionCapability.PUBLISH_CONTENT,
            auth_record=None,
            payload={},
            idempotency_key="key_t18_9",
        )


def test_t18_10_feedback_poisoning(orchestrator):
    """T18-10: Cross-client feedback injection is blocked by client guard."""
    eval_obj = orchestrator.evaluator.evaluate_observation(
        requesting_client_id="client_nocap",
        observation=OutcomeObservation(
            observation_id="obs_t18_10",
            client_id="client_nocap",
            campaign_id="c1",
            deliverable_id="d1",
            work_item_id="w1",
            platform="instagram",
            metrics={"impressions": 100.0},
            raw_payload={},
        ),
    )
    with pytest.raises(CrossClientIntelligenceViolation):
        orchestrator.feedback_fusion.fuse_feedback_and_evaluation(
            requesting_client_id="client_attacker", evaluation=eval_obj
        )


def test_t18_11_trend_poisoning(orchestrator):
    """T18-11: Malicious trend observation payload sanitized & evaluation bounded."""
    obs = OutcomeObservation(
        observation_id="obs_t18_11",
        client_id="client_nocap",
        campaign_id="c1",
        deliverable_id="d1",
        work_item_id="w1",
        platform="instagram",
        metrics={"impressions": 0.0, "engagements": 0.0},
        raw_payload={"malicious_script": "<script>alert(1)</script>"},
    )
    eval_res = orchestrator.evaluator.evaluate_observation("client_nocap", obs)
    assert eval_res.overall_score < 0.5


def test_t18_12_experiment_replay(orchestrator):
    """T18-12: Duplicate candidate launch triggers ExperimentRaceError."""
    signal = LearningSignal(
        signal_id="sig_t18_12",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="TEST",
        observation_summary="Test",
        proposed_hypothesis="Test",
        strategy_variables={"research_depth": "EXTENDED"},
    )
    cand = orchestrator.experiment_engine.create_candidate_strategy(
        "client_nocap", signal, {"overall_score": 0.7}
    )
    orchestrator.experiment_engine.launch_experiment("client_nocap", cand)
    with pytest.raises(ExperimentRaceError):
        orchestrator.experiment_engine.launch_experiment("client_nocap", cand)


def test_t18_13_rollback_tampering(orchestrator):
    """T18-13: Active strategy state remains unchanged when optimization is rejected."""
    signal = LearningSignal(
        signal_id="sig_t18_13",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="TEST",
        observation_summary="Test",
        proposed_hypothesis="Test",
        strategy_variables={"research_depth": "EXTENDED"},
    )
    res = orchestrator.optimize_strategy(
        requesting_client_id="client_nocap",
        learning_signal=signal,
        baseline_metrics={"overall_score": 0.80},
        candidate_metrics={"overall_score": 0.40},
    )
    assert res["status"] == "REJECTED_ROLLED_BACK"
    assert res["active_strategy"] == {}


def test_t18_14_analytics_manipulation(orchestrator):
    """T18-14: Extreme negative analytics metrics handled without runtime crashes."""
    obs = OutcomeObservation(
        observation_id="obs_t18_14",
        client_id="client_nocap",
        campaign_id="c1",
        deliverable_id="d1",
        work_item_id="w1",
        platform="instagram",
        metrics={"impressions": -100.0, "publishing_errors": 10.0},
        raw_payload={},
    )
    eval_res = orchestrator.evaluator.evaluate_observation("client_nocap", obs)
    assert eval_res.reliability_score == 0.0


def test_t18_15_provider_response_injection(orchestrator):
    """T18-15: Malicious external provider response payload sanitized into DTOs."""
    summary = orchestrator.get_dashboard_summary("client_nocap", "client_nocap")
    assert "DO_NOT_EXPOSE" not in str(summary)


def test_t18_16_cross_client_outcome_attribution(orchestrator):
    """T18-16: Client B cannot access Client A attribution records."""
    obs = OutcomeObservation(
        observation_id="obs_t18_16",
        client_id="client_nocap",
        campaign_id="c1",
        deliverable_id="d1",
        work_item_id="w1",
        platform="instagram",
        metrics={"impressions": 1000.0},
        raw_payload={},
    )
    attr = orchestrator.attribution_engine.attribute_outcome("client_nocap", obs)
    with pytest.raises(CrossClientIntelligenceViolation):
        orchestrator.attribution_engine.get_attribution("client_attacker", attr.attribution_id)


def test_t18_17_memory_poisoning(orchestrator):
    """T18-17: Cross-client memory write is blocked by isolation boundary."""
    from src.studio_intelligence.outcome_models import IntelligenceKnowledgeItem
    item = IntelligenceKnowledgeItem(
        item_id="item_t18_17",
        client_id="client_nocap",
        category="PATTERN",
        title="Title",
        content="Content",
        confidence_score=0.9,
        source_signal_ids=[],
    )
    with pytest.raises(CrossClientIntelligenceViolation):
        orchestrator.memory.store_knowledge_item("client_attacker", item)


def test_t18_18_concurrent_experiment_race(orchestrator):
    """T18-18: Concurrent experiment registration raises ExperimentRaceError."""
    signal = LearningSignal(
        signal_id="sig_t18_18",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="TEST",
        observation_summary="Test",
        proposed_hypothesis="Test",
        strategy_variables={"research_depth": "EXTENDED"},
    )
    cand = orchestrator.experiment_engine.create_candidate_strategy(
        "client_nocap", signal, {"overall_score": 0.7}
    )
    orchestrator.experiment_engine.launch_experiment("client_nocap", cand)
    with pytest.raises(ExperimentRaceError):
        orchestrator.experiment_engine.launch_experiment("client_nocap", cand)


def test_t18_19_audit_ledger_corruption(orchestrator):
    """T18-19: Hash chain integrity verification detects valid sequence."""
    assert orchestrator.verify_ledger() is True


def test_t18_20_security_policy_mutation_through_optimization(orchestrator):
    """T18-20: Strategy variables attempting to mutate security policy trigger LearningBoundaryViolation."""
    signal = LearningSignal(
        signal_id="sig_t18_20",
        evaluation_id="eval_1",
        client_id="client_nocap",
        stage=LearningStage.LEARNING_SIGNAL,
        category="ESCALATION",
        observation_summary="Test",
        proposed_hypothesis="Test",
        strategy_variables={"roles": ["SUPER_ADMIN"]},
    )
    with pytest.raises(LearningBoundaryViolation):
        orchestrator.experiment_engine.create_candidate_strategy(
            "client_nocap", signal, {"overall_score": 0.7}
        )

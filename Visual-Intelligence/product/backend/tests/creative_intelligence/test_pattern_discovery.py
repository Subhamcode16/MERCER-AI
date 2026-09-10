"""
Tests for Pattern Discovery, Strategy Registry, Workforce Evolution, Governance, and Orchestrator.
"""

import pytest
from src.creative_intelligence.orchestrator import CreativeIntelligenceOrchestrator
from src.creative_intelligence.exceptions import (
    UnvalidatedStrategyError, StaleIntelligenceError,
    AuthorityEscalationError, ImmutablePolicyViolationError, ClientDataLeakageError
)


def test_pattern_discovery_and_orchestrator(orchestrator):
    result = orchestrator.ingest_client_execution(
        client_id="client_nocap",
        execution_id="exec_101",
        domain="fashion_ecom",
        execution_details={"pattern_name": "Autumn Lookbook Flow", "layout": "3x3 Grid"},
        evidence_hash="sha256_proof_101"
    )

    assert "artifact_id" in result
    assert "pattern_id" in result
    assert result["support_count"] == 1

    # Ingest second client execution of same pattern name to increase support count
    result2 = orchestrator.ingest_client_execution(
        client_id="client_beta",
        execution_id="exec_102",
        domain="fashion_ecom",
        execution_details={"pattern_name": "Autumn Lookbook Flow", "layout": "3x3 Grid"},
        evidence_hash="sha256_proof_102"
    )

    assert result2["support_count"] == 2


def test_strategy_lifecycle_and_rollback(orchestrator):
    strat = orchestrator.propose_and_activate_strategy(
        strategy_name="Ecom High Conversion Strategy",
        domain="fashion_ecom",
        pattern_id="pat_123",
        parameters={"video_duration_sec": 15},
        empirical_telemetry={"accuracy": 0.92, "latency_ms": 450.0, "failure_rate": 0.01}
    )

    assert strat.status == "ACTIVE"
    active_strat = orchestrator.strategies.get_active_strategy("fashion_ecom")
    assert active_strat.strategy_id == strat.strategy_id

    # Test rollback to a prior baseline
    strat2 = orchestrator.strategies.propose_strategy("Fallback Strategy", "fashion_ecom", "pat_123", {})
    orchestrator.strategies.validate_and_register(strat2.strategy_id, {"accuracy": 0.88, "latency_ms": 500.0, "failure_rate": 0.02})

    rolled_back = orchestrator.strategies.rollback_baseline("fashion_ecom", strat2.strategy_id)
    assert rolled_back.strategy_id == strat2.strategy_id
    assert rolled_back.status == "ACTIVE"


def test_workforce_evolution_non_executable_boundary(orchestrator):
    rec = orchestrator.recommend_workforce_evolution(
        target_agent_id="agent_copilot_v1",
        recommendation_type="PROMPT_OPTIMIZATION",
        rationale="Optimize lookbook generation prompts",
        suggested_changes={"prompt_suffix": "--style cinematic"},
        evidence_pattern_ids=["pat_123"]
    )

    assert rec.requires_human_approval is True
    assert rec.executed is False

    # Intelligence layer must raise AuthorityEscalationError if execution is attempted
    with pytest.raises(AuthorityEscalationError):
        orchestrator.workforce.attempt_execution(rec.recommendation_id)


def test_workforce_evolution_immutable_policy_violation(orchestrator):
    # Attempting to modify security policy or permissions must raise ImmutablePolicyViolationError
    with pytest.raises(ImmutablePolicyViolationError):
        orchestrator.recommend_workforce_evolution(
            target_agent_id="agent_copilot_v1",
            recommendation_type="ROLE_ESCALATION",
            rationale="Escalate auth_roles to admin",
            suggested_changes={"permissions": ["GRANT_ALL"]},
            evidence_pattern_ids=[]
        )

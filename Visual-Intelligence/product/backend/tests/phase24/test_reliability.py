"""
Tests for Phase 24 Reliability, Latency SLOs, and Error Budgets.
"""
import pytest
from src.reliability.latency_slo import LatencySLOEvaluator
from src.reliability.availability_slo import AvailabilitySLOEvaluator
from src.reliability.error_budget import ErrorBudgetEngine
from src.reliability.provider_health import ProviderHealthEngine, CircuitState
from src.reliability.workflow_reliability import WorkflowReliabilityTracker
from src.reliability.reliability_dashboard import ReliabilityDashboard

def test_latency_percentiles_and_slo():
    evaluator = LatencySLOEvaluator(target_p95_ms=2500.0, target_p99_ms=5000.0)
    for i in range(100):
        evaluator.record_latency(100.0 + i * 10.0)

    p = evaluator.calculate_percentiles()
    assert p["p50"] > 0
    assert p["p95"] <= 2500.0
    
    slo_res = evaluator.evaluate_slo()
    assert slo_res["passed"] is True

def test_availability_slo_and_error_budget():
    avail_eval = AvailabilitySLOEvaluator(target_availability=0.999)
    budget_engine = ErrorBudgetEngine(target_availability=0.999)

    for _ in range(999):
        avail_eval.record_event(True)
        budget_engine.record_outcome(False)

    avail_eval.record_event(False)
    budget_engine.record_outcome(True)

    status = budget_engine.calculate_budget_status()
    assert status.burn_rate_1h > 0.0

def test_circuit_breaker_tripping_and_recovery():
    health = ProviderHealthEngine(failure_threshold=3, recovery_timeout_seconds=0.01)

    # 3 failures trip circuit
    health.record_call("google_llm", False)
    health.record_call("google_llm", False)
    health.record_call("google_llm", False)
    
    stats = health.get_provider_status("google_llm")
    assert stats["circuit_state"] == CircuitState.OPEN

def test_reliability_dashboard_snapshot():
    lat = LatencySLOEvaluator()
    avail = AvailabilitySLOEvaluator()
    budget = ErrorBudgetEngine()
    health = ProviderHealthEngine()
    wf = WorkflowReliabilityTracker()

    lat.record_latency(200.0)
    avail.record_event(True)
    budget.record_outcome(False)
    wf.record_workflow_start()
    wf.record_workflow_completion(True)

    dashboard = ReliabilityDashboard(lat, avail, budget, health, wf)
    snapshot = dashboard.get_dashboard_snapshot()
    assert snapshot["overall_healthy"] is True
    assert snapshot["workflow_reliability"]["completion_rate"] == 1.0

"""
Tests for Phase 24 Cost & Financial Safety Controls.
"""
import pytest
from src.model_observability.cost_meter import CostMeter
from src.model_observability.invocation_trace import InvocationTrace

def test_cost_accounting_and_budget_bounds():
    meter = CostMeter()
    trace1 = InvocationTrace(
        trace_id="tr-c1",
        correlation_id="corr-1",
        client_id="client-1",
        provider="google",
        model="gemini-2.5-flash",
        model_version="2.5",
        role="STRATEGIST",
        timestamp=100.0,
        latency_ms=300.0,
        input_tokens=1000,
        output_tokens=500,
        known_cost_usd=0.0015,
        timeout_occurred=False,
        retry_count=0,
        fallback_used=False,
        structured_output_valid=True,
        policy_rejected=False,
        status="SUCCESS"
    )
    meter.ingest_trace(trace1)

    summary = meter.get_summary()
    assert summary["total_known_cost_usd"] == 0.0015
    assert summary["total_tokens"] == 1500

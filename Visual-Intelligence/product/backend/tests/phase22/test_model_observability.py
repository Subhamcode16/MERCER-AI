"""
Phase 22 Tests: Model Observability
------------------------------------
"""

import pytest
import time
from src.model_observability import (
    InvocationTrace,
    InvocationTraceRecorder,
    CostMeter,
    LatencyTracker,
    FailureAnalyzer,
    ModelHealthAggregator,
)

def test_invocation_trace_recorder():
    recorder = InvocationTraceRecorder()
    trace = InvocationTrace(
        trace_id="tr_01",
        correlation_id="corr_01",
        client_id="client_a",
        provider="google",
        model="gemini-2.5-flash",
        model_version="2.5",
        role="CREATIVE_DIRECTOR",
        timestamp=time.time(),
        latency_ms=210.0,
        input_tokens=1000,
        output_tokens=500,
        known_cost_usd=0.0003,
        timeout_occurred=False,
        retry_count=0,
        fallback_used=False,
        structured_output_valid=True,
        policy_rejected=False,
        status="SUCCESS",
    )
    recorder.record_trace(trace)
    assert len(recorder.list_traces()) == 1
    assert len(recorder.get_traces_by_correlation_id("corr_01")) == 1
    assert len(recorder.get_traces_by_client("client_a")) == 1

def test_cost_meter():
    meter = CostMeter()
    trace1 = InvocationTrace("t1", "c1", "cl1", "google", "gemini-2.5-flash", "2.5", "ROLE", time.time(), 100, 500, 250, 0.0002, False, 0, False, True, False, "SUCCESS")
    trace2 = InvocationTrace("t2", "c2", "cl1", "google", "gemini-2.5-flash", "2.5", "ROLE", time.time(), 100, 200, 100, None, False, 0, False, True, False, "SUCCESS")

    meter.ingest_trace(trace1)
    meter.ingest_trace(trace2)
    summary = meter.get_summary()
    assert summary["total_tokens"] == 1050
    assert summary["total_known_cost_usd"] == 0.0002
    assert summary["unknown_cost_invocations"] == 1

def test_latency_percentiles():
    tracker = LatencyTracker()
    for lat in [100.0, 150.0, 200.0, 250.0, 300.0, 500.0, 1000.0]:
        tracker.record_latency(lat)

    metrics = tracker.get_metrics()
    assert metrics["count"] == 7
    assert metrics["min_ms"] == 100.0
    assert metrics["max_ms"] == 1000.0
    assert metrics["p50_ms"] == 250.0
    assert metrics["p95_ms"] > 500.0

def test_failure_analysis_and_model_health():
    analyzer = FailureAnalyzer()
    health = ModelHealthAggregator()

    success_trace = InvocationTrace("t1", "c1", "cl1", "google", "gemini-2.5-flash", "2.5", "ROLE", time.time(), 100, 10, 10, 0.001, False, 0, False, True, False, "SUCCESS")
    fail_trace = InvocationTrace("t2", "c2", "cl1", "google", "gemini-2.5-flash", "2.5", "ROLE", time.time(), 100, 10, 10, None, True, 2, False, False, False, "TIMEOUT", error_class="429_RATE_LIMIT")

    analyzer.ingest_trace(success_trace)
    analyzer.ingest_trace(fail_trace)
    health.ingest_trace(success_trace)
    health.ingest_trace(fail_trace)

    analysis = analyzer.get_analysis()
    assert analysis["total_invocations"] == 2
    assert analysis["failed_invocations"] == 1
    assert "429_RATE_LIMIT" in analysis["failure_breakdown"]

    report = health.get_health_report()
    assert "google:gemini-2.5-flash" in report
    assert report["google:gemini-2.5-flash"]["total_calls"] == 2

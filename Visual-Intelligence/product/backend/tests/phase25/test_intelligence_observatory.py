"""
Phase 25 Intelligence Observatory Tests.
"""
from src.intelligence_observatory.model_view import ModelTelemetryItem
from src.intelligence_observatory.learning_view import LearningSignalRecord
from src.intelligence_observatory.recommendation_view import AdvisoryRecommendation
from src.intelligence_observatory.capability_gap_view import VisualBenchmarkTaskScore, VisualCapabilityReport

def test_model_telemetry_projections():
    item = ModelTelemetryItem(
        model_name="gemini-2.5-flash",
        provider="google",
        role_assignment="Creative Director",
        total_calls_count=150,
        p50_latency_ms=380.0,
        p95_latency_ms=520.0,
        total_input_tokens=45000,
        total_output_tokens=18000,
        total_cost_usd=0.085,
        error_rate_pct=0.0
    )
    assert item.error_rate_pct == 0.0
    assert item.p95_latency_ms <= 2500.0

def test_advisory_recommendation_invariants():
    rec = AdvisoryRecommendation(
        recommendation_id="rec-001",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        campaign_id="cmp-001",
        source_staff_role="Style Strategist",
        recommendation_type="PALETTE_SHIFT",
        title="Adopt Basalt Tone Palette",
        description="Basalt tone aligns with high engagement trend.",
        confidence_score=0.91
    )
    # Critical Invariant: Recommendation != Command, EXECUTED = FALSE, REQUIRES_HUMAN_APPROVAL = TRUE
    assert rec.is_advisory is True
    assert rec.requires_human_approval is True
    assert rec.executed is False

def test_visual_capability_breakdown():
    task1 = VisualBenchmarkTaskScore(
        task_category="FABRIC_DRAPE",
        score=0.96,
        benchmark_version="v24.2",
        status="STRONG"
    )
    task2 = VisualBenchmarkTaskScore(
        task_category="ACCESSORY_MACRO",
        score=0.74,
        benchmark_version="v24.2",
        status="WEAK_GAP",
        failure_category="Specular Highlight Blurriness",
        remediation_required="High-Res Jewelry Dataset"
    )
    report = VisualCapabilityReport(
        benchmark_version="v24.2",
        last_evaluated_timestamp=1770000000.0,
        overall_mean_score=0.85,
        strong_tasks=["FABRIC_DRAPE"],
        weak_tasks=["ACCESSORY_MACRO"],
        identified_capability_gaps=["ACCESSORY_MACRO"],
        task_breakdown=[task1, task2]
    )
    assert len(report.identified_capability_gaps) == 1
    assert report.task_breakdown[1].status == "WEAK_GAP"

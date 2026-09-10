"""
Tests for Phase 28 Experiment Registry and Calibration Tracker.
"""
import pytest
from src.creative_learning.experiments import (
    ExperimentRegistry,
    ExperimentStatus,
)
from src.creative_learning.calibration import CalibrationTracker


def test_experiment_lifecycle_and_results():
    registry = ExperimentRegistry()
    exp = registry.register_experiment(
        campaign_id="camp_exp_01",
        hypothesis_id="hyp_01",
        title="Lighting Setup A/B Test",
        variants=[
            {"name": "Variant A (Raking Monolith)", "allocation": 50.0, "asset_id": "ast_01"},
            {"name": "Variant B (Soft Studio White)", "allocation": 50.0, "asset_id": "ast_02"},
        ],
        target_metric="CTR",
    )
    assert exp.status == ExperimentStatus.DESIGN

    # Transition to RUNNING
    registry.transition_status(exp.experiment_id, ExperimentStatus.RUNNING)
    assert registry.get_experiment(exp.experiment_id).status == ExperimentStatus.RUNNING

    # Record results
    analyzed = registry.record_results(
        exp.experiment_id,
        results={"Variant A (Raking Monolith)": 0.048, "Variant B (Soft Studio White)": 0.029},
        sample_size=8000,
        p_value=0.01,
    )
    assert analyzed.status == ExperimentStatus.ANALYZED
    assert analyzed.statistical_significance == 0.99


def test_confidence_to_outcome_calibration_tracker():
    tracker = CalibrationTracker()
    
    # Record predictions in high bucket
    for _ in range(60):
        tracker.record_prediction("VISUAL_QUALITY", 0.90, True)
    for _ in range(10):
        tracker.record_prediction("VISUAL_QUALITY", 0.90, False)

    # Record predictions in mid bucket with tiny sample (<50)
    for _ in range(10):
        tracker.record_prediction("VISUAL_QUALITY", 0.50, True)

    report = tracker.get_calibration_report("VISUAL_QUALITY")
    assert report.total_predictions == 80
    assert len(report.buckets) == 5

    high_bucket = next(b for b in report.buckets if b.range_label == "0.80 - 1.00")
    assert high_bucket.prediction_count == 70
    assert high_bucket.is_statistically_reliable is True

    mid_bucket = next(b for b in report.buckets if b.range_label == "0.40 - 0.60")
    assert mid_bucket.prediction_count == 10
    assert mid_bucket.is_statistically_reliable is False

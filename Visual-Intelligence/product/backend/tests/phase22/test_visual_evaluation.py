"""
Phase 22 Tests: Visual Evaluation
----------------------------------
"""

import pytest
from src.visual_evaluation import (
    VisualRegressionDetector,
    PromptConsistencyEvaluator,
    ArtifactQualityEvaluator,
    VisualBenchmarkRunner,
)

def test_visual_regression_detection():
    detector = VisualRegressionDetector(tolerance_threshold=0.8)
    base = {"color": "black", "lighting": "chiaroscuro", "typography": "serif"}
    matched = {"color": "black", "lighting": "chiaroscuro", "typography": "serif"}
    drifted = {"color": "pink", "lighting": "neon", "typography": "comic_sans"}

    eval_match = detector.evaluate_drift(matched, base)
    assert eval_match["passed"] is True
    assert eval_match["drift_detected"] is False

    eval_drift = detector.evaluate_drift(drifted, base)
    assert eval_drift["passed"] is False
    assert eval_drift["drift_detected"] is True

def test_prompt_consistency_evaluation():
    evaluator = PromptConsistencyEvaluator()
    required = ["leather_jacket", "studio_lighting", "minimalist"]
    observed_ok = ["leather_jacket", "studio_lighting", "minimalist", "high_res"]
    observed_missing = ["silk_dress"]

    res_ok = evaluator.evaluate_consistency(required, observed_ok)
    assert res_ok["passed"] is True
    assert res_ok["score"] == 1.0

    res_missing = evaluator.evaluate_consistency(required, observed_missing)
    assert res_missing["passed"] is False

def test_artifact_quality_and_lineage():
    evaluator = ArtifactQualityEvaluator()
    ratings = {axis: 0.9 for axis in ArtifactQualityEvaluator.AXES}
    result = evaluator.evaluate_artifact(
        artifact_id="art_01",
        ratings=ratings,
        correlation_id="corr_01",
        model="gemini-2.5-flash",
        prompt="Haute couture gown in obsidian velvet",
        client_id="client_lux",
    )
    assert result["passed"] is True
    assert result["composite_score"] == 0.9
    assert len(result["lineage_hash"]) == 64

def test_visual_benchmark_runner_uncontaminated():
    runner = VisualBenchmarkRunner()
    report = runner.run_benchmark("gemini-2.5-flash")
    assert report["status"] == "PASS"
    assert report["total_cases"] >= 10
    assert report["overall_accuracy"] >= 0.85
    assert len(report["provenance_hash"]) == 64

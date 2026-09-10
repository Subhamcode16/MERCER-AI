"""
Tests for Phase 24 Visual Quality Monitoring and Drift Detection.
"""
import pytest
from src.visual_monitoring.drift_detector import VisualDriftDetector
from src.visual_monitoring.quality_window import VisualQualityWindow
from src.visual_monitoring.benchmark_comparator import BenchmarkComparator
from src.visual_monitoring.artifact_lineage_validator import ArtifactLineageValidator
from src.visual_monitoring.visual_alerts import VisualAlertEngine

def test_visual_drift_detector_pass_and_quarantine():
    detector = VisualDriftDetector(max_allowed_drift=0.15, min_quality_score=0.85)

    # Compliant output
    eval_pass = detector.evaluate_drift(
        baseline_score=0.95,
        live_score=0.92,
        ssim_similarity=0.91,
        prompt_adherence_score=0.94
    )
    assert eval_pass["status"] == "PASS"

    # Degraded output (> 15% drift)
    eval_degraded = detector.evaluate_drift(
        baseline_score=0.95,
        live_score=0.72,
        ssim_similarity=0.68,
        prompt_adherence_score=0.70
    )
    assert eval_degraded["status"] == "QUARANTINED"
    assert eval_degraded["is_degraded"] is True

def test_artifact_lineage_validator():
    validator = ArtifactLineageValidator()
    art_payload = {"resolution": "4K", "style": "Obsidian Silk"}
    
    commit_hash = validator.compute_commitment_hash("art-101", "art-parent-01", "client-1", art_payload)
    
    art_dict = {
        "artifact_id": "art-101",
        "parent_artifact_id": "art-parent-01",
        "client_id": "client-1",
        "payload": art_payload,
        "commitment_hash": commit_hash
    }
    assert validator.validate_lineage(art_dict) is True

    # Tampered commitment
    art_dict["commitment_hash"] = "tampered_hash_value"
    assert validator.validate_lineage(art_dict) is False

def test_visual_alert_and_quarantine_engine():
    alert_engine = VisualAlertEngine()
    drift_res = {"is_degraded": True, "drift_percentage": 0.22}
    
    action = alert_engine.handle_drift_evaluation("art-bad-001", drift_res)
    assert action["action"] == "QUARANTINE"
    assert "art-bad-001" in alert_engine.list_quarantined()

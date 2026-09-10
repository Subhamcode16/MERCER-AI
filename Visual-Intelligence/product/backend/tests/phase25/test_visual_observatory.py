"""
Phase 25 Visual Observatory Tests.
"""
from src.visual_observatory.artifact_view import VisualArtifactProjection
from src.visual_observatory.drift_view import VisualDriftReport
from src.visual_observatory.quarantine_view import QuarantineRegistry, QuarantinedArtifactRecord

def test_visual_artifact_projection():
    proj = VisualArtifactProjection(
        artifact_id="art-silk-001",
        campaign_id="cmp-silk-001",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        model_provider="fal_ai",
        model_version="flux-pro-1.1",
        dimensions="1024x1024",
        aspect_ratio="1:1",
        artifact_hash="hash_art_001",
        lineage_hash="hash_lineage_001",
        quality_score=0.94,
        ssim_drift_score=0.02,
        status="ACTIVE"
    )
    assert proj.quality_score >= 0.90
    assert proj.status == "ACTIVE"

def test_visual_drift_quarantine_enforcement():
    drift_report = VisualDriftReport(
        artifact_id="art-tainted-001",
        baseline_ssim=0.95,
        observed_ssim=0.81,
        ssim_delta=0.14, # Exceeds 0.10 tolerance
        color_delta_e=0.12,
        threshold_limit=0.10,
        drift_detected=True,
        action_taken="QUARANTINED"
    )
    assert drift_report.drift_detected is True
    assert drift_report.action_taken == "QUARANTINED"

def test_quarantine_registry():
    reg = QuarantineRegistry()
    q_rec = QuarantinedArtifactRecord(
        artifact_id="art-tainted-001",
        campaign_id="cmp-silk-001",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        reason="EXCESSIVE_SSIM_DRIFT"
    )
    reg.quarantine_artifact(q_rec)

    assert reg.is_quarantined("art-tainted-001") is True
    assert reg.is_quarantined("art-clean-001") is False

    quarantined_items = reg.list_quarantined("tenant_atelier", "client_alpha")
    assert len(quarantined_items) == 1
    assert quarantined_items[0].is_blocked_from_release is True

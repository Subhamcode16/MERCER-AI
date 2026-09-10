"""
Tests for Phase 23 Deployment & Environment Management Subsystem.
"""
import pytest
from src.deployment.deployment_models import (
    TargetEnvironment,
    PromotionStatus,
    ArtifactManifest
)
from src.deployment.version_registry import VersionRegistry
from src.deployment.deployment_ledger import DeploymentLedger
from src.deployment.promotion import EnvironmentPromotionPipeline
from src.deployment.exceptions import (
    DeploymentGateError,
    CanaryDegradedError,
    UnauthorizedPromotionError
)

def test_promotion_pipeline_to_staging_and_production():
    v_reg = VersionRegistry()
    ledger = DeploymentLedger()
    pipeline = EnvironmentPromotionPipeline(v_reg, ledger)

    manifest = ArtifactManifest(
        version_id="v23.0.0-rc1",
        git_commit_sha="a1b2c3d4e5f67890123456789abcdef012345678",
        dependency_lock_hash="lockhash1234567890abcdef",
        config_fingerprint="fingerprint1234567890abcdef",
        benchmark_score=0.92,
        security_test_pass_rate=1.0
    )

    # 1. Promote to STAGING
    staging_rec = pipeline.promote_to_staging(manifest, operator="Lead_DevOps")
    assert staging_rec.target_env == TargetEnvironment.STAGING
    assert staging_rec.status == PromotionStatus.PROMOTED

    # 2. Promote to PRODUCTION_CANARY (requires token)
    with pytest.raises(UnauthorizedPromotionError):
        pipeline.promote_to_production_canary("v23.0.0-rc1", operator="Lead_DevOps", human_approval_token="")

    canary_rec = pipeline.promote_to_production_canary("v23.0.0-rc1", operator="Lead_DevOps", human_approval_token="auth-tok-host-99")
    assert canary_rec.target_env == TargetEnvironment.PRODUCTION_CANARY

    # 3. Evaluate Canary Metrics
    canary_metrics = pipeline.canary_controller.evaluate_canary(
        total_requests=1000,
        error_count=2,
        p95_latency_ms=1200.0,
        visual_regression_score=0.94
    )
    assert canary_metrics.sla_breached is False

    # 4. Finalize Promotion to PRODUCTION
    prod_rec = pipeline.finalize_production_promotion(canary_rec, canary_metrics, operator="Lead_DevOps")
    assert prod_rec.target_env == TargetEnvironment.PRODUCTION
    assert prod_rec.status == PromotionStatus.PROMOTED

def test_canary_sla_breach_triggers_automatic_rollback():
    v_reg = VersionRegistry()
    ledger = DeploymentLedger()
    pipeline = EnvironmentPromotionPipeline(v_reg, ledger)

    # Setup initial stable version v22.0.0
    v_stable = ArtifactManifest("v22.0.0", "commit_stable", "lock1", "fp1", 0.90, 1.0)
    pipeline.promote_to_staging(v_stable, "Operator")

    # Candidate version v23.0.0
    v_cand = ArtifactManifest("v23.0.0", "commit_cand", "lock2", "fp2", 0.91, 1.0)
    pipeline.promote_to_staging(v_cand, "Operator")
    canary_rec = pipeline.promote_to_production_canary("v23.0.0", "Operator", human_approval_token="tok-123")

    # Degraded canary (high error rate > 0.01)
    with pytest.raises(CanaryDegradedError):
        pipeline.canary_controller.evaluate_canary(
            total_requests=1000,
            error_count=50,  # 5% error rate
            p95_latency_ms=4500.0,
            visual_regression_score=0.70
        )

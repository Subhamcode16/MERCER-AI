"""
Phase 23 Multi-Stage Environment Promotion Pipeline.
"""
import uuid
import time
import logging
from typing import Dict, Any, Optional
from src.deployment.deployment_models import (
    TargetEnvironment,
    PromotionStatus,
    ArtifactManifest,
    DeploymentRecord,
    CanaryEvaluationMetrics
)
from src.deployment.version_registry import VersionRegistry
from src.deployment.canary import CanaryController
from src.deployment.rollback import RollbackEngine
from src.deployment.deployment_ledger import DeploymentLedger
from src.deployment.exceptions import DeploymentGateError, UnauthorizedPromotionError

logger = logging.getLogger(__name__)

class EnvironmentPromotionPipeline:
    """Manages progression through TEST -> SANDBOX -> STAGING -> CANARY -> PRODUCTION."""

    def __init__(self, version_registry: VersionRegistry, ledger: DeploymentLedger):
        self.version_registry = version_registry
        self.ledger = ledger
        self.canary_controller = CanaryController()
        self.rollback_engine = RollbackEngine(version_registry)

    def promote_to_staging(self, manifest: ArtifactManifest, operator: str) -> DeploymentRecord:
        """Promotes validated artifact to STAGING after verifying test coverage & benchmark scores."""
        if manifest.security_test_pass_rate < 1.0:
            raise DeploymentGateError(f"Security test pass rate {manifest.security_test_pass_rate} < 100% required")

        if manifest.benchmark_score < 0.85:
            raise DeploymentGateError(f"Benchmark score {manifest.benchmark_score} < 0.85 required")

        self.version_registry.register_version(manifest)

        record = DeploymentRecord(
            deployment_id=str(uuid.uuid4()),
            version_id=manifest.version_id,
            target_env=TargetEnvironment.STAGING,
            promoted_by=operator,
            status=PromotionStatus.PROMOTED,
            manifest=manifest,
            timestamp=time.time(),
            notes="Promoted to STAGING after passing security and benchmark gates"
        )
        self.ledger.log_deployment(record)
        self.rollback_engine.record_deployment(record)
        return record

    def promote_to_production_canary(self, version_id: str, operator: str, human_approval_token: str) -> DeploymentRecord:
        """Promotes version to PRODUCTION_CANARY requiring explicit human authorization."""
        if not human_approval_token:
            raise UnauthorizedPromotionError("Promotion to production canary requires a valid human authorization token")

        manifest = self.version_registry.get_version(version_id)
        if not manifest:
            raise DeploymentGateError(f"Version {version_id} not registered in version catalog")

        record = DeploymentRecord(
            deployment_id=str(uuid.uuid4()),
            version_id=version_id,
            target_env=TargetEnvironment.PRODUCTION_CANARY,
            promoted_by=operator,
            status=PromotionStatus.IN_PROGRESS,
            manifest=manifest,
            timestamp=time.time(),
            notes=f"Canary initiated with authorization token {human_approval_token}"
        )
        self.ledger.log_deployment(record)
        return record

    def finalize_production_promotion(
        self,
        canary_record: DeploymentRecord,
        canary_metrics: CanaryEvaluationMetrics,
        operator: str
    ) -> DeploymentRecord:
        """Finalizes canary into full PRODUCTION or triggers automatic rollback on SLA breach."""
        if canary_metrics.sla_breached:
            self.rollback_engine.execute_rollback(reason="Canary SLA breached during evaluation", actor=operator)
            canary_record.status = PromotionStatus.ROLLED_BACK
            self.ledger.log_deployment(canary_record)
            raise DeploymentGateError("Canary metrics breached production SLA! Automatic rollback executed.")

        prod_record = DeploymentRecord(
            deployment_id=str(uuid.uuid4()),
            version_id=canary_record.version_id,
            target_env=TargetEnvironment.PRODUCTION,
            promoted_by=operator,
            status=PromotionStatus.PROMOTED,
            manifest=canary_record.manifest,
            canary_metrics=canary_metrics,
            timestamp=time.time(),
            notes="Canary passed all SLAs. Fully promoted to PRODUCTION."
        )
        self.ledger.log_deployment(prod_record)
        self.rollback_engine.record_deployment(prod_record)
        return prod_record

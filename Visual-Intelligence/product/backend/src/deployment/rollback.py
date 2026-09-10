"""
Phase 23 Deterministic Automated Rollback Engine.
"""
import logging
import time
from typing import Dict, Any, Optional
from src.deployment.deployment_models import TargetEnvironment, PromotionStatus, DeploymentRecord
from src.deployment.version_registry import VersionRegistry
from src.deployment.exceptions import RollbackFailedError

logger = logging.getLogger(__name__)

class RollbackEngine:
    """Restores the last known stable deployment manifest upon canary failure or emergency trigger."""

    def __init__(self, version_registry: VersionRegistry):
        self.version_registry = version_registry
        self._current_deployment: Optional[DeploymentRecord] = None
        self._last_stable_deployment: Optional[DeploymentRecord] = None

    def record_deployment(self, deployment: DeploymentRecord) -> None:
        if self._current_deployment and self._current_deployment.status == PromotionStatus.PROMOTED:
            self._last_stable_deployment = self._current_deployment
        self._current_deployment = deployment

    def execute_rollback(self, reason: str, actor: str = "AUTOMATED_CANARY_GUARD") -> Dict[str, Any]:
        """Rolls back to the previous stable release manifest."""
        if not self._last_stable_deployment:
            logger.error("Rollback failed: No previous stable deployment on record!")
            raise RollbackFailedError("Cannot rollback: No previous stable release available")

        target_version = self._last_stable_deployment.version_id
        manifest = self.version_registry.get_version(target_version)
        if not manifest:
            raise RollbackFailedError(f"Previous stable version {target_version} not found in registry")

        logger.warning(f"ROLLBACK INITIATED to version {target_version}. Reason: {reason}")

        if self._current_deployment:
            self._current_deployment.status = PromotionStatus.ROLLED_BACK
            self._current_deployment.notes = f"Rolled back to {target_version}: {reason}"

        return {
            "success": True,
            "restored_version": target_version,
            "manifest_hash": manifest.manifest_hash,
            "reason": reason,
            "actor": actor,
            "timestamp": time.time()
        }

"""
Phase 23 Deployment Audit and Promotion Ledger.
"""
import logging
import uuid
import time
from typing import List, Dict, Any
from src.deployment.deployment_models import DeploymentRecord

logger = logging.getLogger(__name__)

class DeploymentLedger:
    """Immutable audit trail of release promotions, approvals, and canary outcomes."""

    def __init__(self):
        self._records: List[DeploymentRecord] = []

    def log_deployment(self, record: DeploymentRecord) -> None:
        self._records.append(record)
        logger.info(f"Deployment Logged: {record.version_id} -> {record.target_env.value} [{record.status.value}] by {record.promoted_by}")

    def list_history(self) -> List[DeploymentRecord]:
        return list(self._records)

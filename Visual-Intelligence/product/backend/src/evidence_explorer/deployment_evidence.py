"""
Phase 25 Deployment Promotion & Canary Release Evidence Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DeploymentPromotionEvidence:
    deployment_id: str
    target_environment: str # STAGING, CANARY, PRODUCTION
    release_version: str
    manifest_hash: str
    operator_approver_id: str
    canary_duration_seconds: float
    slo_metrics_validated: bool
    status: str # PROMOTED, ROLLED_BACK

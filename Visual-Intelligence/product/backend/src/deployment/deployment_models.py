"""
Phase 23 Deployment Models, Canary Metrics, and Manifest Definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import hashlib
import json

class TargetEnvironment(str, Enum):
    TEST = "TEST"
    SANDBOX = "SANDBOX"
    STAGING = "STAGING"
    PRODUCTION_CANARY = "PRODUCTION_CANARY"
    PRODUCTION = "PRODUCTION"

class PromotionStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    PROMOTED = "PROMOTED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"

@dataclass
class ArtifactManifest:
    version_id: str
    git_commit_sha: str
    dependency_lock_hash: str
    config_fingerprint: str
    benchmark_score: float
    security_test_pass_rate: float
    created_at: float = field(default_factory=time.time)
    manifest_hash: str = ""

    def compute_hash(self) -> str:
        payload = json.dumps({
            "version_id": self.version_id,
            "git_commit_sha": self.git_commit_sha,
            "dependency_lock_hash": self.dependency_lock_hash,
            "config_fingerprint": self.config_fingerprint,
            "benchmark_score": self.benchmark_score,
            "security_test_pass_rate": self.security_test_pass_rate
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

@dataclass
class CanaryEvaluationMetrics:
    total_requests: int
    error_count: int
    error_rate: float
    p95_latency_ms: float
    visual_regression_score: float
    sla_breached: bool = False
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DeploymentRecord:
    deployment_id: str
    version_id: str
    target_env: TargetEnvironment
    promoted_by: str
    status: PromotionStatus
    manifest: ArtifactManifest
    canary_metrics: Optional[CanaryEvaluationMetrics] = None
    timestamp: float = field(default_factory=time.time)
    notes: str = ""

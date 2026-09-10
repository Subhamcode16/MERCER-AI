"""
Phase 24 Live Operations Models, Probe Results, and Evidence Record Definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import hashlib
import json

class LiveValidationMode(str, Enum):
    SIMULATED = "SIMULATED"
    SANDBOX = "SANDBOX"
    STAGING = "STAGING"
    CANARY = "CANARY"
    REAL_PROVIDER = "REAL_PROVIDER"
    PRODUCTION = "PRODUCTION"

class ProbeStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DENIED = "DENIED"
    NOT_VALIDATED = "NOT_VALIDATED"
    QUARANTINED = "QUARANTINED"

@dataclass
class ProbeResult:
    probe_id: str
    target_component: str
    status: ProbeStatus
    latency_ms: float
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

@dataclass
class LiveEvidenceRecord:
    evidence_id: str
    phase: str = "24"
    probe_id: str = ""
    environment: LiveValidationMode = LiveValidationMode.SANDBOX
    timestamp: float = field(default_factory=time.time)
    correlation_id: str = ""
    tenant_id: str = ""
    client_id: str = ""
    component: str = ""
    provider: str = ""
    model_or_version: str = ""
    operation: str = ""
    input_hash: str = ""
    output_hash: str = ""
    status: ProbeStatus = ProbeStatus.PASS
    failure_class: Optional[str] = None
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    authorization_token_id: Optional[str] = None
    policy_decision: str = "PERMITTED"
    artifact_hash: Optional[str] = None
    lineage_hash: Optional[str] = None
    rollback_state: Optional[str] = None
    operator_reference: Optional[str] = None
    record_hash: str = ""

    def compute_hash(self) -> str:
        payload = json.dumps({
            "evidence_id": self.evidence_id,
            "probe_id": self.probe_id,
            "environment": self.environment.value,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "tenant_id": self.tenant_id,
            "client_id": self.client_id,
            "component": self.component,
            "provider": self.provider,
            "model_or_version": self.model_or_version,
            "operation": self.operation,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "status": self.status.value,
            "latency_ms": round(self.latency_ms, 2),
            "cost_usd": round(self.cost_usd, 6),
            "authorization_token_id": self.authorization_token_id,
            "policy_decision": self.policy_decision,
            "artifact_hash": self.artifact_hash,
            "lineage_hash": self.lineage_hash
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

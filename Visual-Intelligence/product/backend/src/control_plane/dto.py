"""
Phase 25 Safe Projection DTOs.
Strictly sanitizes internal models, excluding secrets, credentials, internal pointers, and CoT traces.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
import re
from src.control_plane.exceptions import DTOSerializationError

ALLOWED_TOKEN_FIELDS = {"execution_token_id", "token_id", "brand_tokens", "total_input_tokens", "total_output_tokens"}

PROHIBITED_FIELD_PATTERNS = [
    re.compile(r".*(password|secret|api[-_]?key|credential|bearer|private[-_]?key|chain[-_]?of[-_]?thought|internal_reasoning).*", re.IGNORECASE),
    re.compile(r"^(token|auth[-_]?token|bearer[-_]?token|access[-_]?token|session[-_]?token)$", re.IGNORECASE)
]

def sanitize_payload(obj: Any) -> Any:
    """Recursively validates and sanitizes payloads to ensure zero secret / CoT leakage."""
    if isinstance(obj, dict):
        clean = {}
        for k, v in obj.items():
            if k not in ALLOWED_TOKEN_FIELDS and any(p.match(k) for p in PROHIBITED_FIELD_PATTERNS):
                raise DTOSerializationError(f"Prohibited sensitive field '{k}' detected in outgoing DTO projection.")
            clean[k] = sanitize_payload(v)
        return clean
    elif isinstance(obj, list):
        return [sanitize_payload(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return sanitize_payload(asdict(obj) if hasattr(obj, "_asdict") else obj.__dict__)
    return obj


class DTOSanitizer:
    """Sanitizer class for scrubbing sensitive data from payloads and DTO projections."""

    @staticmethod
    def sanitize(obj: Any) -> Any:
        if isinstance(obj, dict):
            clean = {}
            for k, v in obj.items():
                if k in ALLOWED_TOKEN_FIELDS or not any(p.match(k) for p in PROHIBITED_FIELD_PATTERNS):
                    clean[k] = DTOSanitizer.sanitize(v)
            return clean
        elif isinstance(obj, list):
            return [DTOSanitizer.sanitize(item) for item in obj]
        elif hasattr(obj, "__dict__"):
            return DTOSanitizer.sanitize(asdict(obj) if hasattr(obj, "_asdict") else obj.__dict__)
        return obj


@dataclass
class CampaignSummaryDTO:
    campaign_id: str
    tenant_id: str
    client_id: str
    name: str
    state: str
    version: int
    progress_pct: float
    approval_required: bool
    budget_allocated_usd: float
    budget_spent_usd: float
    created_at: float
    updated_at: float

@dataclass
class DeliverableSummaryDTO:
    deliverable_id: str
    campaign_id: str
    title: str
    deliverable_type: str # IMAGE, COPY, STRATEGY, VIDEO
    state: str
    artifact_id: Optional[str] = None
    lineage_verified: bool = False
    critique_score: Optional[float] = None
    quarantined: bool = False

@dataclass
class ApprovalRequestDTO:
    approval_id: str
    campaign_id: str
    tenant_id: str
    client_id: str
    requested_operation: str
    scope: str
    risk_level: str
    requester_role: str
    evidence_id: str
    created_at: float
    expires_at: float
    status: str # PENDING, APPROVED, REJECTED, EXPIRED, REVOKED
    version: int

@dataclass
class ReliabilityStatusDTO:
    overall_health: str # HEALTHY, DEGRADED, CRITICAL
    availability_slo_pct: float
    observed_availability_pct: float
    p95_latency_ms: float
    error_budget_burn_pct: float
    active_circuit_breakers: List[str]
    open_incidents_count: int

@dataclass
class VisualObservatoryDTO:
    total_artifacts: int
    lineage_valid_pct: float
    average_quality_score: float
    active_quarantined_count: int
    latest_benchmark_version: str
    drift_status: str # STABLE, DRIFT_DETECTED, ELEVATED

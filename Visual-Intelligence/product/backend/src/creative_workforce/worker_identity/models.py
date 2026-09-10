"""
Phase 26 Worker Identity Models & Enums.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timezone
import uuid


class WorkerStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    RESTRICTED = "RESTRICTED"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class WorkerRole(str, Enum):
    STRATEGY_DIRECTOR = "STRATEGY_DIRECTOR"
    BRAND_INTELLIGENCE = "BRAND_INTELLIGENCE"
    CREATIVE_DIRECTOR = "CREATIVE_DIRECTOR"
    ART_DIRECTION = "ART_DIRECTION"
    VISUAL_DNA_SPECIALIST = "VISUAL_DNA_SPECIALIST"
    CAMPAIGN_PLANNER = "CAMPAIGN_PLANNER"
    COPY_STRATEGIST = "COPY_STRATEGIST"
    CONTENT_PRODUCER = "CONTENT_PRODUCER"
    TREND_RESEARCHER = "TREND_RESEARCHER"
    QUALITY_REVIEWER = "QUALITY_REVIEWER"
    PERFORMANCE_ANALYST = "PERFORMANCE_ANALYST"
    CLIENT_COORDINATOR = "CLIENT_COORDINATOR"
    STUDIO_OPERATOR = "STUDIO_OPERATOR"


@dataclass
class RoleIdentity:
    role_id: str
    role_name: str
    description: str
    default_capabilities: List[str] = field(default_factory=list)


@dataclass
class CapabilityIdentity:
    profile_id: str
    allowed_capabilities: Set[str] = field(default_factory=set)
    forbidden_capabilities: Set[str] = field(default_factory=set)


@dataclass
class ExecutionIdentity:
    execution_id: str
    runtime_type: str = "SANDBOXED_WORKER"
    execution_authority: str = "NONE"
    approval_authority: str = "NONE"


@dataclass
class ProvenanceIdentity:
    worker_id: str
    version: str
    model_provider: str
    model_name: str
    model_version: str


@dataclass
class WorkerIdentity:
    worker_id: str
    tenant_id: str
    organization_id: str
    name: str
    role_id: str
    description: str
    status: WorkerStatus = WorkerStatus.DRAFT
    version: str = "1.0.0"
    owner: str = "SYSTEM"
    memory_policy_id: str = "STANDARD_SCOPED"
    capability_profile_id: str = "DEFAULT"
    skill_profile_id: str = "DEFAULT"
    model_policy_id: str = "DEFAULT"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

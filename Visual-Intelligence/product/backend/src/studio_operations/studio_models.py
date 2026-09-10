"""
Phase 15 Studio Operations Immutable Data Models.
Establishes strong types, validation guards, and domain models for the studio control plane.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ClientContextViolation, DeliverableStateViolation

class OperationalPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class CampaignCadence(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"
    MONTHLY = "MONTHLY"

class DeliverableType(str, Enum):
    SOCIAL_POST = "SOCIAL_POST"
    HERO_VISUAL = "HERO_VISUAL"
    CAMPAIGN_BRIEF = "CAMPAIGN_BRIEF"
    CONTENT_CALENDAR = "CONTENT_CALENDAR"
    TREND_REPORT = "TREND_REPORT"
    VIDEO_SHORT = "VIDEO_SHORT"
    BRAND_ASSET = "BRAND_ASSET"

class DeliverableStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    DRAFT = "DRAFT"
    CRITIQUE = "CRITIQUE"
    REVISION = "REVISION"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    READY_FOR_EXECUTION = "READY_FOR_EXECUTION"
    EXECUTED = "EXECUTED"
    OBSERVED = "OBSERVED"
    LEARNED = "LEARNED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class CampaignStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    RESUMED = "RESUMED"

# Valid deliverable status state machine transitions
VALID_DELIVERABLE_TRANSITIONS = {
    DeliverableStatus.PLANNED: {DeliverableStatus.IN_PROGRESS, DeliverableStatus.REJECTED},
    DeliverableStatus.IN_PROGRESS: {DeliverableStatus.DRAFT, DeliverableStatus.REJECTED},
    DeliverableStatus.DRAFT: {DeliverableStatus.CRITIQUE, DeliverableStatus.REJECTED},
    DeliverableStatus.CRITIQUE: {DeliverableStatus.REVISION, DeliverableStatus.REVIEW, DeliverableStatus.REJECTED},
    DeliverableStatus.REVISION: {DeliverableStatus.CRITIQUE, DeliverableStatus.DRAFT, DeliverableStatus.REJECTED},
    DeliverableStatus.REVIEW: {DeliverableStatus.APPROVED, DeliverableStatus.REVISION, DeliverableStatus.REJECTED},
    DeliverableStatus.APPROVED: {DeliverableStatus.READY_FOR_EXECUTION, DeliverableStatus.REJECTED},
    DeliverableStatus.READY_FOR_EXECUTION: {DeliverableStatus.EXECUTED, DeliverableStatus.EXPIRED, DeliverableStatus.REJECTED},
    DeliverableStatus.EXECUTED: {DeliverableStatus.OBSERVED},
    DeliverableStatus.OBSERVED: {DeliverableStatus.LEARNED},
    DeliverableStatus.LEARNED: set(),
    DeliverableStatus.REJECTED: set(),
    DeliverableStatus.EXPIRED: set(),
}

@dataclass(frozen=True)
class StudioClient:
    client_id: str
    name: str
    industry: str
    status: str = "ACTIVE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.client_id or not isinstance(self.client_id, str) or not self.client_id.strip():
            raise ClientContextViolation("client_id cannot be empty or non-string.")
        if not self.name or not isinstance(self.name, str) or not self.name.strip():
            raise ClientContextViolation("Client name cannot be empty or non-string.")

@dataclass(frozen=True)
class StudioBrand:
    brand_id: str
    client_id: str
    brand_name: str
    visual_dna_summary: Dict[str, Any] = field(default_factory=dict)
    tone_of_voice: str = "Modern, Professional"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.brand_id or not self.brand_id.strip():
            raise ClientContextViolation("brand_id cannot be empty.")
        if not self.client_id or not self.client_id.strip():
            raise ClientContextViolation("client_id cannot be empty.")

@dataclass(frozen=True)
class ClientOperatingPolicy:
    policy_id: str
    client_id: str
    max_revisions_override: int = 3
    require_human_approval: bool = True
    allowed_platforms: List[str] = field(default_factory=lambda: ["instagram", "twitter", "linkedin", "tiktok"])
    allowed_capabilities: List[str] = field(default_factory=lambda: ["draft_content", "review_content", "schedule_post"])
    escalation_threshold: int = 3
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.policy_id or not self.client_id:
            raise ClientContextViolation("policy_id and client_id are required.")

@dataclass
class Campaign:
    campaign_id: str
    client_id: str
    brand_id: str
    title: str
    objective: str
    cadence: CampaignCadence = CampaignCadence.WEEKLY
    priority: OperationalPriority = OperationalPriority.MEDIUM
    status: CampaignStatus = CampaignStatus.PLANNED
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.campaign_id or not self.client_id or not self.brand_id:
            raise ClientContextViolation("campaign_id, client_id, and brand_id are required.")

@dataclass
class Workstream:
    workstream_id: str
    campaign_id: str
    client_id: str
    name: str
    workstream_type: str = "social_content"
    status: str = "ACTIVE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.workstream_id or not self.campaign_id or not self.client_id:
            raise ClientContextViolation("workstream_id, campaign_id, and client_id are required.")

@dataclass
class Deliverable:
    deliverable_id: str
    workstream_id: str
    campaign_id: str
    client_id: str
    title: str
    deliverable_type: DeliverableType = DeliverableType.SOCIAL_POST
    status: DeliverableStatus = DeliverableStatus.PLANNED
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    revision_count: int = 0
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def transition_to(self, new_status: DeliverableStatus) -> None:
        """Enforces finite state machine transition validation."""
        valid_next = VALID_DELIVERABLE_TRANSITIONS.get(self.status, set())
        if new_status not in valid_next:
            raise DeliverableStateViolation(
                f"Invalid deliverable state transition from {self.status.value} to {new_status.value} for deliverable '{self.deliverable_id}'."
            )
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc).isoformat()

@dataclass
class StudioCycle:
    cycle_id: str
    campaign_id: str
    client_id: str
    cycle_number: int
    cycle_type: str = "WEEKLY"
    status: str = "IN_PROGRESS"
    start_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    end_time: Optional[str] = None

@dataclass
class OperationalObjective:
    objective_id: str
    client_id: str
    description: str
    target_metrics: Dict[str, Any] = field(default_factory=dict)
    status: str = "ACTIVE"

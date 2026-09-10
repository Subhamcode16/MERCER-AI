"""
Phase 12 Coordination Immutable Models & Data Contracts.

Defines data structures for Multi-Mission Registration, Resource Descriptors,
Leases, Conflict Records, Arbitration Decisions, and Coordination Budgets.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Set, Dict, Any, Optional

from .exceptions import CoordinationPolicyViolation


class MissionPriority(Enum):
    """Enumeration of mission priorities for coordination arbitration."""
    SYSTEM_CRITICAL = 1
    USER_BLOCKING = 2
    HIGH = 3
    NORMAL = 4
    LOW = 5
    BACKGROUND = 6


@dataclass(frozen=True)
class ResourceDescriptor:
    """Descriptor for a logical shared resource (staff slot, API quota, rate limit bucket)."""
    resource_id: str
    resource_type: str  # e.g., "STAFF_SLOT", "MODEL_TOKEN_QUOTA", "SOCIAL_ACCOUNT", "CONTENT_CALENDAR"
    capacity: int
    scope_string: str
    owner_mission_id: Optional[str] = None
    lease_duration_seconds: int = 300
    risk_class: str = "NORMAL"

    def __post_init__(self):
        if not self.resource_id or type(self.resource_id) is not str:
            raise CoordinationPolicyViolation("resource_id must be a non-empty string.")
        if type(self.capacity) is bool or not isinstance(self.capacity, int) or self.capacity <= 0:
            raise CoordinationPolicyViolation("capacity must be a positive integer.")
        if type(self.lease_duration_seconds) is bool or not isinstance(self.lease_duration_seconds, int) or self.lease_duration_seconds <= 0:
            raise CoordinationPolicyViolation("lease_duration_seconds must be a positive integer.")


@dataclass(frozen=True)
class ResourceRequest:
    """Request by a mission for logical resource allocation."""
    request_id: str
    mission_id: str
    resource_id: str
    quantity: int = 1
    requested_duration_seconds: int = 300
    exclusive: bool = False

    def __post_init__(self):
        if not self.request_id or type(self.request_id) is not str:
            raise CoordinationPolicyViolation("request_id must be a non-empty string.")
        if not self.mission_id or type(self.mission_id) is not str:
            raise CoordinationPolicyViolation("mission_id must be a non-empty string.")
        if type(self.quantity) is bool or not isinstance(self.quantity, int) or self.quantity <= 0:
            raise CoordinationPolicyViolation("quantity must be a positive integer.")


@dataclass(frozen=True)
class ResourceLease:
    """Cryptographically verifiable short-lived resource lease token."""
    lease_id: str
    mission_id: str
    resource_id: str
    quantity: int
    issued_at: str
    expires_at: str
    nonce: str
    digest: str = ""

    def is_expired(self, current_time: Optional[datetime] = None) -> bool:
        now = current_time or datetime.now(timezone.utc)
        exp = datetime.fromisoformat(self.expires_at)
        return now >= exp


@dataclass(frozen=True)
class CoordinationMission:
    """Container for an admitted mission inside the Multi-Mission Coordination Registry."""
    mission_id: str
    priority: MissionPriority
    admission_timestamp: datetime
    requested_resources: List[ResourceRequest] = field(default_factory=list)
    active_leases: List[ResourceLease] = field(default_factory=list)
    status: str = "ADMITTED"  # ADMITTED, RUNNING, PAUSED, PREEMPTED, ESCALATED, COMPLETED, CANCELLED
    aging_boost: int = 0      # Dynamic priority aging boost counter

    def __post_init__(self):
        if not self.mission_id or type(self.mission_id) is not str:
            raise CoordinationPolicyViolation("mission_id must be a non-empty string.")
        if not isinstance(self.priority, MissionPriority):
            raise CoordinationPolicyViolation("priority must be a valid MissionPriority enum instance.")


@dataclass(frozen=True)
class ConflictRecord:
    """Description of a detected resource or mutation collision across missions."""
    conflict_id: str
    mission_a_id: str
    mission_b_id: str
    resource_id: str
    severity: str  # INFO, WARNING, BLOCKING
    description: str
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class ArbitrationDecision:
    """Result of deterministic arbitration across competing mission resource requests."""
    decision_id: str
    granted_mission_id: Optional[str]
    deferred_mission_ids: List[str]
    reason_code: str
    granted_leases: List[ResourceLease] = field(default_factory=list)
    conflicts_detected: List[ConflictRecord] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class CoordinationBudget:
    """Global system-wide resource limits across all concurrent missions."""
    global_max_tokens: int = 2000000
    global_max_concurrent_missions: int = 20
    global_max_concurrent_staff_tasks: int = 15
    global_max_execution_slots: int = 10
    global_max_external_requests_per_min: int = 200

    def __post_init__(self):
        for attr in ['global_max_tokens', 'global_max_concurrent_missions',
                     'global_max_concurrent_staff_tasks', 'global_max_execution_slots',
                     'global_max_external_requests_per_min']:
            val = getattr(self, attr)
            if type(val) is bool or not isinstance(val, int) or val <= 0:
                raise CoordinationPolicyViolation(f"Global budget '{attr}' must be a positive integer.")


@dataclass(frozen=True)
class CoordinationOutcome:
    """Summary of multi-mission coordination execution."""
    admitted_missions: int
    completed_missions: int
    preempted_missions: int
    resolved_conflicts: int
    total_granted_leases: int
    global_tokens_consumed: int

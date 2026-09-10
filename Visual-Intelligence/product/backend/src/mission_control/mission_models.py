"""
Phase 11 Mission Control Data Models.

Defines immutable models for Mission, MissionObjective, MissionConstraints, MissionBudget,
MissionAuthorizationContext, and MissionOutcome with strict input validation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Set, Optional, Dict, Any

from .exceptions import MissionPolicyViolationError


@dataclass(frozen=True)
class MissionObjective:
    """Represents a high-level user operational objective."""
    objective_id: str
    title: str
    description: str
    target_outcomes: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.objective_id or not isinstance(self.objective_id, str):
            raise MissionPolicyViolationError("Mission objective_id must be a non-empty string.")
        if not self.title or not isinstance(self.title, str):
            raise MissionPolicyViolationError("Mission title must be a non-empty string.")


@dataclass(frozen=True)
class MissionBudget:
    """Resource and token caps for a mission."""
    max_runtime_seconds: int = 86400
    max_tasks: int = 50
    max_retries: int = 10
    max_executions: int = 20
    max_generated_assets: int = 30
    max_external_requests: int = 100
    token_budget: int = 500000

    def __post_init__(self):
        # Strict type and non-negative checks
        for attr in ['max_runtime_seconds', 'max_tasks', 'max_retries', 'max_executions',
                     'max_generated_assets', 'max_external_requests', 'token_budget']:
            val = getattr(self, attr)
            if type(val) is bool or not isinstance(val, int) or val < 0:
                raise MissionPolicyViolationError(f"Budget parameter '{attr}' must be a non-negative integer.")


@dataclass(frozen=True)
class MissionConstraints:
    """Security boundaries and allowed operational capabilities/resources."""
    allowed_capabilities: Set[str] = field(default_factory=set)
    allowed_resources: Set[str] = field(default_factory=set)
    max_dag_depth: int = 10
    escalation_policy: str = "HUMAN_REVIEW_REQUIRED"
    requires_explicit_authorization: bool = True

    def __post_init__(self):
        if not isinstance(self.allowed_capabilities, set):
            raise MissionPolicyViolationError("allowed_capabilities must be a set.")
        if not isinstance(self.allowed_resources, set):
            raise MissionPolicyViolationError("allowed_resources must be a set.")

        # Invariant: Disallow wildcard '*' in capabilities or resources to prevent privilege amplification
        if "*" in self.allowed_capabilities or "ALL" in self.allowed_capabilities:
            raise MissionPolicyViolationError("Unrestricted capability wildcard ('*' or 'ALL') is prohibited.")
        if "*" in self.allowed_resources or "ALL" in self.allowed_resources:
            raise MissionPolicyViolationError("Unrestricted resource scope wildcard ('*' or 'ALL') is prohibited.")

        if type(self.max_dag_depth) is bool or not isinstance(self.max_dag_depth, int) or self.max_dag_depth <= 0 or self.max_dag_depth > 20:
            raise MissionPolicyViolationError("max_dag_depth must be an integer between 1 and 20.")


@dataclass(frozen=True)
class MissionAuthorizationContext:
    """Context holding Phase 10 external authorization references."""
    authorization_token_id: Optional[str] = None
    authorized_by: Optional[str] = None
    expires_at: Optional[datetime] = None
    granted_capabilities: Set[str] = field(default_factory=set)
    granted_resources: Set[str] = field(default_factory=set)

    def is_valid(self, current_time: Optional[datetime] = None) -> bool:
        if not self.authorization_token_id:
            return False
        now = current_time or datetime.now(timezone.utc)
        if self.expires_at and now > self.expires_at:
            return False
        return True


@dataclass(frozen=True)
class MissionOutcome:
    """Final outcome summary of a completed or failed mission."""
    mission_id: str
    status: str
    completed_tasks: int
    total_tasks: int
    executed_actions: int
    tokens_consumed: int
    error_summary: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Mission:
    """Root Mission object managing operational state and boundaries."""
    mission_id: str
    objective: MissionObjective
    constraints: MissionConstraints
    budget: MissionBudget
    authorization_context: MissionAuthorizationContext = field(default_factory=MissionAuthorizationContext)
    state: str = "PLANNED"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.mission_id or not isinstance(self.mission_id, str):
            raise MissionPolicyViolationError("mission_id must be a non-empty string.")

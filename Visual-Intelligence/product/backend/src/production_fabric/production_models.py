"""
Phase 17 Production Fabric Immutable Data Models.
Establishes strong types, contracts, and validation guards for production intake,
queue items, runs, objectives, checkpoints, and outcomes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from src.production_fabric.exceptions import WorkIntakeError, ProductionStateViolation, CrossClientFabricViolation

class ProductionState(str, Enum):
    PENDING = "PENDING"
    ADMITTED = "ADMITTED"
    IN_PRODUCTION = "IN_PRODUCTION"
    CRITIQUE = "CRITIQUE"
    REVIEW = "REVIEW"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    READY_FOR_EXECUTION = "READY_FOR_EXECUTION"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    LEARNING = "LEARNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    RECOVERING = "RECOVERING"

class ProductionPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

VALID_PRODUCTION_STATE_TRANSITIONS: Dict[ProductionState, Set[ProductionState]] = {
    ProductionState.PENDING: {ProductionState.ADMITTED, ProductionState.FAILED},
    ProductionState.ADMITTED: {ProductionState.IN_PRODUCTION, ProductionState.BLOCKED, ProductionState.FAILED},
    ProductionState.IN_PRODUCTION: {ProductionState.CRITIQUE, ProductionState.BLOCKED, ProductionState.FAILED},
    ProductionState.CRITIQUE: {ProductionState.REVIEW, ProductionState.IN_PRODUCTION, ProductionState.FAILED},
    ProductionState.REVIEW: {ProductionState.AWAITING_APPROVAL, ProductionState.IN_PRODUCTION, ProductionState.FAILED},
    ProductionState.AWAITING_APPROVAL: {ProductionState.APPROVED, ProductionState.IN_PRODUCTION, ProductionState.FAILED, ProductionState.BLOCKED},
    ProductionState.APPROVED: {ProductionState.READY_FOR_EXECUTION, ProductionState.FAILED},
    ProductionState.READY_FOR_EXECUTION: {ProductionState.EXECUTING, ProductionState.FAILED},
    ProductionState.EXECUTING: {ProductionState.OBSERVING, ProductionState.FAILED, ProductionState.RECOVERING},
    ProductionState.OBSERVING: {ProductionState.LEARNING, ProductionState.FAILED},
    ProductionState.LEARNING: {ProductionState.COMPLETED, ProductionState.FAILED},
    ProductionState.COMPLETED: set(),
    ProductionState.FAILED: {ProductionState.RECOVERING},
    ProductionState.BLOCKED: {ProductionState.ADMITTED, ProductionState.IN_PRODUCTION, ProductionState.FAILED},
    ProductionState.RECOVERING: {ProductionState.ADMITTED, ProductionState.IN_PRODUCTION, ProductionState.FAILED},
}

@dataclass(frozen=True)
class ProductionRequest:
    request_id: str
    client_id: str
    campaign_id: str
    brand_id: str
    title: str
    description: str = ""
    deliverable_type: str = "SOCIAL_POST"
    priority: ProductionPriority = ProductionPriority.MEDIUM
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.request_id or not isinstance(self.request_id, str) or not self.request_id.strip():
            raise WorkIntakeError("request_id must be a non-empty string.")
        if not self.client_id or not isinstance(self.client_id, str) or not self.client_id.strip():
            raise CrossClientFabricViolation("client_id must be a non-empty string.")
        if not self.campaign_id or not isinstance(self.campaign_id, str) or not self.campaign_id.strip():
            raise WorkIntakeError("campaign_id must be a non-empty string.")
        if not self.brand_id or not isinstance(self.brand_id, str) or not self.brand_id.strip():
            raise WorkIntakeError("brand_id must be a non-empty string.")

@dataclass(frozen=True)
class ProductionDependency:
    dependency_id: str
    parent_item_id: str
    child_item_id: str
    dependency_type: str = "PREREQUISITE"

@dataclass(frozen=True)
class ProductionObjective:
    objective_id: str
    client_id: str
    campaign_id: str
    target_deliverables_count: int
    max_budget_units: float = 100.0
    status: str = "ACTIVE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.objective_id or not self.objective_id.strip():
            raise WorkIntakeError("objective_id cannot be empty.")
        if not self.client_id or not self.client_id.strip():
            raise CrossClientFabricViolation("client_id cannot be empty.")
        if self.max_budget_units < 0:
            raise WorkIntakeError("max_budget_units cannot be negative.")

@dataclass
class ProductionWorkItem:
    item_id: str
    request_id: str
    client_id: str
    campaign_id: str
    workstream_id: str
    deliverable_id: str
    title: str
    priority: ProductionPriority = ProductionPriority.MEDIUM
    state: ProductionState = ProductionState.PENDING
    assigned_staff_ids: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.item_id or not self.item_id.strip():
            raise WorkIntakeError("item_id cannot be empty.")
        if not self.client_id or not self.client_id.strip():
            raise CrossClientFabricViolation("client_id cannot be empty.")

    def transition_to(self, new_state: ProductionState) -> None:
        valid_next = VALID_PRODUCTION_STATE_TRANSITIONS.get(self.state, set())
        if new_state not in valid_next:
            raise ProductionStateViolation(
                f"Invalid production state transition from {self.state.value} to {new_state.value} for item '{self.item_id}'."
            )
        self.state = new_state
        self.updated_at = datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class ProductionCheckpoint:
    checkpoint_id: str
    run_id: str
    client_id: str
    item_id: str
    state_snapshot: ProductionState
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ProductionRun:
    run_id: str
    client_id: str
    campaign_id: str
    items: List[ProductionWorkItem] = field(default_factory=list)
    status: str = "RUNNING"
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass(frozen=True)
class ProductionOutcome:
    outcome_id: str
    client_id: str
    campaign_id: str
    deliverable_id: str
    provider: str
    external_post_id: str
    reach: int
    engagement_rate: float
    provenance: str = "UNTRUSTED_EXTERNAL_OBSERVATION"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass(frozen=True)
class ProductionHealth:
    active_clients: int
    active_campaigns: int
    pending_items: int
    blocked_items: int
    executing_items: int
    recovery_count: int
    status: str = "HEALTHY"

@dataclass
class ProductionCycle:
    cycle_id: str
    client_id: str
    name: str
    cadence: str = "WEEKLY"
    current_run_id: Optional[str] = None
    status: str = "ACTIVE"

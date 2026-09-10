"""
Phase 23 Production Runtime Models and State Definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import uuid

class ProcessStatus(str, Enum):
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    STOPPED = "STOPPED"
    CRASHED = "CRASHED"

class WorkerStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    PAUSED = "PAUSED"
    TERMINATED = "TERMINATED"

class QueuePriority(int, Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

class WorkflowOperationalState(str, Enum):
    CREATED = "CREATED"
    ADMITTED = "ADMITTED"
    RUNNING = "RUNNING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    LEARNING = "LEARNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"
    BLOCKED = "BLOCKED"
    ESCALATED = "ESCALATED"
    CANCELLED = "CANCELLED"

# Permitted state transitions for the recoverable state machine
VALID_STATE_TRANSITIONS = {
    WorkflowOperationalState.CREATED: {WorkflowOperationalState.ADMITTED, WorkflowOperationalState.CANCELLED, WorkflowOperationalState.FAILED},
    WorkflowOperationalState.ADMITTED: {WorkflowOperationalState.RUNNING, WorkflowOperationalState.WAITING_FOR_APPROVAL, WorkflowOperationalState.FAILED},
    WorkflowOperationalState.RUNNING: {WorkflowOperationalState.WAITING_FOR_APPROVAL, WorkflowOperationalState.EXECUTING, WorkflowOperationalState.COMPLETED, WorkflowOperationalState.FAILED, WorkflowOperationalState.RECOVERING},
    WorkflowOperationalState.WAITING_FOR_APPROVAL: {WorkflowOperationalState.APPROVED, WorkflowOperationalState.BLOCKED, WorkflowOperationalState.ESCALATED, WorkflowOperationalState.CANCELLED},
    WorkflowOperationalState.APPROVED: {WorkflowOperationalState.EXECUTING, WorkflowOperationalState.BLOCKED, WorkflowOperationalState.FAILED},
    WorkflowOperationalState.EXECUTING: {WorkflowOperationalState.OBSERVING, WorkflowOperationalState.COMPLETED, WorkflowOperationalState.FAILED, WorkflowOperationalState.RECOVERING},
    WorkflowOperationalState.OBSERVING: {WorkflowOperationalState.LEARNING, WorkflowOperationalState.COMPLETED, WorkflowOperationalState.FAILED},
    WorkflowOperationalState.LEARNING: {WorkflowOperationalState.COMPLETED, WorkflowOperationalState.FAILED},
    WorkflowOperationalState.FAILED: {WorkflowOperationalState.RECOVERING, WorkflowOperationalState.BLOCKED, WorkflowOperationalState.ESCALATED},
    WorkflowOperationalState.RECOVERING: {WorkflowOperationalState.BLOCKED, WorkflowOperationalState.WAITING_FOR_APPROVAL, WorkflowOperationalState.RUNNING, WorkflowOperationalState.COMPLETED, WorkflowOperationalState.FAILED},
    WorkflowOperationalState.BLOCKED: {WorkflowOperationalState.WAITING_FOR_APPROVAL, WorkflowOperationalState.ESCALATED, WorkflowOperationalState.CANCELLED},
    WorkflowOperationalState.ESCALATED: {WorkflowOperationalState.WAITING_FOR_APPROVAL, WorkflowOperationalState.CANCELLED},
    WorkflowOperationalState.COMPLETED: set(),
    WorkflowOperationalState.CANCELLED: set(),
}

@dataclass
class RuntimeTask:
    task_id: str
    tenant_id: str
    client_id: str
    campaign_id: str
    mission_id: str
    action_name: str
    payload: Dict[str, Any]
    priority: QueuePriority = QueuePriority.NORMAL
    max_retries: int = 3
    retry_count: int = 0
    created_at: float = field(default_factory=time.time)
    timeout_seconds: float = 60.0
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_mutation: bool = False
    requires_authorization: bool = False
    authorization_token_id: Optional[str] = None

@dataclass
class WorkerDescriptor:
    worker_id: str
    status: WorkerStatus = WorkerStatus.IDLE
    current_task_id: Optional[str] = None
    tasks_processed: int = 0
    error_count: int = 0
    last_heartbeat: float = field(default_factory=time.time)
    tenant_id: Optional[str] = None

@dataclass
class RuntimeStateSnapshot:
    process_id: int
    process_status: ProcessStatus
    uptime_seconds: float
    active_workers: int
    idle_workers: int
    queue_depth: int
    dead_letter_depth: int
    total_tasks_completed: int
    total_tasks_failed: int
    active_tenants: List[str]
    timestamp: float = field(default_factory=time.time)

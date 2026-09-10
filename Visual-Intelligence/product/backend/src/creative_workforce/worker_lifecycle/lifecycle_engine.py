"""
Phase 26 Worker Lifecycle Engine.
"""
from typing import Dict, Optional
from datetime import datetime, timezone
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus


VALID_TRANSITIONS: Dict[WorkerStatus, Set_of_statuses := set] = {
    WorkerStatus.DRAFT: {WorkerStatus.ACTIVE, WorkerStatus.RETIRED},
    WorkerStatus.ACTIVE: {WorkerStatus.PAUSED, WorkerStatus.RESTRICTED, WorkerStatus.SUSPENDED, WorkerStatus.RETIRED},
    WorkerStatus.PAUSED: {WorkerStatus.ACTIVE, WorkerStatus.SUSPENDED, WorkerStatus.RETIRED},
    WorkerStatus.RESTRICTED: {WorkerStatus.ACTIVE, WorkerStatus.SUSPENDED, WorkerStatus.RETIRED},
    WorkerStatus.SUSPENDED: {WorkerStatus.RESTRICTED, WorkerStatus.RETIRED},  # Cannot return directly to ACTIVE without review
    WorkerStatus.RETIRED: set(),  # Terminal state, preserves attribution
}


class WorkerLifecycleError(Exception):
    pass


class WorkerLifecycleManager:
    """Manages state transitions and operational checks for workers."""

    @staticmethod
    def transition(worker: WorkerIdentity, target_status: WorkerStatus, reason: str = "") -> WorkerIdentity:
        allowed_targets = VALID_TRANSITIONS.get(worker.status, set())
        if target_status not in allowed_targets:
            raise WorkerLifecycleError(
                f"Invalid status transition from {worker.status.value} to {target_status.value}. Reason: {reason}"
            )
        
        worker.status = target_status
        worker.updated_at = datetime.now(timezone.utc).isoformat()
        worker.metadata["last_transition_reason"] = reason
        return worker

    @staticmethod
    def assert_executable(worker: WorkerIdentity) -> None:
        """Throws WorkerLifecycleError if worker is not in an executable state."""
        if worker.status != WorkerStatus.ACTIVE:
            raise WorkerLifecycleError(
                f"Worker '{worker.worker_id}' is in non-executable state '{worker.status.value}'"
            )

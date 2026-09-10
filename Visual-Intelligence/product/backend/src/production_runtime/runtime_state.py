"""
Phase 23 Runtime Operational State Machine and State Persistence.
"""
import logging
import time
from typing import Dict, Any, Optional, Set
from src.production_runtime.runtime_models import (
    WorkflowOperationalState,
    VALID_STATE_TRANSITIONS
)
from src.production_runtime.exceptions import InvalidStateTransitionError

logger = logging.getLogger(__name__)

class WorkflowStateRecord:
    def __init__(self, workflow_id: str, tenant_id: str, client_id: str, initial_state: WorkflowOperationalState = WorkflowOperationalState.CREATED):
        self.workflow_id = workflow_id
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.current_state = initial_state
        self.history: list[dict[str, Any]] = [{
            "from_state": None,
            "to_state": initial_state.value,
            "timestamp": time.time(),
            "reason": "INITIAL_CREATION"
        }]
        self.authorization_ref: Optional[str] = None
        self.is_recovering: bool = False
        self.checkpoint_hash: Optional[str] = None
        self.metadata: Dict[str, Any] = {}

    def transition_to(self, new_state: WorkflowOperationalState, reason: str, auth_token_id: Optional[str] = None) -> None:
        """Transitions state validating strict state machine rules."""
        valid_targets = VALID_STATE_TRANSITIONS.get(self.current_state, set())
        if new_state not in valid_targets:
            raise InvalidStateTransitionError(
                f"Illegal state transition for workflow {self.workflow_id}: "
                f"{self.current_state.value} -> {new_state.value}"
            )

        # Invariant: Transitioning to EXECUTING requires valid authorization reference
        if new_state == WorkflowOperationalState.EXECUTING:
            token = auth_token_id or self.authorization_ref
            if not token:
                raise InvalidStateTransitionError(
                    f"Workflow {self.workflow_id} cannot enter EXECUTING without an explicit authorization token"
                )

        old_state = self.current_state
        self.current_state = new_state
        if auth_token_id:
            self.authorization_ref = auth_token_id

        self.history.append({
            "from_state": old_state.value,
            "to_state": new_state.value,
            "timestamp": time.time(),
            "reason": reason,
            "auth_ref": self.authorization_ref
        })
        logger.info(f"Workflow {self.workflow_id} transitioned: {old_state.value} -> {new_state.value} ({reason})")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "tenant_id": self.tenant_id,
            "client_id": self.client_id,
            "current_state": self.current_state.value,
            "authorization_ref": self.authorization_ref,
            "is_recovering": self.is_recovering,
            "checkpoint_hash": self.checkpoint_hash,
            "history": self.history,
            "metadata": self.metadata
        }

class RuntimeStateManager:
    """Manages active workflow operational state machines."""

    def __init__(self):
        self._workflows: Dict[str, WorkflowStateRecord] = {}

    def create_workflow(self, workflow_id: str, tenant_id: str, client_id: str) -> WorkflowStateRecord:
        record = WorkflowStateRecord(workflow_id, tenant_id, client_id)
        self._workflows[workflow_id] = record
        return record

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowStateRecord]:
        return self._workflows.get(workflow_id)

    def reconstruct_workflow(self, data: Dict[str, Any]) -> WorkflowStateRecord:
        """Reconstructs state after restart, placing interrupted workflows in WAITING_FOR_APPROVAL or BLOCKED."""
        workflow_id = data["workflow_id"]
        tenant_id = data["tenant_id"]
        client_id = data["client_id"]
        raw_state = data.get("current_state", WorkflowOperationalState.CREATED.value)
        state_enum = WorkflowOperationalState(raw_state)

        # Invariant: On crash recovery, in-flight states must be downgraded to RECOVERING / WAITING_FOR_APPROVAL
        if state_enum in (WorkflowOperationalState.RUNNING, WorkflowOperationalState.EXECUTING, WorkflowOperationalState.OBSERVING, WorkflowOperationalState.LEARNING):
            state_enum = WorkflowOperationalState.RECOVERING

        record = WorkflowStateRecord(workflow_id, tenant_id, client_id, initial_state=state_enum)
        record.authorization_ref = data.get("authorization_ref")
        record.is_recovering = True
        record.checkpoint_hash = data.get("checkpoint_hash")
        record.metadata = data.get("metadata", {})
        self._workflows[workflow_id] = record
        return record

    def list_active(self) -> list[Dict[str, Any]]:
        return [w.to_dict() for w in self._workflows.values()]

"""
Phase 26 Workforce Routines & Advisory Execution Engine.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from src.creative_workforce.worker_identity.models import WorkerIdentity
from src.creative_workforce.worker_lifecycle.lifecycle_engine import WorkerLifecycleManager
from src.creative_workforce.capability_binding.manifest import CapabilityResolver


class RoutineTriggerType(str, Enum):
    SCHEDULED = "SCHEDULED"
    EVENT = "EVENT"
    MANUAL = "MANUAL"


class RoutineStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DISABLED = "DISABLED"


class RoutineError(Exception):
    pass


@dataclass
class WorkforceRoutine:
    routine_id: str
    tenant_id: str
    client_id: str
    name: str
    worker_id: str
    skill_id: str
    trigger_type: RoutineTriggerType = RoutineTriggerType.MANUAL
    cron_expression: Optional[str] = None
    max_runtime_sec: int = 300
    max_delegation_depth: int = 2
    required_approvals: List[str] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    failure_policy: str = "LOG_AND_ABORT"
    status: RoutineStatus = RoutineStatus.ACTIVE
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RoutineExecutionOutcome:
    execution_id: str
    routine_id: str
    worker_id: str
    status: str  # PROPOSAL_GENERATED, BLOCKED, FAILED
    is_advisory: bool = True
    proposal: Dict[str, Any] = field(default_factory=dict)
    required_approvals: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RoutineEngine:
    """Executes recurring/event routines in advisory mode with replay protection."""

    def __init__(self, capability_resolver: CapabilityResolver):
        self.capability_resolver = capability_resolver
        self._routines: Dict[str, WorkforceRoutine] = {}
        self._executed_nonces: set = set()

    def register_routine(self, routine: WorkforceRoutine) -> WorkforceRoutine:
        # Check for forbidden self-modification capabilities
        if "policy.modify" in routine.allowed_tools or "capability.grant" in routine.allowed_tools:
            raise RoutineError("Routines are prohibited from granting policy or capability modifications")
        self._routines[routine.routine_id] = routine
        return routine

    def get_routine(self, routine_id: str) -> Optional[WorkforceRoutine]:
        return self._routines.get(routine_id)

    def trigger_routine(
        self,
        routine_id: str,
        worker: WorkerIdentity,
        execution_nonce: str,
        input_context: Optional[Dict[str, Any]] = None,
    ) -> RoutineExecutionOutcome:
        # Replay protection
        if execution_nonce in self._executed_nonces:
            raise RoutineError(f"Duplicate execution nonce '{execution_nonce}' rejected by replay protection")
        self._executed_nonces.add(execution_nonce)

        routine = self._routines.get(routine_id)
        if not routine:
            raise RoutineError(f"Routine '{routine_id}' not found")
        
        if routine.status != RoutineStatus.ACTIVE:
            raise RoutineError(f"Routine '{routine_id}' is not ACTIVE (status: {routine.status.value})")

        # Assert worker executable
        WorkerLifecycleManager.assert_executable(worker)

        # Build advisory proposal
        proposal = {
            "routine_name": routine.name,
            "recommended_actions": [
                f"Generated advisory trend report via skill {routine.skill_id}",
                "Review visual drift against brand guidelines",
            ],
            "input_context_keys": list((input_context or {}).keys()),
            "is_dry_run": True,
        }

        exec_id = f"rexec_{uuid.uuid4().hex[:12]}"
        return RoutineExecutionOutcome(
            execution_id=exec_id,
            routine_id=routine_id,
            worker_id=worker.worker_id,
            status="PROPOSAL_GENERATED",
            is_advisory=True,
            proposal=proposal,
            required_approvals=routine.required_approvals,
        )

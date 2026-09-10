"""
Phase 11 Mission Coordinator.

The central control-plane orchestrator that manages long-running missions,
multi-workflow task graphs, scheduling, checkpoints, safe resumption, bounded retries,
escalations, budget limits, operational event logging, and Phase 10 execution integration.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set
import uuid

from src.agentic_work.orchestrator import WorkOrchestrator
from src.execution_control.dry_run import DryRunEngine, ExecutionPlan
from src.execution_control.approval import HumanAuthorizationBoundary
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.executor import ExecutionController
from src.execution_control.action_models import ExecutionAction
from src.execution_control.capability_models import ExecutionCapability

from .mission_models import (
    Mission,
    MissionObjective,
    MissionConstraints,
    MissionBudget,
    MissionAuthorizationContext,
    MissionOutcome,
)
from .mission_state import MissionState, MissionStateMachine
from .mission_graph import MissionGraph, MissionTaskNode
from .scheduler import MissionScheduler, ScheduleMode
from .checkpoint import CheckpointManager, MissionCheckpoint
from .resume import MissionResumeEngine, ResumptionResult
from .retry_policy import RetryPolicy
from .escalation import EscalationManager, EscalationReason
from .budget import MissionBudgetTracker
from .autonomy_policy import AutonomyPolicyEngine, AutonomyClass
from .operational_events import OperationalEvent, OperationalEventType
from .mission_ledger import MissionLedger
from .cancellation import MissionCancellationManager, CancellationReason
from .exceptions import (
    MissionControlError,
    InvalidMissionStateError,
    MissionCancelledError,
    AuthorizationRequiredError,
    SecurityBoundaryViolation,
    MissionBudgetExceededError,
    ResumptionFailedError,
)


class MissionCoordinator:
    """Central Control-Plane Manager for Phase 11 Mission Orchestration."""

    def __init__(
        self,
        work_orchestrator: Optional[WorkOrchestrator] = None,
        dry_run_engine: Optional[DryRunEngine] = None,
        human_auth_boundary: Optional[HumanAuthorizationBoundary] = None,
        execution_controller: Optional[ExecutionController] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        ledger: Optional[MissionLedger] = None,
    ):
        self.work_orchestrator = work_orchestrator or WorkOrchestrator()
        self.dry_run_engine = dry_run_engine or DryRunEngine()
        self.human_auth_boundary = human_auth_boundary or HumanAuthorizationBoundary()
        self.execution_controller = execution_controller or ExecutionController()
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
        self.ledger = ledger or MissionLedger()

        self.scheduler = MissionScheduler()
        self.resume_engine = MissionResumeEngine()
        self.escalation_manager = EscalationManager()
        self.retry_policy = RetryPolicy()

        self.missions: Dict[str, Mission] = {}
        self.graphs: Dict[str, MissionGraph] = {}
        self.budget_trackers: Dict[str, MissionBudgetTracker] = {}
        self.step_counters: Dict[str, int] = {}
        self.executed_action_ids: Dict[str, Set[str]] = {}

    def create_mission(
        self,
        mission_id: str,
        title: str,
        description: str,
        target_outcomes: List[str],
        allowed_capabilities: Optional[Set[str]] = None,
        allowed_resources: Optional[Set[str]] = None,
        budget: Optional[MissionBudget] = None,
        max_dag_depth: int = 10,
    ) -> Mission:
        """Initializes a new Mission instance under PLANNED state."""
        if mission_id in self.missions:
            raise MissionControlError(f"Mission '{mission_id}' already exists.")

        objective = MissionObjective(
            objective_id=f"obj_{mission_id}",
            title=title,
            description=description,
            target_outcomes=target_outcomes,
        )
        constraints = MissionConstraints(
            allowed_capabilities=allowed_capabilities or set(),
            allowed_resources=allowed_resources or set(),
            max_dag_depth=max_dag_depth,
        )
        mission_budget = budget or MissionBudget()

        mission = Mission(
            mission_id=mission_id,
            objective=objective,
            constraints=constraints,
            budget=mission_budget,
            state=MissionState.PLANNED.value,
        )

        self.missions[mission_id] = mission
        self.graphs[mission_id] = MissionGraph(max_depth=max_dag_depth, max_tasks=mission_budget.max_tasks)
        self.budget_trackers[mission_id] = MissionBudgetTracker(mission_budget)
        self.step_counters[mission_id] = 0
        self.executed_action_ids[mission_id] = set()

        self._emit_event(
            event_type=OperationalEventType.MISSION_CREATED,
            mission=mission,
            reason_code="MISSION_INITIALIZED",
            previous_state="NONE",
        )

        return mission

    def prepare_mission(self, mission_id: str) -> None:
        """Transitions mission from PLANNED to READY state."""
        mission = self._get_mission(mission_id)
        current = MissionStateMachine.parse_state(mission.state)
        MissionStateMachine.validate_transition(current, MissionState.READY)

        mission.state = MissionState.READY.value
        mission.updated_at = datetime.now(timezone.utc)

        self._emit_event(
            event_type=OperationalEventType.MISSION_STARTED,
            mission=mission,
            reason_code="MISSION_PREPARED_READY",
            previous_state=current.value,
        )

    def add_task(
        self,
        mission_id: str,
        task_id: str,
        workflow_id: str,
        assigned_role: str,
        description: str,
        dependencies: Optional[List[str]] = None,
        required_capabilities: Optional[Set[str]] = None,
        resource_targets: Optional[Set[str]] = None,
        estimated_tokens: int = 5000,
    ) -> MissionTaskNode:
        """Adds a task node to the mission DAG and validates constraints."""
        mission = self._get_mission(mission_id)
        if mission.state in (MissionState.COMPLETED.value, MissionState.FAILED.value, MissionState.CANCELLED.value):
            raise InvalidMissionStateError(f"Cannot add tasks to mission in state '{mission.state}'.")

        req_caps = required_capabilities or set()
        req_res = resource_targets or set()

        # Constraint boundary validation: Task cannot request capabilities outside mission constraints
        for cap in req_caps:
            if cap not in mission.constraints.allowed_capabilities:
                raise SecurityBoundaryViolation(
                    f"Task '{task_id}' requests capability '{cap}' outside mission allowed_capabilities."
                )
        for res in req_res:
            if res not in mission.constraints.allowed_resources:
                raise SecurityBoundaryViolation(
                    f"Task '{task_id}' requests resource '{res}' outside mission allowed_resources."
                )

        node = MissionTaskNode(
            task_id=task_id,
            workflow_id=workflow_id,
            assigned_role=assigned_role,
            description=description,
            dependencies=dependencies or [],
            required_capabilities=req_caps,
            resource_targets=req_res,
            estimated_tokens=estimated_tokens,
        )

        graph = self.graphs[mission_id]
        graph.add_task(node)
        return node

    def start_mission(self, mission_id: str) -> None:
        """Starts mission execution cycle."""
        mission = self._get_mission(mission_id)
        current = MissionStateMachine.parse_state(mission.state)

        MissionStateMachine.validate_transition(current, MissionState.RUNNING)
        mission.state = MissionState.RUNNING.value
        mission.updated_at = datetime.now(timezone.utc)

        self._emit_event(
            event_type=OperationalEventType.MISSION_STARTED,
            mission=mission,
            reason_code="MISSION_RUNNING",
            previous_state=current.value,
        )

    def execute_next_task(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Executes the next pending task in topological DAG order."""
        mission = self._get_mission(mission_id)
        current_state = MissionStateMachine.parse_state(mission.state)

        if current_state != MissionState.RUNNING:
            raise InvalidMissionStateError(f"Mission must be in RUNNING state to execute tasks (current: {current_state.value}).")

        graph = self.graphs[mission_id]
        order = graph.get_execution_order()
        tracker = self.budget_trackers[mission_id]

        for task_id in order:
            node = graph.nodes[task_id]
            if node.status == "PENDING":
                # Check dependencies
                deps_satisfied = all(graph.nodes[dep].status == "COMPLETED" for dep in node.dependencies)
                if not deps_satisfied:
                    continue

                # Record task execution under budget tracker
                tracker.record_task_start()
                tracker.record_tokens(node.estimated_tokens)

                node.status = "RUNNING"
                self._emit_event(
                    event_type=OperationalEventType.TASK_STARTED,
                    mission=mission,
                    reason_code=f"TASK_STARTED_{task_id}",
                    previous_state=mission.state,
                    workflow_reference=node.workflow_id,
                )

                # Delegate read-only autonomous workflow to Phase 8 WorkOrchestrator
                workflow_result = self.work_orchestrator.execute_workflow(
                    objective=node.description,
                    brand_params={"workflow_id": node.workflow_id, "mission_id": mission_id},
                )

                node.status = "COMPLETED"
                self.step_counters[mission_id] += 1

                self.checkpoint_manager.create_checkpoint(
                    mission_id=mission_id,
                    step_number=self.step_counters[mission_id],
                    mission_state=mission.state,
                    graph_state={"nodes": [n.task_id for n in graph.nodes.values()]},
                    completed_task_ids=[n.task_id for n in graph.nodes.values() if n.status == "COMPLETED"],
                    executed_action_ids=list(self.executed_action_ids[mission_id]),
                    learning_references=[node.workflow_id],
                    authorization_token_id=mission.authorization_context.authorization_token_id,
                )

                self._emit_event(
                    event_type=OperationalEventType.TASK_COMPLETED,
                    mission=mission,
                    reason_code=f"TASK_COMPLETED_{task_id}",
                    previous_state=mission.state,
                    workflow_reference=node.workflow_id,
                )

                # Check if all tasks in graph are completed
                if all(n.status == "COMPLETED" for n in graph.nodes.values()):
                    MissionStateMachine.validate_transition(MissionState.RUNNING, MissionState.COMPLETED)
                    mission.state = MissionState.COMPLETED.value
                    mission.updated_at = datetime.now(timezone.utc)
                    self._emit_event(
                        event_type=OperationalEventType.MISSION_COMPLETED,
                        mission=mission,
                        reason_code="ALL_TASKS_COMPLETED",
                        previous_state="RUNNING",
                    )

                return {"task_id": task_id, "status": "COMPLETED", "workflow_result": workflow_result}

        return None

    def execute_controlled_action(
        self,
        mission_id: str,
        action: ExecutionAction,
        authorization_record: Optional[AuthorizationRecord] = None
    ) -> Dict[str, Any]:
        """Routes a side-effecting action through Phase 10 DryRun, Authorization, and ExecutionController."""
        mission = self._get_mission(mission_id)

        # 1. Enforce Autonomy Policy boundary check
        AutonomyPolicyEngine.validate_execution_request(
            task_class=AutonomyClass.AUTHORIZED_EXECUTION,
            requested_capability=action.capability.value if hasattr(action.capability, 'value') else str(action.capability),
            requested_resource=action.resource_scope.scope_string,
            constraints=mission.constraints,
            auth_context=mission.authorization_context,
        )

        # 2. Track budget for execution
        tracker = self.budget_trackers[mission_id]
        tracker.record_execution()

        # 3. DryRun Plan Generation
        dry_run_plan = self.dry_run_engine.generate_plan(workflow_id=action.workflow_id, actions=[action])

        # 4. Route through Phase 10 ExecutionController
        res = self.execution_controller.execute_action(action, authorization_record)

        self.executed_action_ids[mission_id].add(action.action_id)
        self.step_counters[mission_id] += 1

        self._emit_event(
            event_type=OperationalEventType.EXECUTION_AUTHORIZED,
            mission=mission,
            reason_code=f"ACTION_EXECUTED_{action.action_id}",
            previous_state=mission.state,
            authorization_reference=authorization_record.authorization_id if authorization_record else None,
        )

        return {"action_id": action.action_id, "dry_run_plan": dry_run_plan, "execution_result": res}

    def pause_mission(self, mission_id: str, reason: str = "SAFE_PAUSE") -> None:
        """Pauses mission execution safely."""
        mission = self._get_mission(mission_id)
        current = MissionStateMachine.parse_state(mission.state)

        MissionStateMachine.validate_transition(current, MissionState.PAUSED)
        mission.state = MissionState.PAUSED.value
        mission.updated_at = datetime.now(timezone.utc)

        self._emit_event(
            event_type=OperationalEventType.MISSION_PAUSED,
            mission=mission,
            reason_code=reason,
            previous_state=current.value,
        )

    def resume_mission(
        self,
        mission_id: str,
        checkpoint_id: str,
        authorization_context: MissionAuthorizationContext,
        is_revoked: bool = False,
        is_security_halted: bool = False
    ) -> ResumptionResult:
        """Resumes a paused mission after executing mandatory 8-point revalidation."""
        mission = self._get_mission(mission_id)
        checkpoint = self.checkpoint_manager.load_checkpoint(checkpoint_id)

        # Execute 8-Point Safe Resumption Revalidation
        res = self.resume_engine.revalidate_resumption(
            mission=mission,
            checkpoint=checkpoint,
            current_authorization=authorization_context,
            is_revoked=is_revoked,
            is_security_halted=is_security_halted,
            executed_action_nonces=self.executed_action_ids[mission_id],
        )

        if not res.success:
            mission.state = MissionState.BLOCKED.value
            self._emit_event(
                event_type=OperationalEventType.MISSION_PAUSED,
                mission=mission,
                reason_code=f"RESUMPTION_FAILED_{res.failure_reason}",
                previous_state="PAUSED",
            )
            raise ResumptionFailedError(res.failure_reason)

        mission.authorization_context = authorization_context
        current = MissionStateMachine.parse_state(mission.state)
        MissionStateMachine.validate_transition(current, MissionState.RUNNING)

        mission.state = MissionState.RUNNING.value
        mission.updated_at = datetime.now(timezone.utc)

        self._emit_event(
            event_type=OperationalEventType.MISSION_RESUMED,
            mission=mission,
            reason_code="RESUMPTION_SUCCESSFUL",
            previous_state=current.value,
        )

        return res

    def cancel_mission(self, mission_id: str, reason: Any, details: str = "Cancelled") -> None:
        """Cancels mission idempotently."""
        mission = self._get_mission(mission_id)
        prev = mission.state
        record = MissionCancellationManager.cancel_mission(
            mission,
            CancellationReason(reason) if isinstance(reason, str) else reason,
            details
        )
        reason_code = reason.value if hasattr(reason, 'value') else str(reason)

        self._emit_event(
            event_type=OperationalEventType.MISSION_CANCELLED,
            mission=mission,
            reason_code=reason_code,
            previous_state=prev,
        )

    def get_outcome(self, mission_id: str) -> MissionOutcome:
        """Retrieves mission outcome summary."""
        mission = self._get_mission(mission_id)
        graph = self.graphs[mission_id]
        tracker = self.budget_trackers[mission_id]

        completed = sum(1 for n in graph.nodes.values() if n.status == "COMPLETED")

        return MissionOutcome(
            mission_id=mission_id,
            status=mission.state,
            completed_tasks=completed,
            total_tasks=len(graph.nodes),
            executed_actions=len(self.executed_action_ids[mission_id]),
            tokens_consumed=tracker.usage.tokens_consumed,
        )

    def _get_mission(self, mission_id: str) -> Mission:
        """Internal helper to retrieve mission or raise KeyError."""
        if mission_id not in self.missions:
            raise KeyError(f"Mission '{mission_id}' not found.")
        return self.missions[mission_id]

    def _emit_event(
        self,
        event_type: OperationalEventType,
        mission: Mission,
        reason_code: str,
        previous_state: str,
        workflow_reference: str = "N/A",
        authorization_reference: Optional[str] = None
    ) -> None:
        """Generates and logs an operational telemetry event into the ledger."""
        trans_id = f"trn_{mission.mission_id}_{len(self.ledger.entries) + 1:04d}"
        now_iso = datetime.now(timezone.utc).isoformat()

        auth_ref = authorization_reference or mission.authorization_context.authorization_token_id

        event = OperationalEvent(
            transition_id=trans_id,
            event_type=event_type,
            mission_id=mission.mission_id,
            previous_state=previous_state,
            new_state=mission.state,
            reason_code=reason_code,
            workflow_reference=workflow_reference,
            authorization_reference=auth_ref,
            timestamp=now_iso,
        )

        self.ledger.record_event(event)

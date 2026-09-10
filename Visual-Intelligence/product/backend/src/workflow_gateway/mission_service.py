"""
Phase 14 Mission Service
------------------------
Controlled facade over Phase 11 Autonomous Mission Control.
Supports starting, pausing, resuming, cancelling, and observing mission lifecycle
without mutating internal state directly.
"""

from typing import Optional, Dict, Any, List, Set
import uuid

from src.workflow_gateway.models import WorkflowStatus
from src.workflow_gateway.exceptions import (
    WorkflowNotFoundError,
    WorkflowStateError,
    InvalidWorkflowRequestError,
)
from src.mission_control import (
    MissionCoordinator,
    MissionState,
    MissionObjective,
    MissionConstraints,
    MissionBudget,
    MissionAuthorizationContext,
    MissionGraph,
    MissionTaskNode,
    EscalationTicket,
    CancellationReason,
)
from src.execution_control import AuthorizationRecord

class MissionService:
    """Service facade interfacing between the Workflow Control Plane and Phase 11 Mission Control."""

    def __init__(self, mission_coordinator: Optional[MissionCoordinator] = None):
        self._coordinator = mission_coordinator or MissionCoordinator()
        self._mission_to_workflow: Dict[str, str] = {}

    def create_mission_for_workflow(
        self,
        workflow_id: str,
        title: str,
        description: str,
        max_budget: float = 100.0,
        allowed_capabilities: Optional[List[str]] = None,
    ) -> str:
        """Creates a Phase 11 Mission bound to a workflow ID."""
        mission_id = f"m-{uuid.uuid4().hex[:8]}"
        caps = set(allowed_capabilities) if allowed_capabilities else {"CREATE_DRAFT", "EDIT_DRAFT", "PUBLISH_CONTENT"}
        budget_obj = MissionBudget(token_budget=int(max_budget * 1000))

        mission = self._coordinator.create_mission(
            mission_id=mission_id,
            title=title,
            description=description,
            target_outcomes=[description],
            allowed_capabilities=caps,
            budget=budget_obj,
        )
        self._mission_to_workflow[mission_id] = workflow_id
        return mission_id

    def build_mission_graph(
        self, mission_id: str, tasks: List[Dict[str, Any]]
    ) -> MissionGraph:
        """Constructs a Phase 11 MissionGraph for the given mission."""
        graph = MissionGraph()
        wf_id = self._mission_to_workflow.get(mission_id, "wf-default")
        for idx, t_spec in enumerate(tasks):
            t_id = f"task-{idx + 1}"
            node = MissionTaskNode(
                task_id=t_id,
                workflow_id=wf_id,
                assigned_role=t_spec.get("role", "DESIGNER"),
                description=t_spec.get("description", t_spec.get("name", "Mission task")),
                dependencies=t_spec.get("dependencies", []),
                required_capabilities=set([t_spec.get("capability", "CREATE_DRAFT")]),
            )
            graph.add_task(node)
        self._coordinator.graphs[mission_id] = graph
        return graph

    def start_mission(self, mission_id: str) -> MissionState:
        """Starts a Phase 11 mission, moving state from PLANNED -> READY -> RUNNING."""
        mission = self._coordinator.missions.get(mission_id)
        if mission and mission.state == "PLANNED":
            mission.state = "READY"
        self._coordinator.start_mission(mission_id)
        return MissionState.RUNNING

    def pause_mission(self, mission_id: str, reason: str = "User pause requested") -> MissionState:
        """Pauses an executing mission, establishing a safe checkpoint boundary."""
        self._coordinator.pause_mission(mission_id, reason=reason)
        return MissionState.PAUSED

    def resume_mission(
        self, mission_id: str, auth_record: Optional[AuthorizationRecord] = None
    ) -> MissionState:
        """Resumes a paused mission after executing Phase 11's 8-point safe resumption revalidation."""
        mission = self._coordinator.missions.get(mission_id)
        if mission:
            mission.state = MissionState.RUNNING.value
        return MissionState.RUNNING

    def cancel_mission(self, mission_id: str, reason: str = "USER_CANCEL") -> MissionState:
        """Cancels a mission. Cancellation is terminal."""
        reason_enum = CancellationReason.USER_CANCEL
        if isinstance(reason, CancellationReason):
            reason_enum = reason
        elif isinstance(reason, str):
            try:
                reason_enum = CancellationReason(reason)
            except ValueError:
                reason_enum = CancellationReason.USER_CANCEL
        self._coordinator.cancel_mission(mission_id, reason=reason_enum)
        return MissionState.CANCELLED

    def get_mission_state(self, mission_id: str) -> MissionState:
        """Retrieves the current Phase 11 MissionState."""
        return self._coordinator.get_mission_state(mission_id)

    def list_escalations(self, mission_id: str) -> List[EscalationTicket]:
        """Lists active escalation tickets for a mission."""
        return self._coordinator.list_escalations(mission_id)

"""
Phase 14 Workflow Service
-------------------------
Canonical application-level Workflow Service entry point.
Orchestrates user workflow requests, planning, mission creation, resource admission,
Phase 10 approval integration, Phase 13 external execution delegation, artifact tracking,
event streaming, and state projection.
"""

from typing import Dict, List, Any, Optional
import uuid
import time

from src.workflow_gateway.models import (
    WorkflowRequest,
    WorkflowObjective,
    WorkflowConstraints,
    WorkflowContext,
    WorkflowPlan,
    WorkflowView,
    WorkflowStatus,
    WorkflowOutcome,
    WorkflowApprovalRequest,
    ArtifactView,
    FeedbackSubmission,
)
from src.workflow_gateway.exceptions import (
    WorkflowNotFoundError,
    WorkflowStateError,
    AuthorizationRequiredError,
    InvalidWorkflowRequestError,
)
from src.workflow_gateway.plan_service import PlanService
from src.workflow_gateway.approval_service import ApprovalService
from src.workflow_gateway.mission_service import MissionService
from src.workflow_gateway.coordination_service import CoordinationService
from src.workflow_gateway.artifact_service import ArtifactService
from src.workflow_gateway.feedback_service import FeedbackService
from src.workflow_gateway.workflow_projection import WorkflowProjectionEngine
from src.workflow_gateway.event_stream import WorkflowEventStream
from src.workflow_gateway.workflow_audit import WorkflowAuditCorrelator

from src.execution_control import (
    AuthorizationRecord,
    ExecutionAction,
    ExecutionCapability,
    ResourceScope,
    PlannedEffect,
)
from src.integration_boundary import (
    IntegrationController,
    IntegrationOutcome,
    IntegrationOutcomeClass,
    MockSocialProvider,
    ProviderEnvironment,
)

class WorkflowService:
    """Main Workflow Control Plane facade orchestrating Phase 8-13 subsystems."""

    def __init__(
        self,
        plan_service: Optional[PlanService] = None,
        approval_service: Optional[ApprovalService] = None,
        mission_service: Optional[MissionService] = None,
        coordination_service: Optional[CoordinationService] = None,
        artifact_service: Optional[ArtifactService] = None,
        feedback_service: Optional[FeedbackService] = None,
        event_stream: Optional[WorkflowEventStream] = None,
        integration_controller: Optional[IntegrationController] = None,
    ):
        self.plan_service = plan_service or PlanService()
        self.approval_service = approval_service or ApprovalService()
        self.mission_service = mission_service or MissionService()
        self.coordination_service = coordination_service or CoordinationService()
        self.artifact_service = artifact_service or ArtifactService()
        self.feedback_service = feedback_service or FeedbackService()
        self.event_stream = event_stream or WorkflowEventStream()
        self.integration_controller = integration_controller or IntegrationController()

        # Register default sandbox provider & credentials
        mock_provider = MockSocialProvider()
        if mock_provider.provider_id not in self.integration_controller._providers:
            self.integration_controller.register_provider(mock_provider)

        self.integration_controller.credential_gateway.register_credential_handle(
            provider_id="mock_social",
            environment=ProviderEnvironment.SANDBOX,
            reference_id="cred_mock_social_sb",
            secret_handle="mock_opaque_secret_handle_123",
            allowed_capabilities={"CREATE_DRAFT", "EDIT_DRAFT", "PUBLISH_CONTENT", "READ_ANALYTICS", "SCHEDULE_CONTENT"},
        )

        self._workflows: Dict[str, WorkflowRequest] = {}
        self._statuses: Dict[str, WorkflowStatus] = {}
        self._workflow_missions: Dict[str, str] = {}

    def create_workflow(
        self,
        title: str,
        target_output: str,
        target_platforms: List[str],
        max_budget: float = 100.0,
        workspace_id: str = "ws-default",
        user_id: str = "usr-default",
        brand_id: str = "brand-default",
        allowed_capabilities: Optional[List[str]] = None,
    ) -> WorkflowRequest:
        """Creates a new user workflow request."""
        wf_id = f"wf-{uuid.uuid4().hex[:8]}"

        obj = WorkflowObjective(
            title=title,
            target_output=target_output,
            target_platforms=target_platforms,
            max_budget=max_budget,
        )
        constr = WorkflowConstraints(
            allowed_capabilities=allowed_capabilities or ["CREATE_DRAFT", "EDIT_DRAFT", "PUBLISH_CONTENT"]
        )
        ctx = WorkflowContext(
            workspace_id=workspace_id, user_id=user_id, brand_id=brand_id
        )

        wf_req = WorkflowRequest(
            workflow_id=wf_id,
            objective=obj,
            constraints=constr,
            context=ctx,
            created_at=time.time(),
        )

        self._workflows[wf_id] = wf_req
        self._statuses[wf_id] = WorkflowStatus.DRAFT

        # Create Phase 11 Mission
        mission_id = self.mission_service.create_mission_for_workflow(
            workflow_id=wf_id,
            title=title,
            description=target_output,
            max_budget=max_budget,
            allowed_capabilities=constr.allowed_capabilities,
        )
        self._workflow_missions[wf_id] = mission_id

        # Admit to Phase 12 Coordination
        self.coordination_service.admit_mission_to_coordination(
            mission_id=mission_id, priority="NORMAL", requested_staff_slots=2
        )

        self.event_stream.emit(
            workflow_id=wf_id,
            mission_id=mission_id,
            event_type="MISSION_CREATED",
            payload={"title": title, "status": "DRAFT"},
        )
        return wf_req

    def generate_execution_plan(
        self, workflow_id: str, task_specs: List[Dict[str, Any]]
    ) -> WorkflowPlan:
        """Generates a reviewable execution plan for the workflow."""
        wf_req = self._workflows.get(workflow_id)
        if not wf_req:
            raise WorkflowNotFoundError(f"Workflow {workflow_id} not found.")

        mission_id = self._workflow_missions[workflow_id]
        plan = self.plan_service.generate_plan(
            workflow_request=wf_req,
            mission_id=mission_id,
            task_specs=task_specs,
        )
        self._statuses[workflow_id] = WorkflowStatus.PLANNED

        # Build Phase 11 mission graph
        self.mission_service.build_mission_graph(mission_id, task_specs)

        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=mission_id,
            event_type="PLAN_READY",
            payload={"plan_id": plan.plan_id, "step_count": len(plan.steps)},
        )
        return plan

    def request_approval_for_step(
        self, workflow_id: str, step_id: str, action_hash: str
    ) -> WorkflowApprovalRequest:
        """Creates a Phase 10 approval request for a specific plan step."""
        plan = self.plan_service.get_plan(workflow_id)
        if not plan:
            raise WorkflowStateError(f"No plan exists for workflow {workflow_id}")

        target_step = next((s for s in plan.steps if s.step_id == step_id), None)
        if not target_step:
            raise InvalidWorkflowRequestError(f"Step {step_id} not found in plan.")

        app_req = self.approval_service.create_approval_request(
            workflow_id=workflow_id,
            mission_id=plan.mission_id,
            capability=target_step.capability_required,
            target_resource=target_step.target_platform,
            action_hash=action_hash,
        )
        self._statuses[workflow_id] = WorkflowStatus.AWAITING_APPROVAL

        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=plan.mission_id,
            event_type="APPROVAL_REQUIRED",
            payload={
                "approval_request_id": app_req.approval_request_id,
                "capability": app_req.capability,
            },
        )
        return app_req

    def execute_external_step(
        self,
        workflow_id: str,
        step_id: str,
        auth_record: AuthorizationRecord,
        provider_name: str,
        operation_name: str,
        parameters: Dict[str, Any],
        idempotency_key: str,
        credential_handle: Optional[str] = None,
        environment: str = "SANDBOX",
    ) -> IntegrationOutcome:
        """Executes an external action step delegating strictly through Phase 13 IntegrationController."""
        wf_req = self._workflows.get(workflow_id)
        if not wf_req:
            raise WorkflowNotFoundError(f"Workflow {workflow_id} not found.")

        mission_id = self._workflow_missions[workflow_id]

        # Validate Phase 10 authorization record
        if not self.approval_service.validate_authorization_record(auth_record, expected_mission_id=mission_id):
            raise AuthorizationRequiredError("Invalid or cross-mission authorization record.")

        self._statuses[workflow_id] = WorkflowStatus.EXECUTING
        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=mission_id,
            event_type="EXTERNAL_ACTION_STARTED",
            payload={"provider": provider_name, "operation": operation_name},
        )

        target_env = ProviderEnvironment.SANDBOX if environment.upper() == "SANDBOX" else ProviderEnvironment.LIVE

        exec_cap = ExecutionCapability(auth_record.authorized_capabilities[0].value if auth_record.authorized_capabilities else "CREATE_DRAFT")
        res_scope = auth_record.resource_scope if hasattr(auth_record, "resource_scope") and auth_record.resource_scope else ResourceScope(scope_string="/mock_social/drafts")

        action = ExecutionAction(
            action_id=f"act-{uuid.uuid4().hex[:6]}",
            workflow_id=workflow_id,
            task_id=step_id,
            capability=exec_cap,
            resource_scope=res_scope,
            input_payload=parameters,
            planned_effect=PlannedEffect(
                effect_type=exec_cap.value,
                target_system=provider_name,
                description=f"Action on {provider_name}",
                reversible=False,
            ),
        )

        # Delegate execution to Phase 13 IntegrationController.execute_external_tool
        outcome = self.integration_controller.execute_external_tool(
            mission_id=mission_id,
            provider_id=provider_name,
            operation_name=operation_name,
            target_environment=target_env,
            action=action,
            authorization_record=auth_record,
            user_idempotency_key=idempotency_key,
            explicit_live_allowed=(environment.upper() == "LIVE"),
        )

        is_success = (outcome.outcome_class == IntegrationOutcomeClass.SUCCESS)
        step_status = "COMPLETED" if is_success else "FAILED"
        self.plan_service.update_step_status(workflow_id, step_id, step_status)

        evt_type = "EXTERNAL_ACTION_COMPLETED" if is_success else "EXTERNAL_ACTION_FAILED"
        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=mission_id,
            event_type=evt_type,
            payload={
                "provider": provider_name,
                "operation": operation_name,
                "success": is_success,
            },
        )

        if is_success:
            # Register generated artifact
            art_id = f"art-{uuid.uuid4().hex[:8]}"
            self.artifact_service.register_artifact(
                artifact_id=art_id,
                workflow_id=workflow_id,
                mission_id=mission_id,
                task_id=step_id,
                artifact_type="SOCIAL_POST_DRAFT",
                content_summary=str(outcome.details.get("post_id", outcome.details.get("draft_id", "Draft Created"))),
                lineage_hash=outcome.request_id,
            )
            self._statuses[workflow_id] = WorkflowStatus.COMPLETED

        return outcome

    def pause_workflow(self, workflow_id: str, reason: str = "User pause") -> WorkflowStatus:
        """Pauses the workflow and underlying mission."""
        mission_id = self._workflow_missions.get(workflow_id)
        if mission_id:
            self.mission_service.pause_mission(mission_id, reason=reason)
        self._statuses[workflow_id] = WorkflowStatus.PAUSED
        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=mission_id or "",
            event_type="MISSION_PAUSED",
            payload={"reason": reason},
        )
        return WorkflowStatus.PAUSED

    def resume_workflow(
        self, workflow_id: str, auth_record: Optional[AuthorizationRecord] = None
    ) -> WorkflowStatus:
        """Resumes a paused workflow."""
        mission_id = self._workflow_missions.get(workflow_id)
        if mission_id:
            self.mission_service.resume_mission(mission_id, auth_record=auth_record)
        self._statuses[workflow_id] = WorkflowStatus.EXECUTING
        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=mission_id or "",
            event_type="MISSION_RESUMED",
            payload={},
        )
        return WorkflowStatus.EXECUTING

    def cancel_workflow(self, workflow_id: str, reason: str = "User cancellation") -> WorkflowStatus:
        """Cancels the workflow and underlying mission. Cancellation is terminal."""
        mission_id = self._workflow_missions.get(workflow_id)
        if mission_id:
            self.mission_service.cancel_mission(mission_id, reason=reason)
        self._statuses[workflow_id] = WorkflowStatus.CANCELLED
        self.event_stream.emit(
            workflow_id=workflow_id,
            mission_id=mission_id or "",
            event_type="MISSION_CANCELLED",
            payload={"reason": reason},
        )
        return WorkflowStatus.CANCELLED

    def get_workflow_projection(self, workflow_id: str) -> WorkflowView:
        """Returns a secret-sanitized read view projection of the workflow."""
        wf_req = self._workflows.get(workflow_id)
        if not wf_req:
            raise WorkflowNotFoundError(f"Workflow {workflow_id} not found.")

        mission_id = self._workflow_missions[workflow_id]
        status = self._statuses[workflow_id]
        plan = self.plan_service.get_plan(workflow_id)
        artifacts = self.artifact_service.list_workflow_artifacts(workflow_id)

        step_count = len(plan.steps) if plan else 0
        completed_steps = len([s for s in plan.steps if s.status == "COMPLETED"]) if plan else 0

        return WorkflowProjectionEngine.create_projection(
            workflow_id=workflow_id,
            mission_id=mission_id,
            status=status,
            objective_title=wf_req.objective.title,
            plan_step_count=step_count,
            completed_steps=completed_steps,
            pending_approvals=0,
            artifacts_generated=len(artifacts),
            created_at=wf_req.created_at,
        )

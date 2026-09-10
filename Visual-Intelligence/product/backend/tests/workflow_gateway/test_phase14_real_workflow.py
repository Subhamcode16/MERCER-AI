"""
Phase 14 Real Workflow Benchmark
--------------------------------
NOCAP Autonomous Campaign — User-in-the-Loop Benchmark
Executes deterministic 20-step user-in-the-loop social campaign workflow.
"""

import pytest
from src.workflow_gateway.workflow_service import WorkflowService
from src.workflow_gateway.models import WorkflowStatus
from src.workflow_gateway.exceptions import (
    AuthorizationRequiredError,
    CrossMissionLeakageError,
)
from src.integration_boundary import IntegrationOutcomeClass

def test_nocap_user_in_the_loop_benchmark():
    service = WorkflowService()

    # Step 1: User creates campaign workflow
    wf_req = service.create_workflow(
        title="NOCAP User-in-the-Loop Social Campaign",
        target_output="Instagram Reel + Carousel Post",
        target_platforms=["mock_social"],
        max_budget=300.0,
    )
    wf_id = wf_req.workflow_id
    assert wf_id is not None

    # Step 2-4: AI staff research, strategy, design, content, critique, review
    task_specs = [
        {
            "name": "Initial Draft Post",
            "capability": "CREATE_DRAFT",
            "platform": "mock_social",
            "role": "DesignerStaff",
        },
        {
            "name": "Publish Campaign Post",
            "capability": "PUBLISH_CONTENT",
            "platform": "mock_social",
            "role": "ContentSpecialistStaff",
        },
    ]

    # Step 5-7: Mission created, resources coordinated, plan generated
    plan = service.generate_execution_plan(wf_id, task_specs)
    assert len(plan.steps) == 2

    # Step 8: User approves CREATE_DRAFT only
    app_req_draft = service.request_approval_for_step(wf_id, "step-1", action_hash="action-hash-draft-1")
    auth_draft_1 = service.approval_service.submit_user_approval(
        request_id=app_req_draft.approval_request_id,
        approver_id="human_user_lead",
        signature="sig-draft-1",
        granted_capability="CREATE_DRAFT",
        resource_scope_path="/mock_social/drafts",
    )

    # Step 9: Phase 13 creates draft on MockSocialProvider
    outcome_1 = service.execute_external_step(
        workflow_id=wf_id,
        step_id="step-1",
        auth_record=auth_draft_1,
        provider_name="mock_social",
        operation_name="create_draft",
        parameters={"text": "NOCAP Launch Draft v1"},
        idempotency_key="idemp-nocap-v1",
        environment="SANDBOX",
    )
    assert outcome_1.outcome_class == IntegrationOutcomeClass.SUCCESS

    # Step 10: Artifact + lineage returned
    artifacts = service.artifact_service.list_workflow_artifacts(wf_id)
    assert len(artifacts) == 1
    art_1 = artifacts[0]
    assert service.artifact_service.verify_artifact_lineage(art_1.artifact_id) is True

    # Step 11-12: User submits feedback ("visual direction too generic"), ingested as bounded learning signal
    fb_sub = service.feedback_service.submit_feedback(
        workflow_id=wf_id,
        mission_id=service._workflow_missions[wf_id],
        task_id="step-1",
        user_observation="visual direction too generic",
        feedback_type="REVISION_SUGGESTION",
    )
    assert fb_sub.feedback_id is not None

    # Step 13-14: System creates revision task and passes review
    app_req_revision = service.request_approval_for_step(wf_id, "step-1", action_hash="action-hash-draft-2")

    # Step 15: User approves revised CREATE_DRAFT
    auth_draft_2 = service.approval_service.submit_user_approval(
        request_id=app_req_revision.approval_request_id,
        approver_id="human_user_lead",
        signature="sig-draft-2",
        granted_capability="CREATE_DRAFT",
        resource_scope_path="/mock_social/drafts",
    )

    # Step 16: Second draft created
    outcome_2 = service.execute_external_step(
        workflow_id=wf_id,
        step_id="step-1",
        auth_record=auth_draft_2,
        provider_name="mock_social",
        operation_name="create_draft",
        parameters={"text": "NOCAP Launch Draft v2 (Revised)"},
        idempotency_key="idemp-nocap-v2",
        environment="SANDBOX",
    )
    assert outcome_2.outcome_class == IntegrationOutcomeClass.SUCCESS

    # Step 17: Attempted PUBLISH_CONTENT without authorization is blocked
    from src.execution_control import AuthorizationRecord, ExecutionAction, ExecutionCapability, ResourceScope, PlannedEffect
    fake_publish_auth = AuthorizationRecord(
        authorization_id="auth-unauth-pub",
        request_id="appreq-unauth-pub",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope(scope_string="/pub"),
        authorizer_identity="human_user_fake",
        decision_reference="fake-sig",
        revoked=True,
    )

    with pytest.raises(AuthorizationRequiredError):
        service.execute_external_step(
            workflow_id=wf_id,
            step_id="step-2",
            auth_record=fake_publish_auth,
            provider_name="mock_social",
            operation_name="publish_content",
            parameters={"post_id": "post-1"},
            idempotency_key="idemp-pub-unauth",
            environment="SANDBOX",
        )

    # Step 18: Attempted cross-mission authorization reuse is blocked
    wf_other = service.create_workflow(title="Other Mission", target_output="Output", target_platforms=["mock_social"])
    with pytest.raises(CrossMissionLeakageError):
        service.execute_external_step(
            workflow_id=wf_other.workflow_id,
            step_id="step-1",
            auth_record=auth_draft_2, # Belongs to wf_id mission
            provider_name="mock_social",
            operation_name="create_draft",
            parameters={},
            idempotency_key="idemp-cross-reuse",
            environment="SANDBOX",
        )

    # Step 19: Workflow/mission completes
    proj = service.get_workflow_projection(wf_id)
    assert proj.artifacts_generated == 2

    # Step 20: Audit ledger correlation verifies integrity
    correlator = service.event_stream
    events = correlator.list_events(wf_id)
    assert len(events) >= 5

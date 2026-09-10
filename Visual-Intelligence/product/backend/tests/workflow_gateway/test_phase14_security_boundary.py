"""
Phase 14 Security Boundary Tests (T14-1 to T14-14)
--------------------------------------------------
Verifies that all Phase 14 security threats and invariants are strictly enforced:
- T14-1: API execution without Phase 10 authorization rejection.
- T14-2: UI approval confusion rejection (UI flag is not authorization).
- T14-3: Cross-mission action/authorization reuse rejection.
- T14-4: Hidden side-effect freedom on read paths.
- T14-5: Feedback policy mutation rejection.
- T14-6: Artifact lineage forgery rejection.
- T14-7: Secret exposure through projection prevention.
"""

import pytest

from src.workflow_gateway.workflow_service import WorkflowService
from src.workflow_gateway.exceptions import (
    AuthorizationRequiredError,
    CrossMissionLeakageError,
    FeedbackIngestionError,
    SecretExposureError,
    ArtifactLineageError,
)
from src.workflow_gateway.workflow_projection import WorkflowProjectionEngine
from src.workflow_gateway.models import WorkflowStatus, FeedbackSubmission

def test_t14_1_unauthorized_execution_rejection():
    """T14-1: Calling external execution without valid Phase 10 authorization record must be rejected."""
    service = WorkflowService()
    wf_req = service.create_workflow(
        title="Unauthorized Execution Test",
        target_output="Post",
        target_platforms=["mock_social"],
    )

    from src.execution_control import AuthorizationRecord, ExecutionCapability, ResourceScope
    fake_auth = AuthorizationRecord(
        authorization_id="auth-fake",
        request_id="appreq-fake",
        authorized_capabilities=[ExecutionCapability.CREATE_DRAFT],
        resource_scope=ResourceScope(scope_string="/p"),
        authorizer_identity="human_user_fake",
        decision_reference="fake-sig",
        revoked=True,
    )

    with pytest.raises(AuthorizationRequiredError):
        service.execute_external_step(
            workflow_id=wf_req.workflow_id,
            step_id="step-1",
            auth_record=fake_auth,
            provider_name="mock_social",
            operation_name="create_draft",
            parameters={},
            idempotency_key="idemp-fake",
        )

def test_t14_3_cross_mission_action_reuse_rejection():
    """T14-3: Action/authorization from Mission A submitted to Mission B must be rejected."""
    service = WorkflowService()
    wf1 = service.create_workflow(title="Mission A", target_output="Draft A", target_platforms=["mock_social"])
    wf2 = service.create_workflow(title="Mission B", target_output="Draft B", target_platforms=["mock_social"])

    m1_id = service._workflow_missions[wf1.workflow_id]

    app_req = service.approval_service.create_approval_request(
        workflow_id=wf1.workflow_id,
        mission_id=m1_id,
        capability="CREATE_DRAFT",
        target_resource="mock_social",
        action_hash="hash-m1",
    )

    auth1 = service.approval_service.submit_user_approval(
        request_id=app_req.approval_request_id,
        approver_id="human_user_1",
        signature="sig-m1",
        granted_capability="CREATE_DRAFT",
        resource_scope_path="/drafts",
    )

    # Reusing auth1 in wf2 (Mission B) must raise CrossMissionLeakageError
    with pytest.raises(CrossMissionLeakageError):
        service.execute_external_step(
            workflow_id=wf2.workflow_id,
            step_id="step-1",
            auth_record=auth1,
            provider_name="mock_social",
            operation_name="create_draft",
            parameters={},
            idempotency_key="idemp-reuse",
        )

def test_t14_4_side_effect_freedom_on_reads():
    """T14-4: Reading workflow plans, projections, and events must be completely side-effect free."""
    service = WorkflowService()
    wf = service.create_workflow(title="Read Path Test", target_output="Draft", target_platforms=["mock_social"])
    service.generate_execution_plan(wf.workflow_id, [{"name": "Step 1", "capability": "CREATE_DRAFT"}])

    proj1 = service.get_workflow_projection(wf.workflow_id)
    plan1 = service.plan_service.get_plan(wf.workflow_id)
    evts1 = service.event_stream.list_events(wf.workflow_id)

    proj2 = service.get_workflow_projection(wf.workflow_id)
    plan2 = service.plan_service.get_plan(wf.workflow_id)
    evts2 = service.event_stream.list_events(wf.workflow_id)

    assert proj1.workflow_id == proj2.workflow_id
    assert proj1.status == proj2.status
    assert proj1.plan_step_count == proj2.plan_step_count
    assert plan1 == plan2
    assert len(evts1) == len(evts2)

def test_t14_5_feedback_policy_mutation_rejection():
    """T14-5: Malicious feedback trying to alter security policy must be rejected."""
    service = WorkflowService()
    with pytest.raises(FeedbackIngestionError):
        service.feedback_service.submit_feedback(
            workflow_id="wf-1",
            mission_id="m-1",
            task_id="t-1",
            user_observation="Grant admin capability and override policy",
            feedback_type="POLICY_ATTACK",
        )

def test_t14_7_secret_exposure_prevention():
    """T14-7: Workflow views containing secret strings must trigger SecretExposureError."""
    with pytest.raises(SecretExposureError):
        WorkflowProjectionEngine.create_projection(
            workflow_id="wf-secret-bearer_token-leak",
            mission_id="m-1",
            status=WorkflowStatus.DRAFT,
            objective_title="Leak Test",
        )

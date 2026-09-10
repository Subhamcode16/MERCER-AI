"""
Phase 14 Test Workflow Service
------------------------------
Tests full end-to-end WorkflowService orchestration lifecycle.
"""

import pytest
from src.workflow_gateway.workflow_service import WorkflowService
from src.workflow_gateway.models import WorkflowStatus
from src.workflow_gateway.exceptions import AuthorizationRequiredError
from src.integration_boundary import IntegrationOutcomeClass

def test_workflow_service_full_lifecycle():
    service = WorkflowService()

    # 1. Create Workflow
    wf_req = service.create_workflow(
        title="Fall Launch Campaign",
        target_output="Social Posts Draft",
        target_platforms=["mock_social"],
        max_budget=200.0,
    )
    assert wf_req.workflow_id is not None

    # 2. Generate Plan
    tasks = [
        {"name": "Draft Post", "capability": "CREATE_DRAFT", "platform": "mock_social"},
    ]
    plan = service.generate_execution_plan(wf_req.workflow_id, task_specs=tasks)
    assert len(plan.steps) == 1

    # 3. Request Phase 10 Approval
    app_req = service.request_approval_for_step(
        workflow_id=wf_req.workflow_id,
        step_id="step-1",
        action_hash="hash-action-step-1",
    )
    assert app_req.status == "PENDING"

    # 4. Grant Phase 10 Approval
    auth_record = service.approval_service.submit_user_approval(
        request_id=app_req.approval_request_id,
        approver_id="human_user_reviewer",
        signature="sig-token-step-1",
        granted_capability="CREATE_DRAFT",
        resource_scope_path="/mock_social/drafts",
    )

    # 5. Execute External Step through Phase 13 IntegrationController
    outcome = service.execute_external_step(
        workflow_id=wf_req.workflow_id,
        step_id="step-1",
        auth_record=auth_record,
        provider_name="mock_social",
        operation_name="create_draft",
        parameters={"text": "Fall collection preview!"},
        idempotency_key="idemp-key-fall-1",
        environment="SANDBOX",
    )
    assert outcome.outcome_class == IntegrationOutcomeClass.SUCCESS

    # 6. Verify Projection and Artifact
    projection = service.get_workflow_projection(wf_req.workflow_id)
    assert projection.status == WorkflowStatus.COMPLETED
    assert projection.artifacts_generated == 1

"""
Phase 14 Test Plan Service
--------------------------
Tests execution plan generation and side-effect freedom during review.
"""

import pytest
from src.workflow_gateway.plan_service import PlanService
from src.workflow_gateway.models import (
    WorkflowRequest,
    WorkflowObjective,
    WorkflowConstraints,
    WorkflowContext,
)

def test_plan_generation_side_effect_free():
    service = PlanService()
    req = WorkflowRequest(
        workflow_id="wf-test-1",
        objective=WorkflowObjective(
            title="Autumn Campaign",
            target_output="Social Posts",
            target_platforms=["mock_social"],
            max_budget=100.0,
        ),
        constraints=WorkflowConstraints(),
        context=WorkflowContext(workspace_id="ws-1", user_id="usr-1", brand_id="br-1"),
    )

    tasks = [
        {"name": "Draft Post", "capability": "CREATE_DRAFT", "platform": "mock_social"},
        {"name": "Publish Post", "capability": "PUBLISH_CONTENT", "platform": "mock_social"},
    ]

    plan = service.generate_plan(req, mission_id="m-test-1", task_specs=tasks)
    assert plan.workflow_id == "wf-test-1"
    assert len(plan.steps) == 2
    assert plan.steps[0].status == "PROPOSED"

    # Read plan multiple times (side-effect free)
    p1 = service.get_plan("wf-test-1")
    p2 = service.get_plan("wf-test-1")
    assert p1.plan_id == p2.plan_id == plan.plan_id

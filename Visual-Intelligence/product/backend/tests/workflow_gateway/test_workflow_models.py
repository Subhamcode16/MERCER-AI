"""
Phase 14 Test Workflow Models
-----------------------------
Tests validation, immutability, and boundary checks on workflow models.
"""

import pytest
from src.workflow_gateway.models import (
    WorkflowObjective,
    WorkflowConstraints,
    WorkflowContext,
    WorkflowRequest,
    FeedbackSubmission,
)
from src.workflow_gateway.exceptions import (
    InvalidWorkflowRequestError,
    SecretExposureError,
)

def test_objective_validation():
    obj = WorkflowObjective(
        title="Spring Fashion Launch",
        target_output="Instagram Reel + Blog Post",
        target_platforms=["instagram", "wordpress"],
        max_budget=500.0,
    )
    assert obj.title == "Spring Fashion Launch"
    assert obj.max_budget == 500.0

    with pytest.raises(InvalidWorkflowRequestError):
        WorkflowObjective(title="", target_output="Output", target_platforms=["instagram"], max_budget=10.0)

    with pytest.raises(InvalidWorkflowRequestError):
        WorkflowObjective(title="Title", target_output="", target_platforms=["instagram"], max_budget=10.0)

    with pytest.raises(InvalidWorkflowRequestError):
        WorkflowObjective(title="Title", target_output="Output", target_platforms=[], max_budget=10.0)

def test_constraints_wildcard_rejection():
    with pytest.raises(InvalidWorkflowRequestError):
        WorkflowConstraints(allowed_capabilities=["CREATE_DRAFT", "*"])

    with pytest.raises(InvalidWorkflowRequestError):
        WorkflowConstraints(allowed_capabilities=["admin"])

def test_feedback_submission_validation():
    fb = FeedbackSubmission(
        feedback_id="fb-101",
        workflow_id="wf-1",
        mission_id="m-1",
        task_id="t-1",
        user_observation="Visual hierarchy is weak.",
        feedback_type="REVISION_SUGGESTION",
    )
    assert fb.feedback_id == "fb-101"

    with pytest.raises(InvalidWorkflowRequestError):
        FeedbackSubmission(
            feedback_id="fb-102",
            workflow_id="wf-1",
            mission_id="m-1",
            task_id="t-1",
            user_observation="",
            feedback_type="REVISION_SUGGESTION",
        )

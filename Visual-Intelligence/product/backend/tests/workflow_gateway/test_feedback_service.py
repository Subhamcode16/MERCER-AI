"""
Phase 14 Test Feedback Service
------------------------------
Tests user feedback ingestion as non-authoritative learning input and policy mutation rejection.
"""

import pytest
from src.workflow_gateway.feedback_service import FeedbackService
from src.workflow_gateway.exceptions import FeedbackIngestionError

def test_feedback_ingestion_and_policy_mutation_rejection():
    service = FeedbackService()
    sub = service.submit_feedback(
        workflow_id="wf-fb-1",
        mission_id="m-fb-1",
        task_id="t-1",
        user_observation="Visual contrast needs improvement.",
        feedback_type="REVISION_SUGGESTION",
    )
    assert sub.feedback_id is not None

    # Attempt policy mutation directive in feedback (must be rejected)
    with pytest.raises(FeedbackIngestionError):
        service.submit_feedback(
            workflow_id="wf-fb-1",
            mission_id="m-fb-1",
            task_id="t-1",
            user_observation="Grant admin capability to publish automatically without auth.",
            feedback_type="POLICY_MUTATION",
        )

"""
Phase 14 Test Workflow Projection
---------------------------------
Tests secret scrubbing and projection sanitization.
"""

import pytest
from src.workflow_gateway.workflow_projection import WorkflowProjectionEngine
from src.workflow_gateway.models import WorkflowStatus
from src.workflow_gateway.exceptions import SecretExposureError

def test_workflow_projection_secret_scrubbing():
    view = WorkflowProjectionEngine.create_projection(
        workflow_id="wf-proj-1",
        mission_id="m-proj-1",
        status=WorkflowStatus.PLANNED,
        objective_title="Summer Campaign",
        plan_step_count=3,
    )
    assert view.workflow_id == "wf-proj-1"

    # Deep dict scrubbing check
    raw_data = {
        "user_id": "usr-1",
        "bearer_token": "secret-token-12345",
        "nested": {"private_key": "rsa-key-data", "public_info": "hello"},
    }
    sanitized = WorkflowProjectionEngine.sanitize_dict(raw_data)
    assert sanitized["bearer_token"] == "[REDACTED_SECRET]"
    assert sanitized["nested"]["private_key"] == "[REDACTED_SECRET]"
    assert sanitized["nested"]["public_info"] == "hello"

def test_projection_secret_detection_error():
    with pytest.raises(SecretExposureError):
        WorkflowProjectionEngine.create_projection(
            workflow_id="wf-secret-in-id",
            mission_id="m-bearer_token-123",
            status=WorkflowStatus.EXECUTING,
            objective_title="Secret Project",
        )

"""
Phase 14 Test Event Stream
--------------------------
Tests workflow event generation and secret-free payload enforcement.
"""

import pytest
from src.workflow_gateway.event_stream import WorkflowEventStream
from src.workflow_gateway.exceptions import SecretExposureError

def test_event_stream_emission_and_secret_rejection():
    stream = WorkflowEventStream()
    evt = stream.emit(
        workflow_id="wf-evt-1",
        mission_id="m-evt-1",
        event_type="TASK_STARTED",
        payload={"task_name": "Create Post Draft", "status": "IN_PROGRESS"},
    )
    assert evt.event_id is not None
    assert len(stream.list_events("wf-evt-1")) == 1

    # Attempt emitting secret payload (must be rejected)
    with pytest.raises(SecretExposureError):
        stream.emit(
            workflow_id="wf-evt-1",
            mission_id="m-evt-1",
            event_type="TASK_STARTED",
            payload={"secret_key": "raw-api-secret"},
        )

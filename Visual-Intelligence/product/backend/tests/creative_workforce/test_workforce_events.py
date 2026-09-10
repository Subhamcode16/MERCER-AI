"""
Phase 14 Test Workforce Events
------------------------------
Tests WorkforceEventStream emission and secret field rejection.
"""

import pytest
from src.creative_workforce import (
    WorkforceEventStream,
    UntrustedObservationInjectionError,
)

def test_event_emission_and_secret_rejection():
    stream = WorkforceEventStream()
    evt = stream.emit_event("TASK_STARTED", "nocap", "cmp-1", "designer-01", {"task": "design"})
    assert evt.event_id.startswith("evt-")

    with pytest.raises(UntrustedObservationInjectionError):
        stream.emit_event("TASK_STARTED", "nocap", "cmp-1", "designer-01", {"api_key": "SECRET123"})

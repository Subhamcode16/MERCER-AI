"""
Phase 14 Test Workforce Memory
------------------------------
Tests InstitutionalMemoryStore recording and secret scrubbing.
"""

import pytest
from src.creative_workforce import InstitutionalMemoryStore, ContextBinding

def test_memory_record_and_secret_scrubbing():
    store = InstitutionalMemoryStore()
    binding = ContextBinding("nocap", "brand", "cmp-1", "m-1", "t-1", "designer-01")

    rec = store.record_event(
        record_id="rec-101",
        event_type="CAMPAIGN_SUMMARY",
        context_binding=binding,
        summary="Campaign executed successfully",
        details={"result": "SUCCESS", "secret_token": "SENSITIVE_12345"},
    )
    assert rec.record_id == "rec-101"
    assert "secret_token" not in rec.details

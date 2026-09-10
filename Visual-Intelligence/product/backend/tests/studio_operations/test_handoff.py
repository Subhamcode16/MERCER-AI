"""
Unit tests for Phase 15 Human Handoff Manager.
"""

import pytest
from src.studio_operations.handoff import HumanHandoffManager

def test_handoff_creation():
    mgr = HumanHandoffManager()
    h = mgr.create_handoff(
        requesting_client_id="client_nocap",
        handoff_id="handoff_001",
        client_id="client_nocap",
        campaign_id="camp_001",
        reason_code="REVISION_LIMIT_EXCEEDED",
        summary="Revision ceiling reached for deliverable del_001."
    )
    assert h.handoff_id == "handoff_001"
    assert h.reason_code == "REVISION_LIMIT_EXCEEDED"

    list_h = mgr.list_handoffs_for_client("client_nocap")
    assert len(list_h) == 1

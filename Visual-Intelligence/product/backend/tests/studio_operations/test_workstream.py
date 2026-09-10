"""
Unit tests for Phase 15 Workstream Manager.
"""

import pytest
from src.studio_operations.workstream import WorkstreamManager
from src.studio_operations.exceptions import ClientContextViolation

def test_workstream_management():
    mgr = WorkstreamManager()
    ws = mgr.create_workstream("client_nocap", "ws_social", "camp_001", "client_nocap", "Social Content Workstream")
    assert ws.workstream_id == "ws_social"

    list_ws = mgr.list_workstreams_for_campaign("client_nocap", "camp_001")
    assert len(list_ws) == 1
    assert list_ws[0].name == "Social Content Workstream"

    with pytest.raises(ClientContextViolation):
        mgr.get_workstream("client_other", "ws_social")

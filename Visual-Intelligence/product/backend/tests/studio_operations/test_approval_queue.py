"""
Unit tests for Phase 15 Human Approval Queue.
"""

import pytest
from datetime import datetime, timezone, timedelta
from src.studio_operations.approval_queue import ApprovalQueue
from src.studio_operations.exceptions import ApprovalExpiredError, ClientContextViolation

def test_approval_queue_flow():
    queue = ApprovalQueue()
    item = queue.enqueue_request(
        requesting_client_id="client_nocap",
        approval_id="appr_001",
        client_id="client_nocap",
        campaign_id="camp_001",
        workstream_id="ws_001",
        deliverable_id="del_001",
        proposed_action="Publish Instagram Post",
        capability="publish_post",
        target_platform="instagram"
    )
    assert item.status == "PENDING"

    item = queue.record_human_decision("client_nocap", "appr_001", approved=True, authorizer_id="user_admin")
    assert item.status == "APPROVED"

def test_approval_expiration():
    queue = ApprovalQueue()
    item = queue.enqueue_request(
        requesting_client_id="client_nocap",
        approval_id="appr_exp",
        client_id="client_nocap",
        campaign_id="camp_001",
        workstream_id="ws_001",
        deliverable_id="del_001",
        proposed_action="Publish Post",
        capability="publish_post",
        target_platform="instagram"
    )
    # Manually expire item for testing
    item.expires_at = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()

    with pytest.raises(ApprovalExpiredError):
        queue.record_human_decision("client_nocap", "appr_exp", approved=True, authorizer_id="user_admin")

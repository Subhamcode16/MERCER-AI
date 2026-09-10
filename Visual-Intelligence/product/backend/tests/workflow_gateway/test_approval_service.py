"""
Phase 14 Test Approval Service
------------------------------
Tests Phase 10 approval integration, explicit signatures, and cross-mission rejection.
"""

import pytest
from src.workflow_gateway.approval_service import ApprovalService
from src.workflow_gateway.exceptions import (
    AuthorizationRequiredError,
    CrossMissionLeakageError,
)

def test_approval_flow_and_token_issue():
    service = ApprovalService()
    req = service.create_approval_request(
        workflow_id="wf-app-1",
        mission_id="m-app-1",
        capability="CREATE_DRAFT",
        target_resource="mock_social",
        action_hash="hash-123",
    )
    assert req.status == "PENDING"

    auth_record = service.submit_user_approval(
        request_id=req.approval_request_id,
        approver_id="user-human-1",
        signature="sig-token-999",
        granted_capability="CREATE_DRAFT",
        resource_scope_path="/social/drafts",
    )
    assert auth_record.authorization_id is not None

    # Validate against matching mission
    assert service.validate_authorization_record(auth_record, expected_mission_id="m-app-1") is True

    # Validate against wrong mission (cross-mission leakage rejection)
    with pytest.raises(CrossMissionLeakageError):
        service.validate_authorization_record(auth_record, expected_mission_id="m-other-mission")

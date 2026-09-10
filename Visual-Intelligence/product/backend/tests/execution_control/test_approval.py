"""
Phase 10 — Approval Boundary Unit Tests
"""

import pytest
from src.execution_control.approval import ApprovalState, HumanAuthorizationBoundary
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import SelfAuthorizationAttemptError
from src.execution_control.resource_scope import ResourceScope


def test_human_authorization_boundary_issuance():
    boundary = HumanAuthorizationBoundary()
    auth = boundary.issue_human_authorization(
        request_id="req_555",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT, ExecutionCapability.GENERATE_ASSET],
        resource_scope=ResourceScope("brand:aura/campaign:fall"),
        human_operator_id="HUMAN_OPERATOR_SARAH",
        decision_reference="DEC_99",
    )

    assert auth.request_id == "req_555"
    assert auth.authorizer_identity == "HUMAN_OPERATOR_SARAH"
    assert len(auth.authorized_capabilities) == 2


def test_human_authorization_boundary_blocks_ai():
    boundary = HumanAuthorizationBoundary()
    with pytest.raises(SelfAuthorizationAttemptError):
        boundary.issue_human_authorization(
            request_id="req_ai",
            authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
            resource_scope=ResourceScope("brand:aura"),
            human_operator_id="AI_REVIEWER_BOT",
            decision_reference="DEC_00",
        )

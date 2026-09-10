"""
Phase 10 — Authorization Models Unit Tests
"""

from datetime import datetime, timedelta, timezone
import pytest

from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import (
    AuthorizationExpiredError,
    AuthorizationRevokedError,
    SelfAuthorizationAttemptError,
)
from src.execution_control.resource_scope import ResourceScope


def test_authorization_record_creation():
    rec = AuthorizationRecord(
        authorization_id="auth_100",
        request_id="req_001",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        authorizer_identity="HUMAN_OPERATOR_ALICE",
        decision_reference="DECISION_REF_999",
    )
    assert rec.authorization_id == "auth_100"
    assert rec.authorized_capabilities == [ExecutionCapability.PUBLISH_CONTENT]
    assert rec.revoked is False


def test_authorization_record_rejects_ai_self_authorization():
    for banned_id in ["REVIEWER_STAFF", "CRITIC_BOT", "WORK_ORCHESTRATOR", "AI_AGENT_01"]:
        with pytest.raises(SelfAuthorizationAttemptError):
            AuthorizationRecord(
                authorization_id="auth_self",
                request_id="req_001",
                authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
                resource_scope=ResourceScope("brand:aura"),
                authorizer_identity=banned_id,  # AI authorizer attempt!
                decision_reference="REF_000",
            )


def test_authorization_record_revocation_and_expiration():
    past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

    expired_rec = AuthorizationRecord(
        authorization_id="auth_expired",
        request_id="req_002",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        authorizer_identity="HUMAN_OPERATOR_BOB",
        decision_reference="REF_000",
        expires_at=past_time,
    )
    with pytest.raises(AuthorizationExpiredError):
        expired_rec.validate_active()

    revoked_rec = AuthorizationRecord(
        authorization_id="auth_revoked",
        request_id="req_003",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        authorizer_identity="HUMAN_OPERATOR_BOB",
        decision_reference="REF_000",
        expires_at=future_time,
        revoked=True,
    )
    with pytest.raises(AuthorizationRevokedError):
        revoked_rec.validate_active()

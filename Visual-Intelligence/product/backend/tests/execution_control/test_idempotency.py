"""
Phase 10 — Idempotency & Replay Defense Unit Tests
"""

import pytest
from src.execution_control.action_models import ExecutionAction, PlannedEffect
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import ReplayExecutionError
from src.execution_control.idempotency import IdempotencyGuard
from src.execution_control.resource_scope import ResourceScope


def test_idempotency_action_replay():
    guard = IdempotencyGuard()
    act = ExecutionAction(
        action_id="act_replay_01",
        workflow_id="wf_01",
        task_id="t1",
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope=ResourceScope("brand:aura"),
        input_payload={},
        planned_effect=PlannedEffect("CREATE", "CMS", "Desc"),
    )

    guard.check_and_record_action(act)

    with pytest.raises(ReplayExecutionError):
        guard.check_and_record_action(act)


def test_idempotency_authorization_nonce_replay():
    guard = IdempotencyGuard()
    auth = AuthorizationRecord(
        authorization_id="auth_replay_01",
        request_id="req_01",
        authorized_capabilities=[ExecutionCapability.PUBLISH_CONTENT],
        resource_scope=ResourceScope("brand:aura"),
        authorizer_identity="HUMAN_OPERATOR",
        decision_reference="REF_01",
        nonce="nonce_unique_123",
    )

    guard.check_and_record_authorization(auth)

    with pytest.raises(ReplayExecutionError):
        guard.check_and_record_authorization(auth)

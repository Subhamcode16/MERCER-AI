"""
Unit tests for StudioProviderRuntime subordinate to Phase 13 controls.
"""

import pytest
from src.studio_intelligence.provider_runtime import StudioProviderRuntime
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.studio_intelligence.exceptions import ProviderRuntimeError


def test_provider_runtime_authorization_enforcement():
    runtime = StudioProviderRuntime()
    cap = ExecutionCapability.PUBLISH_CONTENT

    invalid_auth = AuthorizationRecord(
        authorization_id="auth_inv",
        request_id="req_inv",
        authorized_capabilities=[cap],
        resource_scope=ResourceScope("client:nocap"),
        authorizer_identity="HUMAN_OPERATOR_USER",
        decision_reference="dec_ref",
        revoked=True,  # Revoked authorization
    )

    with pytest.raises(ProviderRuntimeError, match="Provider operation rejected"):
        runtime.execute_provider_action(
            client_id="client_nocap",
            action_name="publish_post",
            capability=cap,
            auth_record=invalid_auth,
            payload={"content": "test"},
            idempotency_key="key_1",
        )

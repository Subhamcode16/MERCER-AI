"""
Unit tests for Phase 13 Mock Sandbox Social Provider.
"""

import pytest

from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.mock_social_provider import MockSocialProvider
from src.integration_boundary.models import (
    ProviderEnvironment,
    ExternalRequest,
    CredentialReference,
    IntegrationOutcomeClass,
)
from src.integration_boundary.exceptions import ExternalTimeoutError, ExternalOperationRejectedError


def test_mock_social_provider_execution():
    provider = MockSocialProvider()
    cred_ref = CredentialReference("ref_1", "mock_social", ProviderEnvironment.SANDBOX)

    req = ExternalRequest(
        request_id="req_01",
        operation_name="create_draft",
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope_string="campaign:nocap",
        payload={"text": "Draft content"},
        idempotency_key="idem_01",
        action_hash="hash_01",
        mission_id="m_01",
        authorization_id="auth_01",
    )

    res = provider.execute(req, cred_ref, "OPAQUE_SECRET")
    assert res.outcome_class == IntegrationOutcomeClass.SUCCESS
    assert "draft_id" in res.output_data


def test_mock_social_provider_timeout_simulation():
    provider = MockSocialProvider()
    provider.simulate_timeout = True
    cred_ref = CredentialReference("ref_1", "mock_social", ProviderEnvironment.SANDBOX)

    req = ExternalRequest(
        request_id="req_02",
        operation_name="create_draft",
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope_string="campaign:nocap",
        payload={},
        idempotency_key="idem_02",
        action_hash="hash_02",
        mission_id="m_01",
        authorization_id="auth_01",
    )

    with pytest.raises(ExternalTimeoutError):
        provider.execute(req, cred_ref, "OPAQUE_SECRET")

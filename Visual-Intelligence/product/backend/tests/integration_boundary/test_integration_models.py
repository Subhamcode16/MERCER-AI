"""
Unit tests for Phase 13 Integration Boundary Immutable Models.
"""

import pytest

from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.models import (
    ProviderEnvironment,
    CredentialReference,
    ExternalOperation,
    ExternalRequest,
    ExternalResponse,
    IntegrationOutcomeClass,
)
from src.integration_boundary.exceptions import IntegrationBoundaryError


def test_credential_reference_validation():
    ref = CredentialReference("ref_01", "mock_social", ProviderEnvironment.SANDBOX)
    assert ref.reference_id == "ref_01"
    assert ref.environment == ProviderEnvironment.SANDBOX

    with pytest.raises(IntegrationBoundaryError):
        CredentialReference("", "mock_social", ProviderEnvironment.SANDBOX)


def test_external_operation_validation():
    op = ExternalOperation("create_draft", "mock_social", ExecutionCapability.CREATE_DRAFT)
    assert op.operation_name == "create_draft"
    assert op.mapped_capability == ExecutionCapability.CREATE_DRAFT

    with pytest.raises(IntegrationBoundaryError):
        ExternalOperation("", "mock_social", ExecutionCapability.CREATE_DRAFT)


def test_external_request_validation():
    req = ExternalRequest(
        request_id="req_01",
        operation_name="create_draft",
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        capability=ExecutionCapability.CREATE_DRAFT,
        resource_scope_string="campaign:nocap",
        payload={"text": "Hello"},
        idempotency_key="idem_01",
        action_hash="hash_01",
        mission_id="m_01",
        authorization_id="auth_01",
    )
    assert req.compute_request_hash() is not None

    with pytest.raises(IntegrationBoundaryError):
        ExternalRequest(
            request_id="",
            operation_name="create_draft",
            provider_id="mock_social",
            environment=ProviderEnvironment.SANDBOX,
            capability=ExecutionCapability.CREATE_DRAFT,
            resource_scope_string="campaign:nocap",
            payload={},
            idempotency_key="idem_01",
            action_hash="hash_01",
            mission_id="m_01",
            authorization_id="auth_01",
        )

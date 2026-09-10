"""
Unit tests for Phase 13 Outcome Reconciliation Engine.
"""

import pytest

from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.models import (
    ProviderEnvironment,
    ExternalRequest,
    ExternalResponse,
    IntegrationOutcomeClass,
)
from src.integration_boundary.reconciliation import ReconciliationEngine
from src.integration_boundary.exceptions import ReconciliationTamperError


def test_reconciliation_success():
    req = ExternalRequest(
        request_id="req_recon_01",
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

    res = ExternalResponse(
        request_id="req_recon_01",
        provider_transaction_id="tx_01",
        outcome_class=IntegrationOutcomeClass.SUCCESS,
        output_data={"draft_id": "d1"},
    )

    outcome = ReconciliationEngine.reconcile_execution(req, res)
    assert outcome.reconciled is True
    assert outcome.provider_transaction_id == "tx_01"


def test_reconciliation_tamper_mismatch_rejection():
    req = ExternalRequest(
        request_id="req_recon_01",
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

    # Response has mismatched request_id
    res_tampered = ExternalResponse(
        request_id="req_OTHER",
        provider_transaction_id="tx_01",
        outcome_class=IntegrationOutcomeClass.SUCCESS,
        output_data={},
    )

    with pytest.raises(ReconciliationTamperError):
        ReconciliationEngine.reconcile_execution(req, res_tampered)

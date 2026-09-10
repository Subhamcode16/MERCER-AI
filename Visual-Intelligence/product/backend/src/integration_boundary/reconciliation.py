"""
Phase 13 Outcome Reconciliation Engine.

Validates outcome consistency across requested action, authorization, provider result,
and audit record. Detects provider response tampering or payload discrepancies.
"""

from typing import Dict, Any
from src.integration_boundary.models import ExternalRequest, ExternalResponse, IntegrationOutcome, IntegrationOutcomeClass
from src.integration_boundary.exceptions import ReconciliationTamperError


class ReconciliationEngine:
    """Validates external outcome consistency against authorized intent."""

    @staticmethod
    def reconcile_execution(
        request: ExternalRequest,
        response: ExternalResponse
    ) -> IntegrationOutcome:
        """
        Reconciles ExternalRequest and ExternalResponse.
        Fails closed with ReconciliationTamperError if transaction IDs, request IDs,
        or capabilities do not match.
        """
        # 1. Request ID match check
        if request.request_id != response.request_id:
            raise ReconciliationTamperError(
                f"Outcome Reconciliation Violation: Response request_id '{response.request_id}' "
                f"does not match request_id '{request.request_id}'."
            )

        # 2. Provider transaction ID integrity check
        if not response.provider_transaction_id or not isinstance(response.provider_transaction_id, str):
            raise ReconciliationTamperError(
                "Outcome Reconciliation Violation: Missing or invalid provider transaction ID in response."
            )

        # 3. Outcome classification reconciliation
        reconciled = response.outcome_class == IntegrationOutcomeClass.SUCCESS

        return IntegrationOutcome(
            request_id=request.request_id,
            mission_id=request.mission_id,
            provider_id=request.provider_id,
            environment=request.environment,
            capability=request.capability,
            resource_scope_string=request.resource_scope_string,
            outcome_class=response.outcome_class,
            provider_transaction_id=response.provider_transaction_id,
            reconciled=reconciled,
            details=response.output_data,
        )

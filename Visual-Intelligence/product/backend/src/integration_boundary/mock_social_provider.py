"""
Phase 13 Mock Sandbox Social Provider.

Deterministic test provider representing a social platform. Local state only, zero external calls.
"""

from typing import Dict, List, Any
import uuid

from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.models import (
    ProviderEnvironment,
    ExternalOperation,
    ExternalRequest,
    ExternalResponse,
    IntegrationOutcomeClass,
    CredentialReference,
)
from src.integration_boundary.provider import BaseProviderAdapter
from src.integration_boundary.exceptions import ExternalTimeoutError, ExternalOperationRejectedError


class MockSocialProvider(BaseProviderAdapter):
    """Deterministic mock provider for social publishing & scheduling in sandbox/test mode."""

    def __init__(self, provider_id: str = "mock_social", environment: ProviderEnvironment = ProviderEnvironment.SANDBOX):
        self._provider_id = provider_id
        self._environment = environment

        # State storage
        self.drafts: Dict[str, Dict[str, Any]] = {}
        self.published_posts: List[Dict[str, Any]] = []
        self.scheduled_posts: List[Dict[str, Any]] = []

        # Failure flags for testing
        self.simulate_timeout: bool = False
        self.simulate_rejection: bool = False

    @property
    def provider_id(self) -> str:
        return self._provider_id

    @property
    def environment(self) -> ProviderEnvironment:
        return self._environment

    def supported_operations(self) -> List[ExternalOperation]:
        return [
            ExternalOperation("create_draft", self._provider_id, ExecutionCapability.CREATE_DRAFT),
            ExternalOperation("edit_draft", self._provider_id, ExecutionCapability.EDIT_DRAFT),
            ExternalOperation("read_analytics", self._provider_id, ExecutionCapability.READ_ANALYTICS),
            ExternalOperation("schedule_content", self._provider_id, ExecutionCapability.SCHEDULE_CONTENT),
            ExternalOperation("publish_content", self._provider_id, ExecutionCapability.PUBLISH_CONTENT),
        ]

    def execute(
        self,
        request: ExternalRequest,
        credential_reference: CredentialReference,
        opaque_secret: str
    ) -> ExternalResponse:
        if self.simulate_timeout:
            raise ExternalTimeoutError(f"Mock provider '{self._provider_id}' timed out during operation '{request.operation_name}'.")

        if self.simulate_rejection:
            raise ExternalOperationRejectedError(f"Mock provider '{self._provider_id}' rejected operation '{request.operation_name}'.")

        tx_id = f"tx_{self._provider_id}_{uuid.uuid4().hex[:8]}"

        op = request.operation_name.lower().strip()
        out_data: Dict[str, Any] = {}

        if op == "create_draft":
            draft_id = f"draft_{uuid.uuid4().hex[:6]}"
            self.drafts[draft_id] = request.payload
            out_data = {"draft_id": draft_id, "status": "DRAFT_CREATED", "payload": request.payload}

        elif op == "edit_draft":
            draft_id = request.payload.get("draft_id", "draft_01")
            self.drafts[draft_id] = request.payload
            out_data = {"draft_id": draft_id, "status": "DRAFT_UPDATED", "payload": request.payload}

        elif op == "read_analytics":
            out_data = {"metrics": {"impressions": 10500, "engagement_rate": 0.042, "reach": 8200}}

        elif op == "schedule_content":
            sched_item = {"request_id": request.request_id, "payload": request.payload}
            self.scheduled_posts.append(sched_item)
            out_data = {"schedule_id": f"sched_{uuid.uuid4().hex[:6]}", "status": "SCHEDULED"}

        elif op == "publish_content":
            pub_item = {"request_id": request.request_id, "payload": request.payload}
            self.published_posts.append(pub_item)
            out_data = {"post_id": f"post_{uuid.uuid4().hex[:6]}", "status": "PUBLISHED"}

        else:
            return ExternalResponse(
                request_id=request.request_id,
                provider_transaction_id=tx_id,
                outcome_class=IntegrationOutcomeClass.REJECTED,
                output_data={},
                error_message=f"Unsupported operation '{request.operation_name}'",
            )

        return ExternalResponse(
            request_id=request.request_id,
            provider_transaction_id=tx_id,
            outcome_class=IntegrationOutcomeClass.SUCCESS,
            output_data=out_data,
        )

    def health(self) -> Dict[str, Any]:
        return {
            "provider_id": self._provider_id,
            "environment": self._environment.value,
            "status": "HEALTHY",
            "active_drafts": len(self.drafts),
            "published_count": len(self.published_posts),
        }

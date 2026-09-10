"""
Phase 13 Integration Boundary Immutable Data Models.

Defines data contracts for external operations, environments, opaque credential references,
requests, responses, and outcome classifications. Raw secrets are strictly prohibited.
"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, Optional, Set

from src.execution_control.capability_models import ExecutionCapability, validate_capability_string
from src.integration_boundary.exceptions import IntegrationBoundaryError


class ProviderEnvironment(Enum):
    """Execution environment tier for external integration."""
    TEST = "TEST"
    SANDBOX = "SANDBOX"
    DRY_RUN = "DRY_RUN"
    LIVE = "LIVE"


class IntegrationOutcomeClass(Enum):
    """Classified result status of an external operation execution."""
    SUCCESS = "SUCCESS"
    REJECTED = "REJECTED"
    RATE_LIMITED = "RATE_LIMITED"
    TIMEOUT = "TIMEOUT"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    FAILED = "FAILED"


@dataclass(frozen=True)
class CredentialReference:
    """Opaque reference handle to provider credentials. Contains NO raw secret material."""
    reference_id: str
    provider_id: str
    environment: ProviderEnvironment
    allowed_capabilities: Set[str] = field(default_factory=set)

    def __post_init__(self):
        if not self.reference_id or not isinstance(self.reference_id, str):
            raise IntegrationBoundaryError("CredentialReference reference_id must be a non-empty string.")
        if not self.provider_id or not isinstance(self.provider_id, str):
            raise IntegrationBoundaryError("CredentialReference provider_id must be a non-empty string.")


@dataclass(frozen=True)
class ExternalOperation:
    """Definition of a specific external operation exposed by a provider adapter."""
    operation_name: str
    provider_id: str
    mapped_capability: ExecutionCapability
    requires_idempotency: bool = True

    def __post_init__(self):
        if not self.operation_name or not isinstance(self.operation_name, str):
            raise IntegrationBoundaryError("ExternalOperation operation_name must be a non-empty string.")
        if not self.provider_id or not isinstance(self.provider_id, str):
            raise IntegrationBoundaryError("ExternalOperation provider_id must be a non-empty string.")


@dataclass(frozen=True)
class ExternalRequest:
    """Request payload sent to an external provider adapter."""
    request_id: str
    operation_name: str
    provider_id: str
    environment: ProviderEnvironment
    capability: ExecutionCapability
    resource_scope_string: str
    payload: Dict[str, Any]
    idempotency_key: str
    action_hash: str
    mission_id: str
    authorization_id: str

    def __post_init__(self):
        if not self.request_id or type(self.request_id) is not str:
            raise IntegrationBoundaryError("ExternalRequest request_id must be a non-empty string.")
        if not self.operation_name or type(self.operation_name) is not str:
            raise IntegrationBoundaryError("ExternalRequest operation_name must be a non-empty string.")
        if not self.idempotency_key or type(self.idempotency_key) is not str:
            raise IntegrationBoundaryError("ExternalRequest idempotency_key must be a non-empty string.")

    def compute_request_hash(self) -> str:
        """Computes SHA-256 digest of canonical request parameters."""
        canonical = {
            "request_id": self.request_id,
            "operation_name": self.operation_name,
            "provider_id": self.provider_id,
            "environment": self.environment.value,
            "capability": self.capability.value if hasattr(self.capability, "value") else str(self.capability),
            "resource_scope_string": self.resource_scope_string,
            "idempotency_key": self.idempotency_key,
            "action_hash": self.action_hash,
            "mission_id": self.mission_id,
            "authorization_id": self.authorization_id,
        }
        return hashlib.sha256(json.dumps(canonical, sort_keys=True).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExternalResponse:
    """Response returned by an external provider adapter."""
    request_id: str
    provider_transaction_id: str
    outcome_class: IntegrationOutcomeClass
    output_data: Dict[str, Any]
    error_message: Optional[str] = None
    executed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.request_id or type(self.request_id) is not str:
            raise IntegrationBoundaryError("ExternalResponse request_id must be a non-empty string.")
        if not self.provider_transaction_id or type(self.provider_transaction_id) is not str:
            raise IntegrationBoundaryError("ExternalResponse provider_transaction_id must be a non-empty string.")


@dataclass(frozen=True)
class IntegrationOutcome:
    """Final reconciled outcome summary of an integrated external tool execution."""
    request_id: str
    mission_id: str
    provider_id: str
    environment: ProviderEnvironment
    capability: ExecutionCapability
    resource_scope_string: str
    outcome_class: IntegrationOutcomeClass
    provider_transaction_id: str
    reconciled: bool
    details: Dict[str, Any]

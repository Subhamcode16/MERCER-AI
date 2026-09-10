"""
Phase 13 Abstract Base Provider Contract.

Defines mandatory interface for all external tool and platform integration adapters.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any

from src.integration_boundary.models import (
    ProviderEnvironment,
    ExternalOperation,
    ExternalRequest,
    ExternalResponse,
    CredentialReference,
)


class BaseProviderAdapter(ABC):
    """Abstract base class for external integration adapters."""

    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Returns unique provider identifier."""
        pass

    @property
    @abstractmethod
    def environment(self) -> ProviderEnvironment:
        """Returns adapter environment tier."""
        pass

    @abstractmethod
    def supported_operations(self) -> List[ExternalOperation]:
        """Returns list of supported external operations."""
        pass

    @abstractmethod
    def execute(
        self,
        request: ExternalRequest,
        credential_reference: CredentialReference,
        opaque_secret: str
    ) -> ExternalResponse:
        """Executes an external operation against the provider adapter."""
        pass

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Returns health telemetry status for provider adapter."""
        pass

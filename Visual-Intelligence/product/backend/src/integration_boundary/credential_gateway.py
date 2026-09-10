"""
Phase 13 Credential Gateway.

Provides opaque credential reference handles for provider adapters.
Enforces INV-13-003 (Credential Non-Authority) and INV-13-004 (Credential Isolation).
Credential access MUST occur strictly AFTER human authorization validation.
"""

from typing import Dict, Optional, Set
from src.integration_boundary.models import CredentialReference, ProviderEnvironment
from src.integration_boundary.exceptions import CredentialAccessViolationError, IntegrationBoundaryError


class CredentialGateway:
    """Narrow interface managing opaque credential reference handles."""

    def __init__(self):
        # provider_id -> Dict[env_str, CredentialReference]
        self._references: Dict[str, Dict[str, CredentialReference]] = {}
        # Stores secret payloads in isolated in-memory memory (never exposed in strings/logs)
        self._opaque_store: Dict[str, str] = {}

    def register_credential_handle(
        self,
        provider_id: str,
        environment: ProviderEnvironment,
        reference_id: str,
        secret_handle: str,
        allowed_capabilities: Optional[Set[str]] = None,
    ) -> CredentialReference:
        """Registers an opaque credential reference handle for test sandbox providers."""
        if not provider_id or not reference_id or not secret_handle:
            raise IntegrationBoundaryError("Credential registration requires non-empty provider_id, reference_id, and secret_handle.")

        ref = CredentialReference(
            reference_id=reference_id,
            provider_id=provider_id,
            environment=environment,
            allowed_capabilities=allowed_capabilities or set(),
        )

        if provider_id not in self._references:
            self._references[provider_id] = {}

        self._references[provider_id][environment.value] = ref
        self._opaque_store[reference_id] = secret_handle
        return ref

    def get_credential_reference(
        self,
        provider_id: str,
        environment: ProviderEnvironment,
        authorization_verified: bool = False
    ) -> CredentialReference:
        """
        Retrieves opaque CredentialReference.
        MUST fail closed if authorization_verified is False (INV-13-004).
        """
        if not authorization_verified:
            raise CredentialAccessViolationError(
                f"Credential Access Violation (INV-13-004): Cannot retrieve credentials for provider '{provider_id}' without prior verified human authorization."
            )

        provider_refs = self._references.get(provider_id)
        if not provider_refs:
            raise CredentialAccessViolationError(f"No credentials configured for provider '{provider_id}'.")

        ref = provider_refs.get(environment.value)
        if not ref:
            raise CredentialAccessViolationError(
                f"No credentials found for provider '{provider_id}' in environment '{environment.value}'."
            )

        return ref

    def get_opaque_secret(self, reference: CredentialReference, authorization_verified: bool = False) -> str:
        """
        Retrieves secret payload for provider invocation.
        Requires explicit prior authorization verification.
        """
        if not authorization_verified:
            raise CredentialAccessViolationError(
                f"Credential Non-Authority Violation (INV-13-003): Possession of credential handle '{reference.reference_id}' does not grant authorization."
            )

        secret = self._opaque_store.get(reference.reference_id)
        if not secret:
            raise CredentialAccessViolationError(f"Opaque secret handle '{reference.reference_id}' not found.")
        return secret

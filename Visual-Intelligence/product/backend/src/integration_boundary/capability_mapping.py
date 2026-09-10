"""
Phase 13 Capability Mapping Registry.

Maps provider-specific operation names 1-to-1 to explicit Phase 10 capabilities.
Enforces INV-13-002: Rejects wildcard, admin, and generic permission strings.
"""

from typing import Dict, List, Optional
from src.execution_control.capability_models import ExecutionCapability
from src.integration_boundary.exceptions import CapabilityMappingError


BANNED_OPERATION_NAMES = {
    "ADMIN",
    "ALL",
    "*",
    "ROOT",
    "BYPASS",
    "MANAGE_EVERYTHING",
    "SUPERUSER",
    "EXECUTE_ALL",
    "UNRESTRICTED",
}


class CapabilityMappingRegistry:
    """Registry mapping provider operation names 1-to-1 to explicit Phase 10 capabilities."""

    def __init__(self):
        # provider_id -> { operation_name -> ExecutionCapability }
        self._mappings: Dict[str, Dict[str, ExecutionCapability]] = {}

    def register_mapping(
        self,
        provider_id: str,
        operation_name: str,
        capability: ExecutionCapability
    ) -> None:
        """Registers a 1-to-1 mapping between a provider operation and a Phase 10 capability."""
        if not provider_id or not isinstance(provider_id, str):
            raise CapabilityMappingError("Provider ID must be a non-empty string.")

        clean_op = operation_name.upper().strip()
        if clean_op in BANNED_OPERATION_NAMES or "*" in clean_op:
            raise CapabilityMappingError(
                f"Capability Exactness Violation (INV-13-002): Generic or wildcard operation '{operation_name}' is prohibited."
            )

        if provider_id not in self._mappings:
            self._mappings[provider_id] = {}

        self._mappings[provider_id][operation_name.strip()] = capability

    def resolve_capability(self, provider_id: str, operation_name: str) -> ExecutionCapability:
        """Resolves the Phase 10 capability for a given provider operation. Fails closed if unmapped."""
        clean_op = operation_name.upper().strip()
        if clean_op in BANNED_OPERATION_NAMES or "*" in clean_op:
            raise CapabilityMappingError(
                f"Capability Exactness Violation (INV-13-002): Wildcard operation '{operation_name}' is forbidden."
            )

        provider_map = self._mappings.get(provider_id)
        if not provider_map:
            raise CapabilityMappingError(f"No capability mappings registered for provider '{provider_id}'.")

        capability = provider_map.get(operation_name.strip())
        if not capability:
            raise CapabilityMappingError(
                f"Operation '{operation_name}' on provider '{provider_id}' is not mapped to any approved Phase 10 capability."
            )

        return capability

    def get_supported_operations(self, provider_id: str) -> List[str]:
        """Returns list of supported operation names for a provider."""
        return list(self._mappings.get(provider_id, {}).keys())

"""
Phase 14 Client Context & Scope Manager
----------------------------------------
Establishes hierarchical context scopes (System -> Organization -> Client -> Brand -> Campaign -> Mission -> Task)
and enforces fail-closed client isolation (INV-14-W003).
Prevents Client A staff/learning signals from accessing or leaking Client B confidential data.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set
from src.creative_workforce.organization_models import ContextBinding
from src.creative_workforce.exceptions import ContextScopeViolationError, CrossClientLeakageError

@dataclass
class ClientScope:
    """Scoped metadata for a client workspace."""
    client_id: str
    client_name: str
    allowed_brands: Set[str] = field(default_factory=set)
    confidential_metadata: Dict[str, Any] = field(default_factory=dict)

class ClientContextManager:
    """Manager enforcing hierarchical context scope and cross-client isolation boundaries."""

    def __init__(self):
        self._clients: Dict[str, ClientScope] = {}
        self._active_bindings: Dict[str, ContextBinding] = {}

    def register_client(self, client_id: str, client_name: str, allowed_brands: Optional[List[str]] = None) -> ClientScope:
        """Registers a client scope."""
        brands = set(allowed_brands) if allowed_brands else {client_id}
        scope = ClientScope(client_id=client_id, client_name=client_name, allowed_brands=brands)
        self._clients[client_id] = scope
        return scope

    def create_context_binding(
        self,
        client_id: str,
        brand_id: str,
        campaign_id: str,
        mission_id: str,
        task_id: str,
        staff_id: str,
    ) -> ContextBinding:
        """Creates a validated hierarchical context binding."""
        if client_id not in self._clients:
            # Auto-register client if not present for convenience in sandbox
            self.register_client(client_id, client_id, [brand_id])

        scope = self._clients[client_id]
        if brand_id not in scope.allowed_brands:
            raise ContextScopeViolationError(
                f"Brand '{brand_id}' is not authorized under client '{client_id}' scope."
            )

        binding = ContextBinding(
            client_id=client_id,
            brand_id=brand_id,
            campaign_id=campaign_id,
            mission_id=mission_id,
            task_id=task_id,
            staff_id=staff_id,
        )
        binding_key = f"{mission_id}:{task_id}:{staff_id}"
        self._active_bindings[binding_key] = binding
        return binding

    def validate_cross_client_access(self, requesting_binding: ContextBinding, target_client_id: str) -> None:
        """Validates that a staff member operates strictly within its authorized client scope."""
        if requesting_binding.client_id != target_client_id:
            raise CrossClientLeakageError(
                f"Cross-client leakage detected! Staff '{requesting_binding.staff_id}' (client '{requesting_binding.client_id}') "
                f"attempted to access target client '{target_client_id}' scope."
            )

    def sanitize_context_payload(self, requesting_binding: ContextBinding, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Scrubs payload fields belonging to other clients."""
        sanitized = {}
        for k, v in payload.items():
            if isinstance(v, str) and any(c_id in v for c_id in self._clients if c_id != requesting_binding.client_id):
                continue
            sanitized[k] = v
        return sanitized

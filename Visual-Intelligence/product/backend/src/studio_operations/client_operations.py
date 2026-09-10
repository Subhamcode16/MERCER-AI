"""
Phase 15 Client Operations Manager.
Manages persistent client operating contexts, brand bindings, and operational policies with strict cross-client isolation.
"""

from typing import Dict, List, Optional
from src.studio_operations.exceptions import ClientContextViolation
from src.studio_operations.studio_models import StudioClient, StudioBrand, ClientOperatingPolicy
from src.creative_workforce.client_context import ClientContextManager, ClientScope

class ClientOperationsManager:
    """Manages studio client records, brand bindings, and operational policies."""

    def __init__(self, workforce_context_manager: Optional[ClientContextManager] = None):
        self._clients: Dict[str, StudioClient] = {}
        self._brands: Dict[str, StudioBrand] = {}
        self._policies: Dict[str, ClientOperatingPolicy] = {}
        self._workforce_context_manager = workforce_context_manager or ClientContextManager()

    def create_client(self, client_id: str, name: str, industry: str) -> StudioClient:
        """Creates and registers a new studio client."""
        if client_id in self._clients:
            raise ClientContextViolation(f"Client '{client_id}' already exists.")
        
        client = StudioClient(client_id=client_id, name=name, industry=industry)
        self._clients[client_id] = client
        
        # Initialize default policy if none exists
        policy = ClientOperatingPolicy(
            policy_id=f"policy_{client_id}",
            client_id=client_id
        )
        self._policies[client_id] = policy

        # Register in Phase 14 workforce context manager
        self._workforce_context_manager.register_client(client_id, name)
        return client

    def bind_brand(self, brand_id: str, client_id: str, brand_name: str, visual_dna_summary: Optional[Dict] = None, tone_of_voice: str = "Modern, Professional") -> StudioBrand:
        """Binds a brand to a client context."""
        if client_id not in self._clients:
            raise ClientContextViolation(f"Client '{client_id}' not found.")
        if brand_id in self._brands:
            raise ClientContextViolation(f"Brand '{brand_id}' already exists.")

        brand = StudioBrand(
            brand_id=brand_id,
            client_id=client_id,
            brand_name=brand_name,
            visual_dna_summary=visual_dna_summary or {},
            tone_of_voice=tone_of_voice
        )
        self._brands[brand_id] = brand

        # Bind in workforce context manager
        scope = self._workforce_context_manager._clients.get(client_id)
        if scope:
            scope.allowed_brands.add(brand_id)
        else:
            self._workforce_context_manager.register_client(client_id, client_id, [brand_id])
        return brand

    def set_client_policy(self, policy: ClientOperatingPolicy) -> None:
        """Sets or updates a client's operating policy."""
        if policy.client_id not in self._clients:
            raise ClientContextViolation(f"Client '{policy.client_id}' not found.")
        self._policies[policy.client_id] = policy

    def get_client(self, requesting_client_id: str, target_client_id: str) -> StudioClient:
        """Retrieves a client record with strict fail-closed isolation check."""
        self.verify_client_access(requesting_client_id, target_client_id)
        return self._clients[target_client_id]

    def get_brand(self, requesting_client_id: str, brand_id: str) -> StudioBrand:
        """Retrieves a brand record with strict fail-closed isolation check."""
        if brand_id not in self._brands:
            raise ClientContextViolation(f"Brand '{brand_id}' not found.")
        brand = self._brands[brand_id]
        self.verify_client_access(requesting_client_id, brand.client_id)
        return brand

    def get_policy(self, requesting_client_id: str, target_client_id: str) -> ClientOperatingPolicy:
        """Retrieves a client policy with strict fail-closed isolation check."""
        self.verify_client_access(requesting_client_id, target_client_id)
        if target_client_id not in self._policies:
            raise ClientContextViolation(f"Policy for client '{target_client_id}' not found.")
        return self._policies[target_client_id]

    def verify_client_access(self, requesting_client_id: str, target_client_id: str) -> None:
        """Enforces INV-15-003: Fail-closed cross-client isolation."""
        if not requesting_client_id or not target_client_id:
            raise ClientContextViolation("requesting_client_id and target_client_id are required.")
        if requesting_client_id != target_client_id:
            raise ClientContextViolation(
                f"CROSS-CLIENT LEAKAGE ATTEMPT: Requesting client '{requesting_client_id}' cannot access target client '{target_client_id}'."
            )
        if target_client_id not in self._clients:
            raise ClientContextViolation(f"Target client '{target_client_id}' does not exist.")

    def get_client_summary(self, requesting_client_id: str) -> Dict:
        """Returns a read-only client summary."""
        client = self.get_client(requesting_client_id, requesting_client_id)
        client_brands = [b for b in self._brands.values() if b.client_id == requesting_client_id]
        policy = self._policies.get(requesting_client_id)

        return {
            "client_id": client.client_id,
            "name": client.name,
            "industry": client.industry,
            "status": client.status,
            "brands": [b.brand_name for b in client_brands],
            "policy": {
                "max_revisions": policy.max_revisions_override if policy else 3,
                "require_approval": policy.require_human_approval if policy else True,
                "allowed_platforms": policy.allowed_platforms if policy else [],
            }
        }

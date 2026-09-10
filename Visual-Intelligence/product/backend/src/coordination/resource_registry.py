"""
Phase 12 Shared Logical Resource Catalog.

Registers and catalogues logical shared system resources (AI staff capacity,
model token buckets, execution slots, social accounts, content calendar namespaces).
"""

import threading
from typing import Dict, List, Optional

from .models import ResourceDescriptor
from .exceptions import CoordinationPolicyViolation


class ResourceRegistry:
    """Registry catalog for shared logical resources."""

    def __init__(self):
        self._resources: Dict[str, ResourceDescriptor] = {}
        self._lock = threading.RLock()
        self._register_default_resources()

    def register_resource(self, descriptor: ResourceDescriptor) -> None:
        """Registers a logical resource descriptor."""
        with self._lock:
            if descriptor.resource_id in self._resources:
                raise CoordinationPolicyViolation(f"Resource '{descriptor.resource_id}' already registered.")
            self._resources[descriptor.resource_id] = descriptor

    def get_resource(self, resource_id: str) -> ResourceDescriptor:
        """Retrieves a resource descriptor by ID."""
        with self._lock:
            if resource_id not in self._resources:
                raise KeyError(f"Resource '{resource_id}' not found in registry.")
            return self._resources[resource_id]

    def list_resources(self) -> List[ResourceDescriptor]:
        """Returns all registered resource descriptors."""
        with self._lock:
            return list(self._resources.values())

    def _register_default_resources(self) -> None:
        """Populates baseline logical shared resources."""
        defaults = [
            ResourceDescriptor("staff:designer", "STAFF_SLOT", capacity=2, scope_string="staff:role:designer"),
            ResourceDescriptor("staff:strategist", "STAFF_SLOT", capacity=2, scope_string="staff:role:strategist"),
            ResourceDescriptor("staff:trend_analyst", "STAFF_SLOT", capacity=2, scope_string="staff:role:trend_analyst"),
            ResourceDescriptor("quota:model_tokens", "MODEL_TOKEN_QUOTA", capacity=1000000, scope_string="quota:tokens:global"),
            ResourceDescriptor("account:nocap_social", "SOCIAL_ACCOUNT", capacity=1, scope_string="account:nocap"),
            ResourceDescriptor("calendar:nocap_september", "CONTENT_CALENDAR", capacity=1, scope_string="calendar:nocap:2026-09"),
            ResourceDescriptor("slot:execution", "EXECUTION_SLOT", capacity=5, scope_string="execution:sandbox:slots"),
        ]
        for r in defaults:
            self._resources[r.resource_id] = r

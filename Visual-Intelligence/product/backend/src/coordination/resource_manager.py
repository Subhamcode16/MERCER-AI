"""
Phase 12 Thread-Safe Resource Manager.

Handles atomic resource reservations, capacity accounting, lease issuance via LeaseManager,
and resource releases across multi-mission workloads.
"""

import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

from .models import ResourceDescriptor, ResourceRequest, ResourceLease
from .resource_registry import ResourceRegistry
from .leases import LeaseManager
from .exceptions import ResourceUnavailable, ReservationExpired


class ResourceManager:
    """Thread-safe resource manager for logical shared resources."""

    def __init__(self, resource_registry: Optional[ResourceRegistry] = None):
        self.registry = resource_registry or ResourceRegistry()
        self.lease_manager = LeaseManager()
        self._allocations: Dict[str, int] = {}  # resource_id -> current allocated quantity
        self._active_leases: Dict[str, ResourceLease] = {}  # lease_id -> ResourceLease
        self._lock = threading.RLock()

    def allocate(
        self,
        request: ResourceRequest,
        current_time: Optional[datetime] = None
    ) -> ResourceLease:
        """Atomically checks capacity and reserves resource quantity, returning a ResourceLease."""
        with self._lock:
            self._purge_expired_leases(current_time)

            descriptor = self.registry.get_resource(request.resource_id)
            current_allocated = self._allocations.get(request.resource_id, 0)

            if current_allocated + request.quantity > descriptor.capacity:
                raise ResourceUnavailable(
                    f"Resource '{request.resource_id}' depleted ({current_allocated}+{request.quantity} > {descriptor.capacity})."
                )

            lease = self.lease_manager.issue_lease(
                mission_id=request.mission_id,
                resource_id=request.resource_id,
                quantity=request.quantity,
                duration_seconds=request.requested_duration_seconds,
                issued_at=current_time,
            )

            self._allocations[request.resource_id] = current_allocated + request.quantity
            self._active_leases[lease.lease_id] = lease
            return lease

    def release_lease(self, lease_id: str) -> None:
        """Releases an active lease and decrements allocated quantity."""
        with self._lock:
            if lease_id in self._active_leases:
                lease = self._active_leases.pop(lease_id)
                self.lease_manager.revoke_lease(lease_id)

                curr = self._allocations.get(lease.resource_id, 0)
                self._allocations[lease.resource_id] = max(0, curr - lease.quantity)

    def get_allocated_quantity(self, resource_id: str, current_time: Optional[datetime] = None) -> int:
        """Returns active allocated quantity for a resource after purging expired leases."""
        with self._lock:
            self._purge_expired_leases(current_time)
            return self._allocations.get(resource_id, 0)

    def _purge_expired_leases(self, current_time: Optional[datetime] = None) -> None:
        """Purges expired leases and restores available capacity."""
        now = current_time or datetime.now(timezone.utc)
        expired_ids = [
            l_id for l_id, lease in self._active_leases.items() if lease.is_expired(now)
        ]
        for l_id in expired_ids:
            lease = self._active_leases.pop(l_id)
            curr = self._allocations.get(lease.resource_id, 0)
            self._allocations[lease.resource_id] = max(0, curr - lease.quantity)

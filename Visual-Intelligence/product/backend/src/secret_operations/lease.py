"""
Phase 23 Time-Bounded Secret Lease Manager.
"""
import uuid
import time
import logging
from typing import Dict, Optional
from src.secret_operations.secret_models import SecretLease, CredentialDomain
from src.secret_operations.exceptions import LeaseExpiredError

logger = logging.getLogger(__name__)

class SecretLeaseManager:
    """Issues and enforces time-bounded, auto-expiring credential leases."""

    def __init__(self, default_ttl_seconds: float = 3600.0):
        self.default_ttl_seconds = default_ttl_seconds
        self._leases: Dict[str, SecretLease] = {}

    def issue_lease(self, secret_name: str, domain: CredentialDomain, consumer_service: str, ttl_seconds: Optional[float] = None) -> SecretLease:
        ttl = ttl_seconds or self.default_ttl_seconds
        now = time.time()
        lease = SecretLease(
            lease_id=str(uuid.uuid4()),
            secret_name=secret_name,
            domain=domain,
            consumer_service=consumer_service,
            created_at=now,
            expires_at=now + ttl,
            is_revoked=False
        )
        self._leases[lease.lease_id] = lease
        logger.info(f"Issued lease {lease.lease_id} for {secret_name} to {consumer_service} (TTL: {ttl}s)")
        return lease

    def validate_lease(self, lease_id: str) -> SecretLease:
        lease = self._leases.get(lease_id)
        if not lease or not lease.is_valid():
            logger.warning(f"Lease validation failed or expired for lease_id: {lease_id}")
            raise LeaseExpiredError(f"Secret lease {lease_id} is expired or invalid")
        return lease

    def revoke_lease(self, lease_id: str) -> None:
        if lease_id in self._leases:
            self._leases[lease_id].is_revoked = True
            logger.info(f"Revoked secret lease {lease_id}")

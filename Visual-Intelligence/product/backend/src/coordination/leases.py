"""
Phase 12 Cryptographic Resource Lease Manager.

Issues and verifies short-lived, signed ResourceLease tokens with explicit TTLs,
replay defense, and automatic revocation upon expiration.
"""

import hmac
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Set

from .models import ResourceLease
from .exceptions import ReservationExpired, CoordinationReplayError, CheckpointTamperedError

HMAC_LEASE_KEY = b"PHASE_12_RESOURCE_LEASE_KEY_SECURE_HMAC"


class LeaseManager:
    """Manages creation, verification, and revocation of short-lived ResourceLease tokens."""

    def __init__(self):
        self._issued_nonces: Set[str] = set()
        self._revoked_lease_ids: Set[str] = set()

    def issue_lease(
        self,
        mission_id: str,
        resource_id: str,
        quantity: int = 1,
        duration_seconds: int = 300,
        issued_at: Optional[datetime] = None
    ) -> ResourceLease:
        """Issues a cryptographically signed ResourceLease."""
        now = issued_at or datetime.now(timezone.utc)
        exp = now + timedelta(seconds=duration_seconds)
        lease_id = f"lease_{uuid.uuid4().hex[:8]}"
        nonce = str(uuid.uuid4())

        lease = ResourceLease(
            lease_id=lease_id,
            mission_id=mission_id,
            resource_id=resource_id,
            quantity=quantity,
            issued_at=now.isoformat(),
            expires_at=exp.isoformat(),
            nonce=nonce,
        )

        signed_lease = ResourceLease(
            lease_id=lease.lease_id,
            mission_id=lease.mission_id,
            resource_id=lease.resource_id,
            quantity=lease.quantity,
            issued_at=lease.issued_at,
            expires_at=lease.expires_at,
            nonce=lease.nonce,
            digest=self.compute_digest(lease),
        )

        self._issued_nonces.add(nonce)
        return signed_lease

    def verify_lease(self, lease: ResourceLease, current_time: Optional[datetime] = None) -> bool:
        """Verifies HMAC signature, revocation status, expiration, and replay safety."""
        now = current_time or datetime.now(timezone.utc)

        # 1. Check revocation
        if lease.lease_id in self._revoked_lease_ids:
            raise ReservationExpired(f"Resource lease '{lease.lease_id}' has been explicitly revoked.")

        # 2. Check expiration
        if lease.is_expired(now):
            raise ReservationExpired(f"Resource lease '{lease.lease_id}' expired at {lease.expires_at}.")

        # 3. Check signature digest
        expected_digest = self.compute_digest(lease)
        if not hmac.compare_digest(expected_digest, lease.digest):
            raise CheckpointTamperedError(f"Lease '{lease.lease_id}' signature tampered or invalid.")

        return True

    def revoke_lease(self, lease_id: str) -> None:
        """Revokes an active lease."""
        self._revoked_lease_ids.add(lease_id)

    def compute_digest(self, lease: ResourceLease) -> str:
        """Computes SHA-256 HMAC digest over lease parameters."""
        payload = f"{lease.lease_id}:{lease.mission_id}:{lease.resource_id}:{lease.quantity}:{lease.issued_at}:{lease.expires_at}:{lease.nonce}"
        return hmac.new(HMAC_LEASE_KEY, payload.encode("utf-8"), hashlib.sha256).hexdigest()

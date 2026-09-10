"""
Unit tests for Phase 12 Cryptographic Resource Lease Manager.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.coordination.leases import LeaseManager
from src.coordination.models import ResourceLease
from src.coordination.exceptions import ReservationExpired, CheckpointTamperedError


def test_lease_issuance_and_verification():
    mgr = LeaseManager()
    now = datetime.now(timezone.utc)

    lease = mgr.issue_lease("m1", "r1", duration_seconds=300, issued_at=now)
    assert mgr.verify_lease(lease, current_time=now) is True

    # Expired lease fails verification
    future = now + timedelta(seconds=350)
    with pytest.raises(ReservationExpired):
        mgr.verify_lease(lease, current_time=future)


def test_lease_tamper_detection():
    mgr = LeaseManager()
    now = datetime.now(timezone.utc)

    lease = mgr.issue_lease("m1", "r1", duration_seconds=300, issued_at=now)

    tampered = ResourceLease(
        lease_id=lease.lease_id,
        mission_id="m1_TAMPERED",
        resource_id=lease.resource_id,
        quantity=lease.quantity,
        issued_at=lease.issued_at,
        expires_at=lease.expires_at,
        nonce=lease.nonce,
        digest=lease.digest,
    )

    with pytest.raises(CheckpointTamperedError):
        mgr.verify_lease(tampered, current_time=now)

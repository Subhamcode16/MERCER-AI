"""
Unit tests for Phase 12 Append-Only Hash-Linked Coordination Audit Ledger.
"""

import pytest

from src.coordination.coordination_ledger import CoordinationLedger


def test_coordination_ledger_hash_chaining(tmp_path):
    ledger = CoordinationLedger(base_dir=str(tmp_path))

    ledger.record_coordination_event("MISSION_ADMITTED", "m1", "d1", "ADMITTED_OK")
    ledger.record_coordination_event("RESOURCE_RESERVED", "m1", "d2", "LEASE_GRANTED", resource_id="staff:designer")

    assert len(ledger.entries) == 2
    assert ledger.entries[1].previous_entry_hash == ledger.entries[0].entry_hash
    assert ledger.verify_ledger_integrity() is True

"""
Unit tests for Phase 15 Studio Operations Ledger.
"""

import pytest
import os
import shutil
from src.studio_operations.studio_ledger import StudioOperationsLedger

def test_studio_ledger_hash_chain(tmp_path):
    ledger_dir = str(tmp_path / "test_ledger")
    ledger = StudioOperationsLedger(ledger_dir=ledger_dir)

    e1 = ledger.record_event("client_nocap", "EVENT_1", {"key": "val1"})
    e2 = ledger.record_event("client_nocap", "EVENT_2", {"secret_token": "hidden_123"})

    assert e2.previous_hash == e1.current_hash
    assert e2.payload["secret_token"] == "[REDACTED]"
    assert ledger.verify_integrity() is True

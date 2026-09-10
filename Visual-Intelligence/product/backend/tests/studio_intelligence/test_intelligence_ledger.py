"""
Unit tests for StudioIntelligenceLedger SHA-256 hash integrity.
"""

import pytest
import shutil
import os
from src.studio_intelligence.intelligence_ledger import StudioIntelligenceLedger
from src.studio_intelligence.exceptions import IntelligenceLedgerError


def test_intelligence_ledger_hash_chain_and_verification(tmp_path):
    ledger_dir = str(tmp_path / "test_ledger")
    ledger = StudioIntelligenceLedger(ledger_dir=ledger_dir)

    e1 = ledger.append_event(
        event_type="OUTCOME_RECEIVED",
        client_id="client_nocap",
        payload={"obs_id": "obs_1"},
    )
    assert e1.sequence == 1
    assert e1.prev_hash == "GENESIS_PHASE18_INTELLIGENCE"

    e2 = ledger.append_event(
        event_type="STRATEGY_PROMOTED",
        client_id="client_nocap",
        payload={"cand_id": "cand_1"},
    )
    assert e2.sequence == 2
    assert e2.prev_hash == e1.entry_hash

    assert ledger.verify_chain_integrity() is True

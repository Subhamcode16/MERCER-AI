"""
Unit tests for Phase 17 Production Fabric Ledger.
"""

from src.production_fabric.production_ledger import ProductionFabricLedger

def test_production_ledger_hash_chain(tmp_path):
    ledger_dir = str(tmp_path / "prod_ledger")
    ledger = ProductionFabricLedger(ledger_dir=ledger_dir)

    e1 = ledger.record_entry("e1", "client_a", "WORK_ADMITTED", "item_1", {"title": "Title 1"})
    e2 = ledger.record_entry("e2", "client_a", "STATE_TRANSITION", "item_1", {"state": "IN_PRODUCTION"})

    assert e2.prev_hash == e1.hash
    assert ledger.verify_integrity() is True

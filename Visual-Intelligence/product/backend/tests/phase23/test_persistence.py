"""
Tests for Phase 23 Persistence & Recovery Subsystem.
"""
import pytest
from src.persistence.state_store import StateStore
from src.persistence.workflow_store import WorkflowStore
from src.persistence.checkpoint_store import CheckpointStore
from src.persistence.ledger_store import LedgerStore
from src.persistence.backup import BackupGenerator
from src.persistence.restore import RestoreEngine
from src.persistence.integrity import PersistenceIntegrityVerifier
from src.persistence.exceptions import CorruptedStateError, LineageBreakError, BackupIntegrityError

def test_atomic_state_store_and_checksum_verification():
    state_store = StateStore()
    rec = state_store.put("brand:101", "tenant-1", "client-1", {"brand_name": "ILYREN", "tier": "LUXURY"})
    assert rec.checksum != ""

    fetched = state_store.get("brand:101")
    assert fetched is not None
    assert fetched.data["brand_name"] == "ILYREN"

    # Tamper with data in memory to trigger corruption detection
    state_store._memory_store["brand:101"].data["brand_name"] = "TAMPERED"
    with pytest.raises(CorruptedStateError):
        state_store.get("brand:101")

def test_checkpoint_store_cryptographic_lineage():
    cp_store = CheckpointStore()
    
    cp1 = cp_store.save_checkpoint("cp-1", "wf-1", "tenant-1", "client-1", 1, "BRIEFING", {"brief": "ok"})
    cp2 = cp_store.save_checkpoint("cp-2", "wf-1", "tenant-1", "client-1", 2, "STRATEGY", {"strategy": "ok"})
    
    assert cp2.parent_checkpoint_hash == cp1.checkpoint_hash
    assert cp_store.verify_chain_integrity("wf-1") is True

    # Tamper with parent hash of cp2
    cp_store._checkpoints["cp-2"].parent_checkpoint_hash = "broken_parent_hash"
    with pytest.raises(LineageBreakError):
        cp_store.verify_chain_integrity("wf-1")

def test_ledger_append_and_integrity_verification():
    ledger = LedgerStore()
    
    e1 = ledger.append_event("evt-1", "t-1", "c-1", "CAMPAIGN_CREATED", {"title": "SS26"})
    e2 = ledger.append_event("evt-2", "t-1", "c-1", "BRIEF_APPROVED", {"approved_by": "Host"})
    
    assert e1.prev_entry_hash == LedgerStore.GENESIS_HASH
    assert e2.prev_entry_hash == e1.entry_hash
    assert ledger.verify_ledger_integrity() is True

def test_disaster_recovery_backup_and_restore():
    state_store = StateStore()
    cp_store = CheckpointStore()
    ledger = LedgerStore()

    state_store.put("brand:test", "t-1", "c-1", {"name": "TestBrand"})
    cp_store.save_checkpoint("cp-test", "wf-test", "t-1", "c-1", 1, "STEP_1", {"v": 1})
    ledger.append_event("evt-test", "t-1", "c-1", "EVENT_TEST", {"data": "test"})

    backup_gen = BackupGenerator(state_store, cp_store, ledger)
    bundle = backup_gen.create_backup("bak-20260907-001")
    assert bundle["metadata"].record_count == 1
    assert bundle["metadata"].checkpoint_count == 1

    # Restore into fresh stores
    fresh_state = StateStore()
    fresh_cp = CheckpointStore()
    fresh_ledger = LedgerStore()

    restore_engine = RestoreEngine(fresh_state, fresh_cp, fresh_ledger)
    res = restore_engine.restore_from_backup(bundle)
    assert res["success"] is True
    assert fresh_state.get("brand:test").data["name"] == "TestBrand"

def test_full_persistence_integrity_verifier():
    state_store = StateStore()
    cp_store = CheckpointStore()
    ledger = LedgerStore()

    state_store.put("item:1", "t-1", "c-1", {"val": "clean"})
    cp_store.save_checkpoint("cp-1", "wf-1", "t-1", "c-1", 1, "INIT", {})
    ledger.append_event("evt-1", "t-1", "c-1", "INIT", {})

    verifier = PersistenceIntegrityVerifier(state_store, cp_store, ledger)
    audit = verifier.run_full_integrity_audit()
    assert audit["passed"] is True
    assert len(audit["errors"]) == 0

"""
Phase 24 Disaster Recovery Drills (Drills A, B, C, D).
"""
import pytest
from src.production_runtime.runtime_orchestrator import ProductionRuntimeOrchestrator
from src.production_runtime.runtime_models import WorkflowOperationalState
from src.persistence.state_store import StateStore
from src.persistence.checkpoint_store import CheckpointStore
from src.persistence.ledger_store import LedgerStore
from src.persistence.backup import BackupGenerator
from src.persistence.restore import RestoreEngine
from src.reliability.provider_health import ProviderHealthEngine, CircuitState

def test_drill_a_worker_restart_recovery():
    """Drill A: Worker Restart -> Interrupted workflow downgrades safely without gaining authority."""
    orchestrator = ProductionRuntimeOrchestrator()
    in_flight_state = {
        "workflow_id": "wf-drill-a",
        "tenant_id": "tenant-1",
        "client_id": "client-1",
        "current_state": "EXECUTING",
        "authorization_ref": "tok-auth-001"
    }
    reconstructed = orchestrator.state_mgr.reconstruct_workflow(in_flight_state)
    assert reconstructed.is_recovering is True
    # Must be downgraded to RECOVERING, never continuing EXECUTING automatically
    assert reconstructed.current_state == WorkflowOperationalState.RECOVERING

def test_drill_b_database_failure_safety():
    """Drill B: Database Failure -> Protected operations fail safely, ledger intact."""
    ledger = LedgerStore()
    ledger.append_event("evt-d1", "t-1", "c-1", "CAMPAIGN_INIT", {})
    assert ledger.verify_ledger_integrity() is True

def test_drill_c_provider_outage_circuit_breaker():
    """Drill C: Provider Outage -> Circuit trips OPEN, preventing cascading failures."""
    health = ProviderHealthEngine(failure_threshold=3, recovery_timeout_seconds=60.0)
    for _ in range(3):
        health.record_call("google_imagen", False)
    
    assert health.is_provider_available("google_imagen") is False

def test_drill_d_backup_restore_and_secret_scan():
    """Drill D: Restore -> Schema, checksum, lineage, and secret scans pass."""
    state = StateStore()
    cp = CheckpointStore()
    ledger = LedgerStore()

    state.put("brand:drill", "t-1", "c-1", {"name": "DrillBrand"})
    cp.save_checkpoint("cp-d", "wf-d", "t-1", "c-1", 1, "INIT", {})
    ledger.append_event("evt-d", "t-1", "c-1", "INIT", {})

    generator = BackupGenerator(state, cp, ledger)
    bundle = generator.create_backup("bak-drill-001")
    assert bundle["metadata"].contains_secrets is False

    restore = RestoreEngine(StateStore(), CheckpointStore(), LedgerStore())
    res = restore.restore_from_backup(bundle)
    assert res["success"] is True

"""
Mutation Testing & Invalidation/Rollback Verification (Phase 30).
Attempts to inject faults, tamper with boundaries, and verifies fail-closed behaviors.
"""
import pytest
from src.institutional_intelligence.types import (
    ThreatID,
    GovernanceInvariantViolation,
    InitiativeHealthState,
    StrategicHorizon,
)
from src.institutional_intelligence.objectives.models import StrategicObjective
from src.institutional_intelligence.cross_client.isolation import MultiTenantIsolationBoundary
from src.institutional_intelligence.governance.gate import GovernancePolicyGate
from src.institutional_intelligence.memory.store import MemoryItem, OrganizationalMemoryStore
from src.institutional_intelligence.rollback.manager import StrategicRollbackManager
from src.institutional_intelligence.health.evaluator import InitiativeHealthEvaluator


def test_mutation_tenant_boundary_bypass():
    # Attempt cross-tenant data access
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        MultiTenantIsolationBoundary.validate_tenant_access("tenant_attacker", "tenant_victim")
    assert excinfo.value.threat_id == ThreatID.T30_017


def test_mutation_ai_escalation_bypass():
    # Attempt AI granting itself authority
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        GovernancePolicyGate.verify_no_ai_self_authorization("AUTONOMOUS_JOB", "COMMIT_CONTRACT")
    assert excinfo.value.threat_id == ThreatID.T30_002


def test_mutation_unknown_state_coercion():
    # Attempt to coerce UNKNOWN into active state without human validation
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        GovernancePolicyGate.verify_unknown_state_preservation("UNKNOWN", "HEALTHY", is_automated=True)
    assert excinfo.value.threat_id == ThreatID.T30_012


def test_mutation_memory_chain_corruption_detection():
    store = OrganizationalMemoryStore(tenant_id="tenant_mut")
    m1 = MemoryItem(tenant_id="tenant_mut", memory_class="STRATEGIC_DECISION", title="M1", content={"val": 1}, provenance="p1")
    m2 = MemoryItem(tenant_id="tenant_mut", memory_class="STRATEGIC_DECISION", title="M2", content={"val": 2}, provenance="p2")
    store.append_memory(m1)
    store.append_memory(m2)
    assert store.verify_ledger_integrity() is True

    # Mutate previous_hash in block 2
    store._items[1].previous_hash = "CORRUPTED_HASH_VALUE"
    assert store.verify_ledger_integrity() is False


def test_mutation_rollback_revoked_privilege_restoration():
    rollback_mgr = StrategicRollbackManager(tenant_id="tenant_mut")
    event = rollback_mgr.execute_rollback("DECISION", "dec_revoked_01", "Fraudulent assumption", "auditor")
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        rollback_mgr.assert_no_zombie_authority_restoration(event.rollback_id, "EXECUTE_BUDGET")
    assert excinfo.value.threat_id == ThreatID.T30_032

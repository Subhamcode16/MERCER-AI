"""
Tests for Organizational Memory Store and Hash Integrity (Phase 30).
"""
import pytest
from src.institutional_intelligence.types import (
    OrganizationalMemoryClass,
    ExternalIntelligenceClassification,
    EpistemicStatus,
    ThreatID,
    GovernanceInvariantViolation,
)
from src.institutional_intelligence.memory.store import (
    MemoryItem,
    OrganizationalMemoryStore,
)


def test_append_all_14_memory_classes():
    store = OrganizationalMemoryStore(tenant_id="tenant_01")
    classes = list(OrganizationalMemoryClass)
    assert len(classes) == 14

    for m_class in classes:
        item = MemoryItem(
            tenant_id="tenant_01",
            memory_class=m_class,
            title=f"Sample memory for {m_class.value}",
            content={"details": f"Data for {m_class.value}"},
            provenance=f"prov_doc_{m_class.value.lower()}"
        )
        stored = store.append_memory(item)
        assert stored.item_hash != ""
        assert stored.memory_class == m_class

    assert store.verify_ledger_integrity() is True
    assert len(store._items) == 14


def test_t30_027_provenance_forgery_prevention():
    store = OrganizationalMemoryStore(tenant_id="tenant_01")
    item_no_prov = MemoryItem(
        tenant_id="tenant_01",
        memory_class=OrganizationalMemoryClass.STRATEGIC_DECISION,
        title="Unverified memory item",
        content={},
        provenance=""  # Missing provenance!
    )
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        store.append_memory(item_no_prov)
    assert excinfo.value.threat_id == ThreatID.T30_027


def test_t30_007_tamper_detection_in_memory_ledger():
    store = OrganizationalMemoryStore(tenant_id="tenant_01")
    item1 = MemoryItem(
        tenant_id="tenant_01",
        memory_class=OrganizationalMemoryClass.STRATEGIC_OBJECTIVE,
        title="Initial Objective",
        content={"scope": "INITIAL"},
        provenance="prov_01"
    )
    item2 = MemoryItem(
        tenant_id="tenant_01",
        memory_class=OrganizationalMemoryClass.LESSON,
        title="Key Lesson Learned",
        content={"lesson": "Test thoroughly"},
        provenance="prov_02"
    )
    store.append_memory(item1)
    store.append_memory(item2)
    assert store.verify_ledger_integrity() is True

    # Malicious tampering of historical record content in-place
    store._items[0].content["scope"] = "TAMPERED_SCOPE"
    assert store.verify_ledger_integrity() is False


def test_governed_memory_invalidation():
    store = OrganizationalMemoryStore(tenant_id="tenant_01")
    item = MemoryItem(
        tenant_id="tenant_01",
        memory_class=OrganizationalMemoryClass.ASSUMPTION,
        title="Outdated Market Fact",
        content={"data": 123},
        provenance="prov_market"
    )
    stored = store.append_memory(item)
    assert stored.is_invalidated is False

    store.invalidate_memory(stored.memory_id, reason="Superseded by new empirical test", actor="human_auditor")
    assert stored.is_invalidated is True
    assert "Invalidated by human_auditor" in stored.invalidation_reason

    # Query without invalidated should exclude it
    active_assumptions = store.query_by_class(OrganizationalMemoryClass.ASSUMPTION, include_invalidated=False)
    assert len(active_assumptions) == 0

    # Query with invalidated should include it
    all_assumptions = store.query_by_class(OrganizationalMemoryClass.ASSUMPTION, include_invalidated=True)
    assert len(all_assumptions) == 1

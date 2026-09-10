"""
Unit & Integration Tests for Organizational Intelligence Graph & Strategic Signal Engine.
"""
import pytest
from src.creative_intelligence_network.graph import (
    OrganizationalIntelligenceGraph,
    GraphEntity,
    GraphRelationship,
    EntityType,
    RelationType,
    IntelligenceClassification,
    TenantAccessViolation,
)
from src.creative_intelligence_network.signals import (
    StrategicSignalEngine,
    SignalClass,
    EpistemicStatus,
    SignalLifecycle,
)


def test_graph_entity_creation_and_provenance():
    graph = OrganizationalIntelligenceGraph()
    entity = GraphEntity(
        entity_id="ENT-001",
        entity_type=EntityType.BRAND,
        tenant_id="TENANT-LUXE",
        classification=IntelligenceClassification.CLIENT_PRIVATE,
        name="Luxe Maison",
    )
    e_id = graph.add_entity(entity)
    assert e_id == "ENT-001"
    assert len(entity.provenance_hashes) > 0

    fetched = graph.get_entity("ENT-001", tenant_id="TENANT-LUXE")
    assert fetched is not None
    assert fetched.name == "Luxe Maison"


def test_cross_tenant_graph_isolation():
    graph = OrganizationalIntelligenceGraph()
    e1 = GraphEntity(
        entity_id="ENT-ALPHA",
        entity_type=EntityType.CAMPAIGN,
        tenant_id="TENANT-A",
        classification=IntelligenceClassification.CLIENT_PRIVATE,
        name="Campaign Alpha",
    )
    graph.add_entity(e1)

    # Attempting to fetch Tenant A's private entity with Tenant B's credentials should raise TenantAccessViolation
    with pytest.raises(TenantAccessViolation):
        graph.get_entity("ENT-ALPHA", tenant_id="TENANT-B")


def test_bidirectional_evidence_traversal():
    graph = OrganizationalIntelligenceGraph()
    camp = GraphEntity(
        entity_id="CAMP-101",
        entity_type=EntityType.CAMPAIGN,
        tenant_id="TENANT-A",
        classification=IntelligenceClassification.CLIENT_PRIVATE,
        name="Summer Campaign",
    )
    sig = GraphEntity(
        entity_id="SIG-201",
        entity_type=EntityType.STRATEGIC_SIGNAL,
        tenant_id="TENANT-A",
        classification=IntelligenceClassification.CLIENT_PRIVATE,
        name="Emerging Pattern",
    )
    rec = GraphEntity(
        entity_id="REC-301",
        entity_type=EntityType.RECOMMENDATION,
        tenant_id="TENANT-A",
        classification=IntelligenceClassification.CLIENT_PRIVATE,
        name="Strategy Shift",
    )

    graph.add_entity(camp)
    graph.add_entity(sig)
    graph.add_entity(rec)

    # Link: Camp -> Sig -> Rec
    graph.add_relationship(
        GraphRelationship(
            relationship_id="R1",
            source_id="CAMP-101",
            target_id="SIG-201",
            relation_type=RelationType.SUPPORTS,
            tenant_id="TENANT-A",
            classification=IntelligenceClassification.CLIENT_PRIVATE,
            scope="LUXURY_HERITAGE",
        )
    )
    graph.add_relationship(
        GraphRelationship(
            relationship_id="R2",
            source_id="SIG-201",
            target_id="REC-301",
            relation_type=RelationType.INFORMS,
            tenant_id="TENANT-A",
            classification=IntelligenceClassification.CLIENT_PRIVATE,
            scope="LUXURY_HERITAGE",
        )
    )

    chain = graph.traverse_evidence_chain("REC-301", tenant_id="TENANT-A")
    assert len(chain) == 2
    sources = [c[0].entity_id for c in chain]
    assert "SIG-201" in sources
    assert "CAMP-101" in sources


def test_signal_engine_emission_and_epistemic_invariants():
    engine = StrategicSignalEngine()
    
    # Invariant: Claiming experimental evidence without exp backing is automatically adjusted to observational correlation
    sig = engine.emit_signal(
        tenant_id="TENANT-LUXE",
        signal_class=SignalClass.EMERGING_PATTERN,
        scope="GEN_Z_DENIM",
        observed_pattern="High engagement with brutalist typography layout",
        method="HISTORICAL_CORRELATION",
        confidence=0.85,
        epistemic_status=EpistemicStatus.EXPERIMENTAL_EVIDENCE,  # No experiment in supporting evidence!
        supporting_evidence=["CAMP-OBS-01", "CAMP-OBS-02"],
    )

    assert sig.epistemic_status == EpistemicStatus.OBSERVATIONAL_CORRELATION
    assert len(sig.unknowns) > 0
    assert sig.provenance_hash != ""

    fetched = engine.get_signal(sig.signal_id, tenant_id="TENANT-LUXE")
    assert fetched is not None
    assert fetched.confidence == 0.85


def test_all_15_signal_classes():
    engine = StrategicSignalEngine()
    for s_class in SignalClass:
        sig = engine.emit_signal(
            tenant_id="TENANT-TEST",
            signal_class=s_class,
            scope="GENERAL",
            observed_pattern=f"Observed pattern for {s_class.value}",
            method="ANALYSIS",
            confidence=0.75,
            epistemic_status=EpistemicStatus.OBSERVATIONAL_CORRELATION,
        )
        assert sig.signal_class == s_class
        assert sig.lifecycle_state == SignalLifecycle.STRATEGIC_SIGNAL

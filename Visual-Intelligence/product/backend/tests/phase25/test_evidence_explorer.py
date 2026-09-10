"""
Phase 25 Evidence Explorer Tests.
"""
import pytest
from src.control_plane.models import OperatorRole
from src.control_plane.context import OperatorContext
from src.evidence_explorer.event_query import EvidenceEventQueryEngine
from src.evidence_explorer.lineage_query import EvidenceLineageQueryEngine
from src.evidence_explorer.integrity import EvidenceIntegrityVerifier
from src.evidence_explorer.export import EvidenceBundleExporter
from src.live_operations.live_ledger import LiveOperationsLedger
from src.live_operations.live_models import LiveEvidenceRecord, ProbeResult, ProbeStatus

def test_evidence_event_query():
    ledger = LiveOperationsLedger()
    rec1 = LiveEvidenceRecord(
        evidence_id="evi-01",
        correlation_id="corr-100",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        status=ProbeStatus.PASS
    )
    rec1.record_hash = rec1.compute_hash()
    ledger.append_evidence(rec1)

    query_engine = EvidenceEventQueryEngine(ledger=ledger)
    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    results = query_engine.query_events_by_correlation(ctx, "corr-100", "tenant_atelier", "client_alpha")
    assert len(results) == 1
    assert results[0].evidence_id == "evi-01"

def test_evidence_lineage_query():
    lineage_engine = EvidenceLineageQueryEngine()
    lineage_engine.register_node("art-01", None, "client_alpha", "hash-01")
    lineage_engine.register_node("art-02", "art-01", "client_alpha", "hash-02")

    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    dag = lineage_engine.trace_lineage(ctx, "art-02", "tenant_atelier", "client_alpha")
    assert len(dag) == 2
    assert dag[0]["artifact_id"] == "art-02"
    assert dag[1]["artifact_id"] == "art-01"

def test_evidence_bundle_export():
    ledger = LiveOperationsLedger()
    rec1 = LiveEvidenceRecord(
        evidence_id="evi-01",
        correlation_id="corr-100",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        status=ProbeStatus.PASS
    )
    rec1.record_hash = rec1.compute_hash()
    ledger.append_evidence(rec1)

    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )

    bundle = EvidenceBundleExporter.export_evidence_bundle(ctx, "tenant_atelier", "client_alpha", ledger.list_entries())
    assert bundle["total_records"] == 1
    assert "bundle_sha256" in bundle

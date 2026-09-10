"""
Tests for Phase 19 Knowledge Models, Dual-Namespace Graph, Provenance, and Confidentiality Filter.
"""

import pytest
from src.creative_intelligence.knowledge_models import (
    GraphNode, GraphEdge, InstitutionalPattern, ValidatedStrategy,
    WorkforceRecommendation, ProvenanceRecord
)
from src.creative_intelligence.knowledge_graph import InstitutionalKnowledgeGraph
from src.creative_intelligence.provenance import ProvenanceTracker
from src.creative_intelligence.generalization import ConfidentialityFilter
from src.creative_intelligence.exceptions import (
    ClientDataLeakageError, LineageBrokenError
)


def test_provenance_hash_chain(provenance_tracker):
    rec1 = provenance_tracker.create_record(
        source_phase="Phase18",
        evidence_hash="abc123hash",
        source_client_id="client_nocap"
    )
    assert rec1.provenance_hash != ""

    rec2 = provenance_tracker.create_record(
        source_phase="Phase19",
        evidence_hash="def456hash",
        parent_provenance_id=rec1.record_id
    )

    assert provenance_tracker.verify_chain(rec2.record_id) is True
    lineage = provenance_tracker.get_lineage(rec2.record_id)
    assert len(lineage) == 2


def test_dual_namespace_graph_isolation(knowledge_graph):
    client_node = GraphNode(
        node_id="c_node_1",
        namespace="client",
        node_type="Deliverable",
        attributes={"client_id": "client_alpha", "name": "Campaign A"}
    )
    knowledge_graph.add_node(client_node, client_id="client_alpha")

    # Attempting to add global node with raw client_id attribute must raise ClientDataLeakageError
    global_leak_node = GraphNode(
        node_id="g_node_leak",
        namespace="global",
        node_type="InstitutionalPattern",
        attributes={"client_id": "client_alpha", "pattern": "leak"}
    )
    with pytest.raises(ClientDataLeakageError):
        knowledge_graph.add_node(global_leak_node)


def test_confidentiality_filter_scrubbing(confidentiality_filter):
    raw_data = {
        "pattern_name": "Luxury Fashion Campaign",
        "client_name": "NOCAP Apparel",
        "contact_email": "ceo@nocapapparel.com",
        "structure": {
            "hero_banner": "Red Silk Dress",
            "notes": "Call client_nocap for signoff"
        }
    }

    filtered = confidentiality_filter.filter_attributes(raw_data)
    assert "client_name" not in filtered
    assert "contact_email" not in filtered
    assert "[ANONYMIZED_IDENTIFIER]" in filtered["structure"]["notes"]
    assert confidentiality_filter.validate_anonymization(filtered) is True

"""
Phase 19 - Institutional Memory Repository.

Provides unified interface for storing, querying, and indexing institutional knowledge assets,
client execution records, and global pattern structures.
"""

from typing import Dict, List, Any, Optional
from .knowledge_models import GraphNode, GraphEdge, InstitutionalPattern, ProvenanceRecord
from .knowledge_graph import InstitutionalKnowledgeGraph
from .provenance import ProvenanceTracker


class InstitutionalMemory:
    """Central store and query manager for institutional memory."""

    def __init__(self, knowledge_graph: InstitutionalKnowledgeGraph, provenance_tracker: ProvenanceTracker):
        self.graph = knowledge_graph
        self.provenance = provenance_tracker

    def record_client_artifact(
        self,
        client_id: str,
        artifact_id: str,
        artifact_type: str,
        attributes: Dict[str, Any],
        evidence_hash: str
    ) -> GraphNode:
        """Store client-scoped artifact node with provenance trace."""
        prov = self.provenance.create_record(
            source_client_id=client_id,
            source_phase="Phase18_StudioIntelligence",
            evidence_hash=evidence_hash
        )

        node = GraphNode(
            node_id=artifact_id,
            namespace="client",
            node_type=artifact_type,
            attributes={**attributes, "client_id": client_id},
            provenance_id=prov.record_id
        )

        return self.graph.add_node(node, client_id=client_id)

    def query_client_history(self, client_id: str) -> List[GraphNode]:
        """Query all client-scoped historical nodes."""
        return self.graph.get_client_nodes(client_id)

    def query_global_knowledge(self) -> List[GraphNode]:
        """Query all studio-global institutional knowledge nodes."""
        return self.graph.get_global_nodes()

    def get_provenance_trace(self, node_id: str) -> List[ProvenanceRecord]:
        """Fetch complete provenance trace for a knowledge node."""
        node = self.graph.get_node(node_id)
        if not node or not node.provenance_id:
            return []
        return self.provenance.get_lineage(node.provenance_id)

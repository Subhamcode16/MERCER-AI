"""
Phase 25 Knowledge Provenance and Source Attribution Graphs.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class KnowledgeSourceNode:
    node_id: str
    source_type: str # BRAND_ARCHIVE, EDITORIAL_DATASET, MCP_ORACLE, CRITIQUE_EVALUATION
    origin_uri: str
    hash_signature: str
    tenant_scope: str
    created_at: float

class ProvenanceGraphViewer:
    @staticmethod
    def build_provenance_graph(nodes: List[KnowledgeSourceNode]) -> Dict[str, Any]:
        return {
            "total_sources": len(nodes),
            "sources": [
                {
                    "node_id": n.node_id,
                    "type": n.source_type,
                    "hash": n.hash_signature,
                    "tenant_scope": n.tenant_scope
                }
                for n in nodes
            ]
        }

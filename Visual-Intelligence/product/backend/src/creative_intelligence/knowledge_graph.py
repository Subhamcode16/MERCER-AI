"""
Phase 19 - Dual-Namespace Institutional Knowledge Graph.

Maintains client-scoped ("client") and studio-global ("global") graph nodes and edges.
Enforces client isolation boundaries to prevent cross-client data leakage.
"""

from typing import Dict, List, Optional, Set, Any
from .knowledge_models import GraphNode, GraphEdge
from .exceptions import ClientDataLeakageError, CreativeIntelligenceError


class InstitutionalKnowledgeGraph:
    """Dual-namespace typed graph managing institutional memory nodes and directed edges."""

    def __init__(self):
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[str, GraphEdge] = {}
        self._adjacency: Dict[str, Set[str]] = {}  # source_node_id -> target_node_ids
        self._client_node_map: Dict[str, Set[str]] = {}  # client_id -> set of node_ids

    def add_node(self, node: GraphNode, client_id: Optional[str] = None) -> GraphNode:
        """Add a node into the graph with strict namespace validation."""
        if node.namespace == "client":
            if not client_id and "client_id" not in node.attributes:
                raise ClientDataLeakageError("Client namespace node must be associated with a client_id.")
            c_id = client_id or node.attributes.get("client_id")
            node.attributes["client_id"] = c_id
            if c_id not in self._client_node_map:
                self._client_node_map[c_id] = set()
            self._client_node_map[c_id].add(node.node_id)
        elif node.namespace == "global":
            # Global namespace nodes MUST NOT contain raw client identifiers in attributes
            for k in ["client_id", "client_name", "raw_client_data"]:
                if k in node.attributes:
                    raise ClientDataLeakageError(f"Global namespace node contains prohibited attribute '{k}'")
        else:
            raise CreativeIntelligenceError(f"Invalid namespace: {node.namespace}")

        self._nodes[node.node_id] = node
        if node.node_id not in self._adjacency:
            self._adjacency[node.node_id] = set()
        return node

    def add_edge(self, edge: GraphEdge) -> GraphEdge:
        """Add a directed edge between nodes while verifying namespace constraints."""
        if edge.source_node_id not in self._nodes or edge.target_node_id not in self._nodes:
            raise CreativeIntelligenceError("Edge source or target node does not exist in graph.")

        src_node = self._nodes[edge.source_node_id]
        tgt_node = self._nodes[edge.target_node_id]

        # Prevent client-A node from linking directly to client-B node across client namespaces
        if src_node.namespace == "client" and tgt_node.namespace == "client":
            src_client = src_node.attributes.get("client_id")
            tgt_client = tgt_node.attributes.get("client_id")
            if src_client and tgt_client and src_client != tgt_client:
                raise ClientDataLeakageError(
                    f"Direct edge between client '{src_client}' and client '{tgt_client}' prohibited."
                )

        self._edges[edge.edge_id] = edge
        self._adjacency[edge.source_node_id].add(edge.target_node_id)
        return edge

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return self._edges.get(edge_id)

    def get_client_nodes(self, client_id: str) -> List[GraphNode]:
        node_ids = self._client_node_map.get(client_id, set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]

    def get_global_nodes(self) -> List[GraphNode]:
        return [n for n in self._nodes.values() if n.namespace == "global"]

    def query_subgraph(
        self,
        start_node_id: str,
        max_depth: int = 2,
        requesting_client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Query subgraph starting from a node, enforcing client isolation filtering."""
        if start_node_id not in self._nodes:
            return {"nodes": [], "edges": []}

        visited_nodes: Set[str] = set()
        result_nodes: List[GraphNode] = []
        result_edges: List[GraphEdge] = []

        queue = [(start_node_id, 0)]
        visited_nodes.add(start_node_id)

        while queue:
            curr_id, depth = queue.pop(0)
            curr_node = self._nodes[curr_id]

            # Security Filter: If accessing client node, ensure requesting_client_id matches or is None for authorized studio query
            if curr_node.namespace == "client" and requesting_client_id:
                node_client = curr_node.attributes.get("client_id")
                if node_client and node_client != requesting_client_id:
                    continue  # Filter out unauthorized client node

            result_nodes.append(curr_node)

            if depth < max_depth:
                target_ids = self._adjacency.get(curr_id, set())
                for tid in target_ids:
                    # Find connecting edges
                    for e in self._edges.values():
                        if e.source_node_id == curr_id and e.target_node_id == tid:
                            result_edges.append(e)

                    if tid not in visited_nodes:
                        visited_nodes.add(tid)
                        queue.append((tid, depth + 1))

        return {"nodes": result_nodes, "edges": result_edges}

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

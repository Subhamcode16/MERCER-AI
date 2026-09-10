"""
Phase 25 Lineage DAG Traverser and Evidence Tracing.
"""
from typing import Dict, Any, List, Optional
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability
from src.control_plane.permissions import PermissionGuard

class EvidenceLineageQueryEngine:
    """Traverses visual artifact parent-child dependency DAGs."""

    def __init__(self):
        self._lineage_dag: Dict[str, Dict[str, Any]] = {}

    def register_node(self, artifact_id: str, parent_id: Optional[str], client_id: str, commitment_hash: str) -> None:
        self._lineage_dag[artifact_id] = {
            "artifact_id": artifact_id,
            "parent_id": parent_id,
            "client_id": client_id,
            "commitment_hash": commitment_hash
        }

    def trace_lineage(self, context: OperatorContext, artifact_id: str, tenant_id: str, client_id: str) -> List[Dict[str, Any]]:
        PermissionGuard.enforce_capability(context, OperatorCapability.VIEW_EVIDENCE)
        PermissionGuard.enforce_tenant_boundary(context, tenant_id, client_id)

        chain = []
        curr = artifact_id
        while curr and curr in self._lineage_dag:
            node = self._lineage_dag[curr]
            chain.append(node)
            curr = node.get("parent_id")
        return chain

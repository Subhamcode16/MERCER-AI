"""
Phase 25 Correlated Operational Event Query Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability
from src.control_plane.permissions import PermissionGuard
from src.live_operations.live_models import LiveEvidenceRecord
from src.live_operations.live_ledger import LiveOperationsLedger

class EvidenceEventQueryEngine:
    """Queries correlated chronological event streams from the cryptographic ledger."""

    def __init__(self, ledger: Optional[LiveOperationsLedger] = None):
        self.ledger = ledger or LiveOperationsLedger()

    def query_events_by_correlation(
        self,
        context: OperatorContext,
        correlation_id: str,
        tenant_id: str,
        client_id: Optional[str] = None
    ) -> List[LiveEvidenceRecord]:
        PermissionGuard.enforce_capability(context, OperatorCapability.VIEW_EVIDENCE)
        PermissionGuard.enforce_tenant_boundary(context, tenant_id, client_id or "*")

        all_entries = self.ledger.list_entries()
        results = []
        for e in all_entries:
            if e.correlation_id == correlation_id:
                if tenant_id == "*" or e.tenant_id == tenant_id:
                    if client_id is None or client_id == "*" or e.client_id == client_id:
                        results.append(e)
        return results

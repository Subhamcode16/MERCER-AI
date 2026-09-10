"""
Phase 14 Workflow Audit
-----------------------
Correlates gateway control plane actions across Phase 7, Phase 10, Phase 11, Phase 12,
and Phase 13 append-only ledgers while maintaining individual authority boundaries.
"""

from typing import Dict, List, Any, Optional
import time

from src.execution_control import ExecutionLedger
from src.mission_control import MissionLedger
from src.coordination import CoordinationLedger
from src.integration_boundary import IntegrationLedger

class WorkflowAuditCorrelator:
    """Service correlating audit ledger entries across system boundaries."""

    def __init__(
        self,
        exec_ledger: Optional[ExecutionLedger] = None,
        mission_ledger: Optional[MissionLedger] = None,
        coord_ledger: Optional[CoordinationLedger] = None,
        integration_ledger: Optional[IntegrationLedger] = None,
    ):
        self._exec_ledger = exec_ledger or ExecutionLedger()
        self._mission_ledger = mission_ledger or MissionLedger()
        self._coord_ledger = coord_ledger or CoordinationLedger()
        self._integration_ledger = integration_ledger or IntegrationLedger()

    def correlate_workflow_history(
        self, workflow_id: str, mission_id: str
    ) -> Dict[str, Any]:
        """Gathers and correlates audit trail entries across all Phase ledgers for a workflow/mission."""
        mission_entries = self._mission_ledger.get_history(mission_id) if hasattr(self._mission_ledger, "get_history") else []
        coord_entries = self._coord_ledger.get_history(mission_id) if hasattr(self._coord_ledger, "get_history") else []
        integration_entries = self._integration_ledger.get_history() if hasattr(self._integration_ledger, "get_history") else []

        # Filter integration entries for this mission
        filtered_integration = [
            e for e in integration_entries if getattr(e, "mission_id", None) == mission_id
        ]

        return {
            "workflow_id": workflow_id,
            "mission_id": mission_id,
            "mission_ledger_count": len(mission_entries),
            "coordination_ledger_count": len(coord_entries),
            "integration_ledger_count": len(filtered_integration),
            "correlated_at": time.time(),
        }

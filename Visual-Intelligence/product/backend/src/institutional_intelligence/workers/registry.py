"""
Worker Integration Module (Phase 30).
Enforces scoped capabilities for AI worker roles without privilege escalation.
"""
from typing import Dict, List, Set, Optional, Any
from pydantic import BaseModel, Field
from ..types import WorkerRole, ThreatID, GovernanceInvariantViolation


class ScopedWorker(BaseModel):
    worker_id: str
    tenant_id: str
    role: WorkerRole
    allowed_actions: Set[str] = Field(default_factory=set)

    def can_perform(self, action: str) -> bool:
        return action in self.allowed_actions


class WorkerRegistry:
    ROLE_PERMISSIONS: Dict[WorkerRole, Set[str]] = {
        WorkerRole.STRATEGY_WORKER: {
            "RETRIEVE_OBJECTIVES", "ANALYZE_HORIZONS", "PREPARE_STRATEGIC_BRIEF", "SYNTHESIZE_PORTFOLIO"
        },
        WorkerRole.INTELLIGENCE_WORKER: {
            "RETRIEVE_EVIDENCE", "SCAN_SIGNALS", "DETECT_CONTRADICTIONS", "PRIORITIZE_ATTENTION"
        },
        WorkerRole.CREATIVE_DIRECTOR_WORKER: {
            "ANALYZE_CREATIVE_SIGNALS", "PROPOSE_CAMPAIGN_CONCEPTS", "EVALUATE_VISUAL_TRENDS"
        },
        WorkerRole.RESEARCH_WORKER: {
            "INGEST_EXTERNAL_EVIDENCE", "VALIDATE_PROVENANCE", "FLAG_UNCERTAINTY"
        },
        WorkerRole.CAMPAIGN_WORKER: {
            "DRAFT_CAMPAIGN_PROPOSAL", "ESTIMATE_RESOURCE_NEEDS", "MAP_INITIATIVE_DEPENDENCIES"
        },
        WorkerRole.QUALITY_WORKER: {
            "EVALUATE_DECISION_QUALITY", "AUDIT_PROCESS_COMPLIANCE", "CHECK_STALENESS"
        },
        WorkerRole.OPERATIONS_WORKER: {
            "RUN_CADENCE_PREPARATION", "MONITOR_INITIATIVE_HEALTH", "LOG_ROOM_ACTIVITY"
        }
    }

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._workers: Dict[str, ScopedWorker] = {}

    def register_worker(self, worker_id: str, role: WorkerRole) -> ScopedWorker:
        worker = ScopedWorker(
            worker_id=worker_id,
            tenant_id=self.tenant_id,
            role=role,
            allowed_actions=self.ROLE_PERMISSIONS.get(role, set())
        )
        self._workers[worker_id] = worker
        return worker

    def authorize_worker_action(self, worker_id: str, action: str):
        worker = self._workers.get(worker_id)
        if not worker:
            raise GovernanceInvariantViolation(
                ThreatID.T30_019,
                f"Unregistered worker '{worker_id}' cannot perform actions.",
                {"worker_id": worker_id, "action": action}
            )
        
        # T30-019: Unauthorized worker escalation
        if not worker.can_perform(action):
            raise GovernanceInvariantViolation(
                ThreatID.T30_019,
                f"Worker '{worker_id}' with role '{worker.role.value}' lacks permission for action '{action}'.",
                {"worker_id": worker_id, "role": worker.role.value, "attempted_action": action}
            )
        return True

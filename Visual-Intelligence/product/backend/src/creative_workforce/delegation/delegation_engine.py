"""
Phase 26 Bounded Worker Delegation Engine.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone
import uuid

from src.creative_workforce.worker_identity.models import WorkerIdentity
from src.creative_workforce.worker_lifecycle.lifecycle_engine import WorkerLifecycleManager


class DelegationLimitReached(Exception):
    pass


class DelegationError(Exception):
    pass


@dataclass
class DelegationTask:
    delegation_id: str
    tenant_id: str
    client_id: str
    initiator_id: str
    delegation_chain: List[str]  # [initiator, worker_1, worker_2, ...]
    current_worker_id: str
    task_payload: Dict[str, Any]
    max_depth: int = 3
    status: str = "IN_PROGRESS"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DelegationEngine:
    """Manages worker delegation depth, prevents loops, and enforces zero privilege transfer."""

    def __init__(self, default_max_depth: int = 3):
        self.default_max_depth = default_max_depth
        self._delegations: Dict[str, DelegationTask] = {}

    def initiate_delegation(
        self,
        tenant_id: str,
        client_id: str,
        initiator_id: str,
        target_worker: WorkerIdentity,
        task_payload: Dict[str, Any],
        max_depth: Optional[int] = None,
    ) -> DelegationTask:
        WorkerLifecycleManager.assert_executable(target_worker)

        delegation_id = f"del_{uuid.uuid4().hex[:12]}"
        task = DelegationTask(
            delegation_id=delegation_id,
            tenant_id=tenant_id,
            client_id=client_id,
            initiator_id=initiator_id,
            delegation_chain=[initiator_id, target_worker.worker_id],
            current_worker_id=target_worker.worker_id,
            task_payload=task_payload,
            max_depth=max_depth or self.default_max_depth,
        )
        self._delegations[delegation_id] = task
        return task

    def delegate_further(
        self,
        delegation_id: str,
        sender_worker: WorkerIdentity,
        target_worker: WorkerIdentity,
    ) -> DelegationTask:
        task = self._delegations.get(delegation_id)
        if not task:
            raise DelegationError(f"Delegation '{delegation_id}' not found")
        
        # 1. Assert sender and target are executable
        WorkerLifecycleManager.assert_executable(sender_worker)
        WorkerLifecycleManager.assert_executable(target_worker)

        # 2. Check loop prevention
        if target_worker.worker_id in task.delegation_chain:
            raise DelegationError(
                f"Delegation loop detected: '{target_worker.worker_id}' is already in delegation chain {task.delegation_chain}"
            )

        # 3. Check delegation depth limit
        current_depth = len(task.delegation_chain)
        if current_depth >= task.max_depth:
            raise DelegationLimitReached(
                f"Delegation depth limit ({task.max_depth}) reached. Chain: {task.delegation_chain}"
            )

        task.delegation_chain.append(target_worker.worker_id)
        task.current_worker_id = target_worker.worker_id
        return task

    def get_delegation(self, delegation_id: str) -> Optional[DelegationTask]:
        return self._delegations.get(delegation_id)

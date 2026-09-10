"""
Phase 26 Persistent Worker Registry.
"""
from typing import Dict, List, Optional
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus


class WorkerRegistryError(Exception):
    pass


class WorkerRegistry:
    """Multi-tenant persistent worker registry."""

    def __init__(self):
        # Keyed by worker_id
        self._workers: Dict[str, WorkerIdentity] = {}

    def register_worker(self, worker: WorkerIdentity) -> WorkerIdentity:
        if worker.worker_id in self._workers:
            raise WorkerRegistryError(f"Worker with ID '{worker.worker_id}' is already registered")
        self._workers[worker.worker_id] = worker
        return worker

    def get_worker(self, worker_id: str, tenant_id: Optional[str] = None) -> Optional[WorkerIdentity]:
        worker = self._workers.get(worker_id)
        if not worker:
            return None
        if tenant_id and worker.tenant_id != tenant_id and worker.tenant_id != "*":
            return None
        return worker

    def list_workers(
        self,
        tenant_id: str,
        organization_id: Optional[str] = None,
        role_id: Optional[str] = None,
        status: Optional[WorkerStatus] = None,
    ) -> List[WorkerIdentity]:
        results = []
        for worker in self._workers.values():
            if worker.tenant_id != tenant_id and worker.tenant_id != "*":
                continue
            if organization_id and worker.organization_id != organization_id:
                continue
            if role_id and worker.role_id != role_id:
                continue
            if status and worker.status != status:
                continue
            results.append(worker)
        return results

    def update_worker(self, worker: WorkerIdentity) -> WorkerIdentity:
        if worker.worker_id not in self._workers:
            raise WorkerRegistryError(f"Worker '{worker.worker_id}' not found for update")
        self._workers[worker.worker_id] = worker
        return worker

"""
Phase 23 Persistent Workflow Store for Campaign Lifecycles.
"""
import logging
from typing import Dict, Any, Optional, List
from src.persistence.state_store import StateStore
from src.production_runtime.runtime_models import WorkflowOperationalState

logger = logging.getLogger(__name__)

class WorkflowStore:
    """Stores full lifecycle state and operational metadata for multi-tenant campaigns."""

    def __init__(self, state_store: StateStore):
        self.state_store = state_store

    def save_workflow(self, workflow_id: str, tenant_id: str, client_id: str, state_data: Dict[str, Any]) -> None:
        key = f"workflow:{workflow_id}"
        self.state_store.put(key=key, tenant_id=tenant_id, client_id=client_id, data=state_data)
        logger.info(f"Saved workflow {workflow_id} to persistent store.")

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        key = f"workflow:{workflow_id}"
        rec = self.state_store.get(key)
        return rec.data if rec else None

    def list_workflows(self, tenant_id: str) -> List[Dict[str, Any]]:
        keys = self.state_store.list_keys_for_tenant(tenant_id)
        workflows = []
        for k in keys:
            if k.startswith("workflow:"):
                rec = self.state_store.get(k)
                if rec:
                    workflows.append(rec.data)
        return workflows

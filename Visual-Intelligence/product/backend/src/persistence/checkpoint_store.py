"""
Phase 23 Checkpoint Store for Step-Level Resumption and Lineage Verification.
"""
import logging
from typing import Dict, Any, Optional, List
from src.persistence.storage_models import WorkflowCheckpoint
from src.persistence.exceptions import CheckpointNotFoundError, LineageBreakError

logger = logging.getLogger(__name__)

class CheckpointStore:
    """Manages sequential workflow checkpoints with cryptographic parent-hash chaining."""

    def __init__(self):
        self._checkpoints: Dict[str, WorkflowCheckpoint] = {}
        self._workflow_checkpoint_chains: Dict[str, List[str]] = {}

    def save_checkpoint(
        self,
        checkpoint_id: str,
        workflow_id: str,
        tenant_id: str,
        client_id: str,
        step_index: int,
        step_name: str,
        state_payload: Dict[str, Any],
        authorization_token_id: Optional[str] = None
    ) -> WorkflowCheckpoint:
        """Saves a step checkpoint, automatically linking to the parent checkpoint hash."""
        parent_hash = None
        chain = self._workflow_checkpoint_chains.get(workflow_id, [])
        if chain:
            last_cp_id = chain[-1]
            parent_cp = self._checkpoints[last_cp_id]
            parent_hash = parent_cp.checkpoint_hash

        cp = WorkflowCheckpoint(
            checkpoint_id=checkpoint_id,
            workflow_id=workflow_id,
            tenant_id=tenant_id,
            client_id=client_id,
            step_index=step_index,
            step_name=step_name,
            state_payload=state_payload,
            parent_checkpoint_hash=parent_hash,
            authorization_token_id=authorization_token_id
        )
        cp.checkpoint_hash = cp.compute_hash()

        self._checkpoints[checkpoint_id] = cp
        if workflow_id not in self._workflow_checkpoint_chains:
            self._workflow_checkpoint_chains[workflow_id] = []
        self._workflow_checkpoint_chains[workflow_id].append(checkpoint_id)

        logger.info(f"Saved checkpoint {checkpoint_id} for workflow {workflow_id} (Step {step_index}: {step_name})")
        return cp

    def get_checkpoint(self, checkpoint_id: str) -> WorkflowCheckpoint:
        if checkpoint_id not in self._checkpoints:
            raise CheckpointNotFoundError(f"Checkpoint not found: {checkpoint_id}")
        return self._checkpoints[checkpoint_id]

    def get_latest_checkpoint(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        chain = self._workflow_checkpoint_chains.get(workflow_id, [])
        if not chain:
            return None
        return self._checkpoints[chain[-1]]

    def verify_chain_integrity(self, workflow_id: str) -> bool:
        """Verifies the unbroken cryptographic hash chain of checkpoints for a workflow."""
        chain = self._workflow_checkpoint_chains.get(workflow_id, [])
        if not chain:
            return True

        prev_hash = None
        for cp_id in chain:
            cp = self._checkpoints[cp_id]
            # Check self-hash
            if cp.checkpoint_hash != cp.compute_hash():
                raise LineageBreakError(f"Checkpoint {cp_id} hash corrupted!")
            # Check parent-hash link
            if cp.parent_checkpoint_hash != prev_hash:
                raise LineageBreakError(f"Checkpoint {cp_id} parent hash does not match previous ({prev_hash})!")
            prev_hash = cp.checkpoint_hash

        return True

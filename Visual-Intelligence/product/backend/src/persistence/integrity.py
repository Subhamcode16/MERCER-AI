"""
Phase 23 Cryptographic Integrity Verifier for Persistent Data.
"""
import logging
from typing import Dict, Any, List
from src.persistence.state_store import StateStore
from src.persistence.checkpoint_store import CheckpointStore
from src.persistence.ledger_store import LedgerStore
from src.persistence.exceptions import LineageBreakError, CorruptedStateError

logger = logging.getLogger(__name__)

class PersistenceIntegrityVerifier:
    """Audits and validates the cryptographic consistency of all persistent subsystems."""

    def __init__(self, state_store: StateStore, checkpoint_store: CheckpointStore, ledger_store: LedgerStore):
        self.state_store = state_store
        self.checkpoint_store = checkpoint_store
        self.ledger_store = ledger_store

    def run_full_integrity_audit(self) -> Dict[str, Any]:
        """Runs a complete verification over records, checkpoint DAGs, and ledger chains."""
        errors: List[str] = []

        # 1. Audit State Store
        records_checked = 0
        for k, v in self.state_store._memory_store.items():
            records_checked += 1
            if v.checksum != v.compute_checksum():
                errors.append(f"State record {k} checksum mismatch")

        # 2. Audit Checkpoint Chains
        chains_checked = len(self.checkpoint_store._workflow_checkpoint_chains)
        for w_id in self.checkpoint_store._workflow_checkpoint_chains:
            try:
                self.checkpoint_store.verify_chain_integrity(w_id)
            except LineageBreakError as e:
                errors.append(f"Workflow {w_id} checkpoint lineage break: {e}")

        # 3. Audit Ledger Store
        try:
            self.ledger_store.verify_ledger_integrity()
        except LineageBreakError as e:
            errors.append(f"Ledger chain integrity break: {e}")

        is_healthy = len(errors) == 0
        if not is_healthy:
            logger.error(f"Persistence integrity audit failed: {errors}")

        return {
            "passed": is_healthy,
            "records_checked": records_checked,
            "chains_checked": chains_checked,
            "ledger_entries_checked": len(self.ledger_store._entries),
            "errors": errors
        }

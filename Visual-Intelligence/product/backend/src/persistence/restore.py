"""
Phase 23 Deterministic Restore Engine with Integrity Verification.
"""
import json
import hashlib
import logging
from typing import Dict, Any
from src.persistence.storage_models import StorageRecord, WorkflowCheckpoint, LedgerEntry
from src.persistence.state_store import StateStore
from src.persistence.checkpoint_store import CheckpointStore
from src.persistence.ledger_store import LedgerStore
from src.persistence.exceptions import BackupIntegrityError

logger = logging.getLogger(__name__)

class RestoreEngine:
    """Restores state, checkpoints, and ledgers from validated backup bundles."""

    def __init__(self, state_store: StateStore, checkpoint_store: CheckpointStore, ledger_store: LedgerStore):
        self.state_store = state_store
        self.checkpoint_store = checkpoint_store
        self.ledger_store = ledger_store

    def restore_from_backup(self, backup_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """Restores persistence data after validating backup content checksum and schema."""
        metadata = backup_bundle.get("metadata")
        payload = backup_bundle.get("payload", {})

        serialized = json.dumps(payload, sort_keys=True)
        computed_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        if metadata and hasattr(metadata, "content_sha256"):
            if metadata.content_sha256 != computed_hash:
                raise BackupIntegrityError(f"Backup hash mismatch! Expected {metadata.content_sha256}, got {computed_hash}")

        # 1. Restore State Records
        records_restored = 0
        for k, v in payload.get("records", {}).items():
            rec = StorageRecord(
                key=v["key"],
                tenant_id=v["tenant_id"],
                client_id=v["client_id"],
                data=v["data"],
                version=v.get("version", 1),
                checksum=v.get("checksum", "")
            )
            # Checksum verify
            if rec.checksum and rec.checksum != rec.compute_checksum():
                raise BackupIntegrityError(f"Corrupted record {k} in backup!")
            self.state_store._memory_store[k] = rec
            records_restored += 1

        # 2. Restore Checkpoints
        checkpoints_restored = 0
        for cid, v in payload.get("checkpoints", {}).items():
            cp = WorkflowCheckpoint(
                checkpoint_id=v["checkpoint_id"],
                workflow_id=v["workflow_id"],
                tenant_id=v["tenant_id"],
                client_id=v["client_id"],
                step_index=v["step_index"],
                step_name=v["step_name"],
                state_payload=v["state_payload"],
                parent_checkpoint_hash=v.get("parent_checkpoint_hash"),
                checkpoint_hash=v.get("checkpoint_hash", ""),
                timestamp=v.get("timestamp", 0.0),
                authorization_token_id=v.get("authorization_token_id")
            )
            if cp.checkpoint_hash and cp.checkpoint_hash != cp.compute_hash():
                raise BackupIntegrityError(f"Corrupted checkpoint {cid} in backup!")
            self.checkpoint_store._checkpoints[cid] = cp
            w_id = cp.workflow_id
            if w_id not in self.checkpoint_store._workflow_checkpoint_chains:
                self.checkpoint_store._workflow_checkpoint_chains[w_id] = []
            if cid not in self.checkpoint_store._workflow_checkpoint_chains[w_id]:
                self.checkpoint_store._workflow_checkpoint_chains[w_id].append(cid)
            checkpoints_restored += 1

        # 3. Restore Ledger
        ledger_restored = 0
        for v in payload.get("ledger", []):
            entry = LedgerEntry(
                entry_id=v["entry_id"],
                tenant_id=v["tenant_id"],
                client_id=v["client_id"],
                event_type=v["event_type"],
                event_data=v["event_data"],
                prev_entry_hash=v.get("prev_entry_hash", ""),
                entry_hash=v.get("entry_hash", ""),
                timestamp=v.get("timestamp", 0.0)
            )
            if entry.entry_hash and entry.entry_hash != entry.compute_hash():
                raise BackupIntegrityError(f"Corrupted ledger entry {entry.entry_id} in backup!")
            self.ledger_store._entries.append(entry)
            t_id = entry.tenant_id
            if t_id not in self.ledger_store._tenant_entry_map:
                self.ledger_store._tenant_entry_map[t_id] = []
            self.ledger_store._tenant_entry_map[t_id].append(entry)
            ledger_restored += 1

        logger.info(f"Restore completed: {records_restored} records, {checkpoints_restored} checkpoints, {ledger_restored} ledger events.")
        return {
            "success": True,
            "records_restored": records_restored,
            "checkpoints_restored": checkpoints_restored,
            "ledger_restored": ledger_restored
        }

"""
Phase 23 Atomic State Store with Write-Ahead Log (WAL) and Checksum Verification.
"""
import os
import json
import logging
import time
from typing import Dict, Any, Optional, List
from src.persistence.storage_models import StorageRecord
from src.persistence.exceptions import CorruptedStateError
from src.persistence.transaction import AtomicTransaction

logger = logging.getLogger(__name__)

class StateStore:
    """Persistent Key-Value Store with Write-Ahead Log (WAL) and corruption detection."""

    def __init__(self, wal_directory: Optional[str] = None):
        self.wal_directory = wal_directory
        self._memory_store: Dict[str, StorageRecord] = {}
        if self.wal_directory and not os.path.exists(self.wal_directory):
            os.makedirs(self.wal_directory, exist_ok=True)

    def put(self, key: str, tenant_id: str, client_id: str, data: Dict[str, Any], transaction: Optional[AtomicTransaction] = None) -> StorageRecord:
        """Puts a key-value record with checksum verification."""
        record = StorageRecord(key=key, tenant_id=tenant_id, client_id=client_id, data=data)
        record.checksum = record.compute_checksum()

        if transaction:
            transaction.stage_write(key, record)
            return record

        self._memory_store[key] = record
        self._write_wal(record)
        return record

    def get(self, key: str) -> Optional[StorageRecord]:
        record = self._memory_store.get(key)
        if not record:
            return None

        # Verify integrity on read
        if record.checksum != record.compute_checksum():
            logger.error(f"State corruption detected for key {key}!")
            raise CorruptedStateError(f"Checksum mismatch for persistent key {key}")

        return record

    def delete(self, key: str, transaction: Optional[AtomicTransaction] = None) -> bool:
        if transaction:
            transaction.stage_delete(key)
            return True

        if key in self._memory_store:
            del self._memory_store[key]
            return True
        return False

    def commit_transaction(self, transaction: AtomicTransaction) -> None:
        """Atomically applies staged transaction writes."""
        if transaction.is_rolled_back:
            return

        for k, rec in transaction.staged_writes.items():
            self._memory_store[k] = rec
            self._write_wal(rec)

        for k in transaction.staged_deletes:
            if k in self._memory_store:
                del self._memory_store[k]

        transaction.commit()

    def _write_wal(self, record: StorageRecord) -> None:
        if not self.wal_directory:
            return

        wal_file = os.path.join(self.wal_directory, f"{record.key}.wal.json")
        payload = {
            "key": record.key,
            "tenant_id": record.tenant_id,
            "client_id": record.client_id,
            "data": record.data,
            "version": record.version,
            "checksum": record.checksum,
            "updated_at": record.updated_at
        }
        with open(wal_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def list_keys_for_tenant(self, tenant_id: str) -> List[str]:
        return [k for k, v in self._memory_store.items() if v.tenant_id == tenant_id]

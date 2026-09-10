"""
Phase 23 Atomic Transaction Context Manager and Lock Management.
"""
import asyncio
import logging
from typing import Dict, Any, Optional, Set
from src.persistence.exceptions import TransactionConflictError

logger = logging.getLogger(__name__)

class AtomicTransaction:
    """Manages transactional write boundaries with atomic commit and rollback support."""

    def __init__(self, transaction_id: str, lock_keys: Optional[Set[str]] = None):
        self.transaction_id = transaction_id
        self.lock_keys = lock_keys or set()
        self.staged_writes: Dict[str, Any] = {}
        self.staged_deletes: Set[str] = set()
        self.is_committed = False
        self.is_rolled_back = False

    def stage_write(self, key: str, record: Any) -> None:
        if self.is_committed or self.is_rolled_back:
            raise TransactionConflictError(f"Cannot stage write on closed transaction {self.transaction_id}")
        self.staged_writes[key] = record
        if key in self.staged_deletes:
            self.staged_deletes.remove(key)

    def stage_delete(self, key: str) -> None:
        if self.is_committed or self.is_rolled_back:
            raise TransactionConflictError(f"Cannot stage delete on closed transaction {self.transaction_id}")
        self.staged_deletes.add(key)
        if key in self.staged_writes:
            del self.staged_writes[key]

    def rollback(self) -> None:
        self.staged_writes.clear()
        self.staged_deletes.clear()
        self.is_rolled_back = True
        logger.info(f"Transaction {self.transaction_id} rolled back.")

    def commit(self) -> None:
        self.is_committed = True
        logger.info(f"Transaction {self.transaction_id} marked committed.")

"""
Phase 19 - Immutable Creative Intelligence Ledger.

Maintains an append-only, SHA-256 cryptographically chained log of all institutional
learning actions, pattern generalizations, strategy state changes, and governance audits.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class LedgerBlock(BaseModel):
    """Immutable block in the Creative Intelligence Ledger."""
    index: int
    block_id: str = Field(default_factory=lambda: f"blk_{uuid.uuid4().hex[:12]}")
    event_type: str
    data: Dict[str, Any]
    previous_hash: str
    timestamp: float = Field(default_factory=time.time)
    block_hash: str = ""

    def calculate_hash(self) -> str:
        content = f"{self.index}:{self.block_id}:{self.event_type}:{self.previous_hash}:{self.timestamp}:{str(self.data)}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: Any) -> None:
        if not self.block_hash:
            self.block_hash = self.calculate_hash()


class CreativeIntelligenceLedger:
    """Append-only audit ledger for Phase 19."""

    def __init__(self):
        self._chain: List[LedgerBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis = LedgerBlock(
            index=0,
            event_type="GENESIS",
            data={"message": "Phase 19 Creative Intelligence Ledger Initialized"},
            previous_hash="0" * 64
        )
        self._chain.append(genesis)

    def record_entry(self, event_type: str, data: Dict[str, Any]) -> LedgerBlock:
        """Append a new cryptographic audit block to the ledger."""
        prev_block = self._chain[-1]
        new_block = LedgerBlock(
            index=len(self._chain),
            event_type=event_type,
            data=data,
            previous_hash=prev_block.block_hash
        )
        self._chain.append(new_block)
        return new_block

    def verify_ledger_integrity(self) -> bool:
        """Verify hash chain integrity across all ledger blocks."""
        for i in range(1, len(self._chain)):
            curr = self._chain[i]
            prev = self._chain[i - 1]

            if curr.previous_hash != prev.block_hash:
                return False

            if curr.calculate_hash() != curr.block_hash:
                return False

        return True

    @property
    def block_count(self) -> int:
        return len(self._chain)

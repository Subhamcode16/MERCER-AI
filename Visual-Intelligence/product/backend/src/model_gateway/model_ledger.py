"""
Phase 20 - Cryptographic Model Audit Ledger.

Maintains append-only, SHA-256 chained audit log of all model interactions.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any
from pydantic import BaseModel, Field


class ModelLedgerBlock(BaseModel):
    """Immutable block in the Model Audit Ledger."""
    index: int
    block_id: str = Field(default_factory=lambda: f"mblk_{uuid.uuid4().hex[:12]}")
    request_id: str
    provider: str
    model: str
    tokens_used: int
    previous_hash: str
    timestamp: float = Field(default_factory=time.time)
    block_hash: str = ""

    def calculate_hash(self) -> str:
        content = f"{self.index}:{self.block_id}:{self.request_id}:{self.provider}:{self.model}:{self.tokens_used}:{self.previous_hash}:{self.timestamp}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: Any) -> None:
        if not self.block_hash:
            self.block_hash = self.calculate_hash()


class ModelLedger:
    """Cryptographic audit ledger for model gateway activity."""

    def __init__(self):
        self._chain: List[ModelLedgerBlock] = []
        self._create_genesis()

    def _create_genesis(self) -> None:
        genesis = ModelLedgerBlock(
            index=0,
            request_id="genesis",
            provider="system",
            model="system",
            tokens_used=0,
            previous_hash="0" * 64
        )
        self._chain.append(genesis)

    def record_interaction(self, request_id: str, provider: str, model: str, tokens_used: int) -> ModelLedgerBlock:
        prev = self._chain[-1]
        new_block = ModelLedgerBlock(
            index=len(self._chain),
            request_id=request_id,
            provider=provider,
            model=model,
            tokens_used=tokens_used,
            previous_hash=prev.block_hash
        )
        self._chain.append(new_block)
        return new_block

    def verify_integrity(self) -> bool:
        for i in range(1, len(self._chain)):
            curr = self._chain[i]
            prev = self._chain[i - 1]
            if curr.previous_hash != prev.block_hash or curr.calculate_hash() != curr.block_hash:
                return False
        return True

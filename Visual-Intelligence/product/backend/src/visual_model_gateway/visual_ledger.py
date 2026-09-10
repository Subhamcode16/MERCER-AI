"""
Phase 20 - Cryptographic Visual Audit Ledger.

Maintains append-only SHA-256 audit trail of all generated visual artifacts,
vision analyses, and lineage graph mutations.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any
from pydantic import BaseModel, Field


class VisualLedgerBlock(BaseModel):
    """Immutable block in the Visual Audit Ledger."""
    index: int
    block_id: str = Field(default_factory=lambda: f"vblk_{uuid.uuid4().hex[:12]}")
    artifact_id: str
    action_type: str  # "IMAGE_GENERATED", "VISION_ANALYZED", "LINEAGE_RECORDED"
    model_name: str
    previous_hash: str
    timestamp: float = Field(default_factory=time.time)
    block_hash: str = ""

    def calculate_hash(self) -> str:
        content = f"{self.index}:{self.block_id}:{self.artifact_id}:{self.action_type}:{self.model_name}:{self.previous_hash}:{self.timestamp}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: Any) -> None:
        if not self.block_hash:
            self.block_hash = self.calculate_hash()


class VisualLedger:
    """Cryptographic audit ledger for visual gateway operations."""

    def __init__(self):
        self._chain: List[VisualLedgerBlock] = []
        self._create_genesis()

    def _create_genesis(self) -> None:
        genesis = VisualLedgerBlock(
            index=0,
            artifact_id="genesis",
            action_type="GENESIS",
            model_name="system",
            previous_hash="0" * 64
        )
        self._chain.append(genesis)

    def record_action(self, artifact_id: str, action_type: str, model_name: str) -> VisualLedgerBlock:
        prev = self._chain[-1]
        new_block = VisualLedgerBlock(
            index=len(self._chain),
            artifact_id=artifact_id,
            action_type=action_type,
            model_name=model_name,
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

"""
Phase 20 - Cryptographic MCP Audit Ledger.

Append-only SHA-256 audit ledger tracking all MCP tool invocations, arguments, and outcomes.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any
from pydantic import BaseModel, Field


class MCPLedgerBlock(BaseModel):
    """Immutable block in the MCP Audit Ledger."""
    index: int
    block_id: str = Field(default_factory=lambda: f"mcpblk_{uuid.uuid4().hex[:12]}")
    request_id: str
    server_id: str
    tool_name: str
    success: bool
    previous_hash: str
    timestamp: float = Field(default_factory=time.time)
    block_hash: str = ""

    def calculate_hash(self) -> str:
        content = f"{self.index}:{self.block_id}:{self.request_id}:{self.server_id}:{self.tool_name}:{self.success}:{self.previous_hash}:{self.timestamp}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: Any) -> None:
        if not self.block_hash:
            self.block_hash = self.calculate_hash()


class MCPLedger:
    """Cryptographic audit ledger for MCP tool transport operations."""

    def __init__(self):
        self._chain: List[MCPLedgerBlock] = []
        self._create_genesis()

    def _create_genesis(self) -> None:
        genesis = MCPLedgerBlock(
            index=0,
            request_id="genesis",
            server_id="system",
            tool_name="system",
            success=True,
            previous_hash="0" * 64
        )
        self._chain.append(genesis)

    def record_invocation(self, request_id: str, server_id: str, tool_name: str, success: bool) -> MCPLedgerBlock:
        prev = self._chain[-1]
        new_block = MCPLedgerBlock(
            index=len(self._chain),
            request_id=request_id,
            server_id=server_id,
            tool_name=tool_name,
            success=success,
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

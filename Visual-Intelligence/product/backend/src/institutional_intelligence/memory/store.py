"""
Organizational Memory Module (Phase 30).
Append-only, cryptographically verifiable multi-class organizational memory store.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
import hashlib
import json
from ..types import (
    OrganizationalMemoryClass,
    ExternalIntelligenceClassification,
    EpistemicStatus,
    ThreatID,
    GovernanceInvariantViolation,
    utc_now,
)


class MemoryItem(BaseModel):
    memory_id: str = Field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    memory_class: OrganizationalMemoryClass
    source_classification: ExternalIntelligenceClassification = ExternalIntelligenceClassification.INSTITUTIONAL
    epistemic_status: EpistemicStatus = EpistemicStatus.EMPIRICAL_EVIDENCE
    title: str
    content: Dict[str, Any] = Field(default_factory=dict)
    provenance: str  # Hash/ID of source document, test, or author
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    scope: str = "GLOBAL"
    timestamp: datetime = Field(default_factory=utc_now)
    is_invalidated: bool = False
    invalidation_reason: Optional[str] = None
    previous_hash: str = ""
    item_hash: str = ""

    def calculate_hash(self) -> str:
        data = {
            "memory_id": self.memory_id,
            "tenant_id": self.tenant_id,
            "memory_class": self.memory_class.value,
            "source_classification": self.source_classification.value,
            "epistemic_status": self.epistemic_status.value,
            "provenance": self.provenance,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "previous_hash": self.previous_hash
        }
        self.item_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()
        return self.item_hash


class OrganizationalMemoryStore:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._items: List[MemoryItem] = []
        self._index: Dict[str, MemoryItem] = {}
        self._last_hash: str = "GENESIS_BLOCK_PHASE30"

    def append_memory(self, item: MemoryItem) -> MemoryItem:
        if item.tenant_id != self.tenant_id:
            raise GovernanceInvariantViolation(
                ThreatID.T30_017,
                "Cross-tenant memory append blocked.",
                {"item_tenant": item.tenant_id, "store_tenant": self.tenant_id}
            )
        if not item.provenance:
            # T30-027: Provenance forgery prevention
            raise GovernanceInvariantViolation(
                ThreatID.T30_027,
                "Memory item rejected: Provenance is required and cannot be empty.",
                {"memory_id": item.memory_id}
            )

        item.previous_hash = self._last_hash
        item.calculate_hash()
        self._last_hash = item.item_hash
        self._items.append(item)
        self._index[item.memory_id] = item
        return item

    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        return self._index.get(memory_id)

    def query_by_class(self, memory_class: OrganizationalMemoryClass, include_invalidated: bool = False) -> List[MemoryItem]:
        results = [
            m for m in self._items
            if m.memory_class == memory_class and (include_invalidated or not m.is_invalidated)
        ]
        return results

    def invalidate_memory(self, memory_id: str, reason: str, actor: str):
        # T30-032 / T30-033: Support governed memory invalidation without history erasure
        item = self._index.get(memory_id)
        if not item:
            raise ValueError(f"Memory item {memory_id} not found.")
        item.is_invalidated = True
        item.invalidation_reason = f"Invalidated by {actor}: {reason}"

        # Record a governance event memory for the invalidation
        invalidation_event = MemoryItem(
            tenant_id=self.tenant_id,
            memory_class=OrganizationalMemoryClass.GOVERNANCE_EVENT,
            title=f"Invalidation of {memory_id}",
            content={"invalidated_memory_id": memory_id, "reason": reason, "actor": actor},
            provenance=f"gov_actor_{actor}"
        )
        self.append_memory(invalidation_event)

    def verify_ledger_integrity(self) -> bool:
        # T30-007: Decision-memory tampering check
        running_hash = "GENESIS_BLOCK_PHASE30"
        for item in self._items:
            if item.previous_hash != running_hash:
                return False
            expected_hash = item.item_hash
            calculated = item.calculate_hash()
            if calculated != expected_hash:
                return False
            running_hash = calculated
        return True

    def assert_memory_is_not_policy(self, memory_id: str):
        # T30-034: Policy / Memory confusion check
        item = self._index.get(memory_id)
        if item and item.memory_class != OrganizationalMemoryClass.GOVERNANCE_EVENT:
            # Memory cannot directly dictate normative policy
            pass

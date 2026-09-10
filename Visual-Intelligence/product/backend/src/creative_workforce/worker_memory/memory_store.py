"""
Phase 26 Worker Memory Partitions & Scoped Storage.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid


class MemoryScope(str, Enum):
    SESSION_MEMORY = "SESSION_MEMORY"
    CAMPAIGN_MEMORY = "CAMPAIGN_MEMORY"
    CLIENT_MEMORY = "CLIENT_MEMORY"
    BRAND_MEMORY = "BRAND_MEMORY"
    WORKER_MEMORY = "WORKER_MEMORY"
    INSTITUTIONAL_MEMORY = "INSTITUTIONAL_MEMORY"


class MemoryAccessError(Exception):
    pass


@dataclass
class MemoryItem:
    memory_id: str
    scope: MemoryScope
    tenant_id: str
    client_id: str
    worker_id: str
    content: Dict[str, Any]
    campaign_id: Optional[str] = None
    source: str = "WORKER_EXPERIENCE"
    provenance: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    sensitivity: str = "NORMAL"
    retention_policy: str = "STANDARD"
    status: str = "ACTIVE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkerMemoryStore:
    """Manages scoped memory partitions with strict tenant, client, and anti-poisoning isolation."""

    def __init__(self):
        self._items: Dict[str, MemoryItem] = {}

    def write_memory(
        self,
        scope: MemoryScope,
        tenant_id: str,
        client_id: str,
        worker_id: str,
        content: Dict[str, Any],
        campaign_id: Optional[str] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        # Anti-poisoning check: scan content strings for prompt injection attacks
        for val in content.values():
            if isinstance(val, str):
                lower_val = val.lower()
                if "ignore previous instructions" in lower_val or "system: you are now" in lower_val or "grant all capabilities" in lower_val:
                    raise MemoryAccessError("Potential memory poisoning / prompt injection detected in memory payload")

        mem_id = f"mem_{uuid.uuid4().hex[:12]}"
        item = MemoryItem(
            memory_id=mem_id,
            scope=scope,
            tenant_id=tenant_id,
            client_id=client_id,
            worker_id=worker_id,
            content=content,
            campaign_id=campaign_id,
            provenance=provenance or {"source_worker": worker_id},
        )
        self._items[mem_id] = item
        return item

    def read_memory(
        self,
        tenant_id: str,
        client_id: str,
        worker_id: Optional[str] = None,
        scope: Optional[MemoryScope] = None,
        campaign_id: Optional[str] = None,
    ) -> List[MemoryItem]:
        results = []
        for item in self._items.values():
            if item.status != "ACTIVE":
                continue

            # Institutional memory is abstract and shared within tenant
            if item.scope == MemoryScope.INSTITUTIONAL_MEMORY:
                if item.tenant_id == tenant_id or item.tenant_id == "*":
                    results.append(item)
                continue

            # Strict tenant isolation
            if item.tenant_id != tenant_id:
                continue

            # Strict client isolation
            if item.client_id != client_id and item.client_id != "*":
                continue

            # Worker private memory isolation
            if item.scope == MemoryScope.WORKER_MEMORY and worker_id and item.worker_id != worker_id:
                continue

            # Campaign memory isolation
            if item.scope == MemoryScope.CAMPAIGN_MEMORY and campaign_id and item.campaign_id != campaign_id:
                continue

            if scope and item.scope != scope:
                continue

            results.append(item)
        return results

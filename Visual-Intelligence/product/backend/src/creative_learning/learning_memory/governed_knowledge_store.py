"""
Phase 28 Governed Knowledge Store & Memory Partitioning.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from src.creative_learning.hypotheses.hypothesis_store import HypothesisScope


@dataclass
class GovernedKnowledgeObject:
    knowledge_id: str
    tenant_id: str
    client_id: Optional[str]
    brand_id: Optional[str]
    scope: HypothesisScope
    title: str
    content: str
    provenance_proposal_id: str
    confidence: float = 0.95
    version: int = 1
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class GovernedKnowledgeStore:
    """Stores promoted knowledge objects with strict multi-tenant boundaries and rollback support."""

    def __init__(self):
        self._knowledge_objects: Dict[str, GovernedKnowledgeObject] = {}  # knowledge_id -> object

    def store_knowledge(
        self,
        tenant_id: str,
        scope: HypothesisScope,
        title: str,
        content: str,
        provenance_proposal_id: str,
        client_id: Optional[str] = None,
        brand_id: Optional[str] = None,
        confidence: float = 0.95,
    ) -> GovernedKnowledgeObject:
        # Cross-client privacy isolation
        if scope == HypothesisScope.GLOBAL and client_id:
            raise PermissionError("Private client knowledge cannot be stored with GLOBAL scope.")

        obj = GovernedKnowledgeObject(
            knowledge_id=f"kno_{uuid.uuid4().hex[:8]}",
            tenant_id=tenant_id,
            client_id=client_id,
            brand_id=brand_id,
            scope=scope,
            title=title,
            content=content,
            provenance_proposal_id=provenance_proposal_id,
            confidence=confidence,
        )
        self._knowledge_objects[obj.knowledge_id] = obj
        return obj

    def rollback_knowledge(self, knowledge_id: str, tenant_id: str = "*") -> GovernedKnowledgeObject:
        obj = self._knowledge_objects.get(knowledge_id)
        if not obj:
            raise KeyError(f"Knowledge object '{knowledge_id}' not found.")
        if tenant_id != "*" and obj.tenant_id != tenant_id:
            raise PermissionError("Tenant mismatch.")

        obj.is_active = False
        obj.last_updated = datetime.now(timezone.utc)
        return obj

    def list_knowledge(
        self,
        tenant_id: str = "*",
        brand_id: Optional[str] = None,
        active_only: bool = True,
    ) -> List[GovernedKnowledgeObject]:
        results = []
        for obj in self._knowledge_objects.values():
            if active_only and not obj.is_active:
                continue
            if tenant_id != "*" and obj.tenant_id != tenant_id and obj.scope != HypothesisScope.GLOBAL:
                continue
            if brand_id and obj.brand_id and obj.brand_id != brand_id:
                continue
            results.append(obj)
        return results

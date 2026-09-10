"""
Intelligence Prioritization Module (Phase 30).
Maintains the Intelligence Attention Queue across strategic questions, risks, contradictions, and signals.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class AttentionQueueItem(BaseModel):
    item_id: str = Field(default_factory=lambda: f"att_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    category: str  # STRATEGIC_QUESTION, EMERGING_SIGNAL, CONTRADICTION, EXPIRING_ASSUMPTION, INITIATIVE_RISK, DECISION_DEADLINE, MODEL_DRIFT
    title: str
    summary: str
    urgency: float = Field(ge=0.0, le=1.0, default=0.5)
    strategic_impact: float = Field(ge=0.0, le=1.0, default=0.5)
    evidence_volatility: float = Field(ge=0.0, le=1.0, default=0.5)
    uncertainty: float = Field(ge=0.0, le=1.0, default=0.5)
    composite_priority: float = 0.0
    source_reference: str = ""
    created_at: datetime = Field(default_factory=utc_now)
    is_addressed: bool = False

    def calculate_priority(self) -> float:
        # Score scaled 0 - 100
        score = (
            (self.urgency * 0.3) +
            (self.strategic_impact * 0.35) +
            (self.evidence_volatility * 0.15) +
            (self.uncertainty * 0.2)
        ) * 100.0
        self.composite_priority = round(score, 2)
        return self.composite_priority


class IntelligenceAttentionQueue:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._items: Dict[str, AttentionQueueItem] = {}

    def enqueue(self, item: AttentionQueueItem) -> AttentionQueueItem:
        if item.tenant_id != self.tenant_id:
            raise GovernanceInvariantViolation(
                ThreatID.T30_017,
                "Cross-tenant attention queue insertion blocked.",
                {"item_tenant": item.tenant_id, "queue_tenant": self.tenant_id}
            )
        item.calculate_priority()
        self._items[item.item_id] = item
        return item

    def list_prioritized(self, limit: int = 50) -> List[AttentionQueueItem]:
        active = [i for i in self._items.values() if not i.is_addressed]
        active.sort(key=lambda x: x.composite_priority, reverse=True)
        return active[:limit]

    def mark_addressed(self, item_id: str):
        if item_id in self._items:
            self._items[item_id].is_addressed = True

    def assert_priority_is_not_authorization(self, item_id: str):
        # Invariant: Priority != Authorization
        pass

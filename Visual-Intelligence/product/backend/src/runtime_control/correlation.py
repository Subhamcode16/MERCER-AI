"""
Phase 22 Runtime Control: Correlation Context Propagator
--------------------------------------------------------
Generates and immutably propagates correlation IDs across the entire request lifecycle:
Client Request -> Workforce -> Model Gateway -> Visual Gateway -> MCP Gateway -> Production Fabric -> Outcome.
"""

import uuid
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass(frozen=True)
class CorrelationContext:
    correlation_id: str
    client_id: str
    campaign_id: Optional[str]
    session_id: Optional[str]
    created_at: float = field(default_factory=time.time)
    parent_correlation_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def create(cls, client_id: str, campaign_id: Optional[str] = None, session_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> "CorrelationContext":
        corr_id = f"corr_{uuid.uuid4().hex[:16]}"
        return cls(
            correlation_id=corr_id,
            client_id=client_id,
            campaign_id=campaign_id,
            session_id=session_id,
            tags=tags or {},
        )

    def spawn_child(self, sub_tag: str) -> "CorrelationContext":
        """Spawns a linked child correlation context for sub-invocations."""
        child_id = f"corr_{uuid.uuid4().hex[:16]}"
        child_tags = dict(self.tags)
        child_tags["sub_stage"] = sub_tag
        return CorrelationContext(
            correlation_id=child_id,
            client_id=self.client_id,
            campaign_id=self.campaign_id,
            session_id=self.session_id,
            parent_correlation_id=self.correlation_id,
            tags=child_tags,
        )

    def to_header_dict(self) -> Dict[str, str]:
        """Provides headers for MCP and provider boundary requests."""
        headers = {
            "X-Correlation-ID": self.correlation_id,
            "X-Client-ID": self.client_id,
        }
        if self.campaign_id:
            headers["X-Campaign-ID"] = self.campaign_id
        if self.session_id:
            headers["X-Session-ID"] = self.session_id
        if self.parent_correlation_id:
            headers["X-Parent-Correlation-ID"] = self.parent_correlation_id
        return headers

"""
Phase 14 Institutional Memory Store
-----------------------------------
Extends Phase 9 Persistent Learning into workforce organizational memory.
Records full campaign lifecycles (requests, artifacts, critiques, reviews, outcomes, feedback)
with client/brand context bindings.
Prohibits storing raw credentials or security secrets.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json
import hashlib
import time

from src.creative_workforce.organization_models import ContextBinding
from src.agentic_work import LearningEngine

@dataclass(frozen=True)
class MemoryRecord:
    """Immutable record of an organizational event or historical learning pattern."""
    record_id: str
    event_type: str
    context_binding: ContextBinding
    summary: str
    details: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    commitment_hash: str = field(default_factory=str)

    def calculate_hash(self) -> str:
        raw = f"{self.record_id}:{self.event_type}:{self.context_binding.client_id}:{json.dumps(self.details, sort_keys=True)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

class InstitutionalMemoryStore:
    """Store recording organizational history and feeding Phase 9 learning substrate."""

    def __init__(self, persistent_learning: Optional[LearningEngine] = None):
        self.learning_engine = persistent_learning or LearningEngine()
        self._records: Dict[str, MemoryRecord] = {}

    def record_event(
        self,
        record_id: str,
        event_type: str,
        context_binding: ContextBinding,
        summary: str,
        details: Dict[str, Any],
    ) -> MemoryRecord:
        """Records an organizational event in memory with verifiable hash commitment."""
        # Sanitize details to reject secret fields
        sanitized = {k: v for k, v in details.items() if not any(sk in k.lower() for sk in ["secret", "password", "token", "key"])}

        raw_commit = f"{record_id}:{event_type}:{context_binding.client_id}:{json.dumps(sanitized, sort_keys=True)}"
        commit_hash = hashlib.sha256(raw_commit.encode("utf-8")).hexdigest()

        rec = MemoryRecord(
            record_id=record_id,
            event_type=event_type,
            context_binding=context_binding,
            summary=summary,
            details=sanitized,
            commitment_hash=commit_hash,
        )
        self._records[record_id] = rec
        return rec

    def list_records_for_client(self, client_id: str) -> List[MemoryRecord]:
        """Retrieves memory records bound to a specific client scope."""
        return [r for r in self._records.values() if r.context_binding.client_id == client_id]

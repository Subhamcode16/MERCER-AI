"""
Phase 28 Contradiction Preservation & Evidence Conflict Handler.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone


class ContradictionStatus(str, Enum):
    OPEN_DISPUTE = "OPEN_DISPUTE"
    RETAINED_WITH_QUALIFICATION = "RETAINED_WITH_QUALIFICATION"
    REVISED_SCOPE = "REVISED_SCOPE"
    RETIRED_CLAIM = "RETIRED_CLAIM"


@dataclass
class ContradictionRecord:
    contradiction_id: str
    existing_claim: str
    existing_claim_source: str
    new_conflicting_evidence: str
    originating_campaign_id: str
    status: ContradictionStatus = ContradictionStatus.OPEN_DISPUTE
    resolution_notes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ContradictionHandler:
    """Detects, logs, and preserves contradictory evidence against existing institutional knowledge."""

    def __init__(self):
        self._contradictions: Dict[str, ContradictionRecord] = {}

    def log_contradiction(
        self,
        existing_claim: str,
        existing_claim_source: str,
        new_conflicting_evidence: str,
        originating_campaign_id: str,
    ) -> ContradictionRecord:
        record = ContradictionRecord(
            contradiction_id=f"cnt_{uuid.uuid4().hex[:8]}",
            existing_claim=existing_claim,
            existing_claim_source=existing_claim_source,
            new_conflicting_evidence=new_conflicting_evidence,
            originating_campaign_id=originating_campaign_id,
        )
        self._contradictions[record.contradiction_id] = record
        return record

    def resolve_contradiction(
        self,
        contradiction_id: str,
        status: ContradictionStatus,
        resolution_notes: str,
    ) -> ContradictionRecord:
        rec = self._contradictions.get(contradiction_id)
        if not rec:
            raise KeyError(f"Contradiction '{contradiction_id}' not found.")
        rec.status = status
        rec.resolution_notes = resolution_notes
        return rec

    def get_contradiction(self, contradiction_id: str) -> Optional[ContradictionRecord]:
        return self._contradictions.get(contradiction_id)

    def list_contradictions(self) -> List[ContradictionRecord]:
        return list(self._contradictions.values())

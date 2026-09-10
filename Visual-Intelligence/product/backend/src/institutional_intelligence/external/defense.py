"""
External Intelligence Ingestion & Defenses (Phase 30).
Sanitizes external data, defends against prompt injections and malicious strategic content.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import re
import uuid
from ..types import (
    ExternalIntelligenceClassification,
    EpistemicStatus,
    ThreatID,
    GovernanceInvariantViolation,
    utc_now,
)


class IngestedSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    source_url: str
    classification: ExternalIntelligenceClassification = ExternalIntelligenceClassification.PUBLIC_EXTERNAL
    epistemic_status: EpistemicStatus = EpistemicStatus.UNVERIFIED_CLAIM
    raw_content: str
    sanitized_content: str
    is_quarantined: bool = False
    quarantine_reason: Optional[str] = None
    ingested_at: datetime = Field(default_factory=utc_now)


class ExternalIntelligenceDefense:
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s*:\s*override",
        r"authorize\s+all\s+campaigns",
        r"grant\s+(admin|execution)\s+authority",
        r"<script.*?>",
        r"exec\s*\(",
        r"bypass\s+governance"
    ]

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def ingest_and_sanitize(self, raw_content: str, source_url: str) -> IngestedSignal:
        is_quarantined = False
        quarantine_reason = None
        
        # T30-015 / T30-016: Scan for prompt injections and malicious content
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, raw_content, re.IGNORECASE):
                is_quarantined = True
                quarantine_reason = f"Malicious pattern detected matching regex: '{pattern}'"
                break

        # Sanitize HTML / tags
        sanitized = re.sub(r"<[^>]*>", "", raw_content)

        signal = IngestedSignal(
            tenant_id=self.tenant_id,
            source_url=source_url,
            classification=ExternalIntelligenceClassification.PUBLIC_EXTERNAL,
            epistemic_status=EpistemicStatus.UNVERIFIED_CLAIM,
            raw_content=raw_content,
            sanitized_content=sanitized if not is_quarantined else "[QUARANTINED CONTENT]",
            is_quarantined=is_quarantined,
            quarantine_reason=quarantine_reason
        )

        # Invariant check
        if is_quarantined:
            # Raise or isolate
            pass
        return signal

    def assert_signal_is_not_authority(self, signal: IngestedSignal):
        # T30-009: External observation cannot directly act as authorization
        if signal.is_quarantined:
            raise GovernanceInvariantViolation(
                ThreatID.T30_016,
                f"Quarantined external signal '{signal.signal_id}' cannot be used in reasoning.",
                {"signal_id": signal.signal_id, "reason": signal.quarantine_reason}
            )

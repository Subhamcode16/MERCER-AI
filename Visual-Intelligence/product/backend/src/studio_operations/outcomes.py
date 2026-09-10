"""
Phase 15 Outcome Observation Engine.
Consumes post-execution external observations, tags them UNTRUSTED_EXTERNAL_OBSERVATION, and sanitizes payloads.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from src.studio_operations.exceptions import ExternalOutcomeValidationError, ClientContextViolation

@dataclass
class ExternalOutcomeRecord:
    outcome_id: str
    client_id: str
    campaign_id: str
    deliverable_id: str
    platform: str
    metrics: Dict[str, Any]
    observation_tag: str = "UNTRUSTED_EXTERNAL_OBSERVATION"
    raw_payload_summary: str = ""
    sanitized: bool = True
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class OutcomeObservationEngine:
    """Ingests and sanitizes post-execution platform outcomes and analytics."""

    def __init__(self):
        self._outcomes: Dict[str, ExternalOutcomeRecord] = {}

    def record_outcome(
        self,
        requesting_client_id: str,
        outcome_id: str,
        client_id: str,
        campaign_id: str,
        deliverable_id: str,
        platform: str,
        metrics: Dict[str, Any],
        raw_feedback: str = ""
    ) -> ExternalOutcomeRecord:
        """Records an external observation, sanitizing inputs and enforcing UNTRUSTED_EXTERNAL_OBSERVATION tag."""
        if requesting_client_id != client_id:
            raise ClientContextViolation(
                f"Cannot record outcome for client '{client_id}' from context '{requesting_client_id}'."
            )

        # Sanitize feedback text for prompt injection / code injection patterns
        sanitized_summary = self._sanitize_text(raw_feedback)

        # Ensure numeric metrics are clean numbers
        sanitized_metrics = {}
        for k, v in metrics.items():
            if isinstance(v, (int, float)):
                sanitized_metrics[k] = v
            elif isinstance(v, str) and v.replace(".", "", 1).isdigit():
                sanitized_metrics[k] = float(v)
            else:
                sanitized_metrics[k] = str(v)[:100]  # truncate unknown strings

        record = ExternalOutcomeRecord(
            outcome_id=outcome_id,
            client_id=client_id,
            campaign_id=campaign_id,
            deliverable_id=deliverable_id,
            platform=platform,
            metrics=sanitized_metrics,
            observation_tag="UNTRUSTED_EXTERNAL_OBSERVATION",
            raw_payload_summary=sanitized_summary,
            sanitized=True
        )
        self._outcomes[outcome_id] = record
        return record

    def get_outcomes_for_deliverable(
        self, requesting_client_id: str, deliverable_id: str
    ) -> List[ExternalOutcomeRecord]:
        """Retrieves external observations for a deliverable with client isolation."""
        return [
            o for o in self._outcomes.values()
            if o.deliverable_id == deliverable_id and o.client_id == requesting_client_id
        ]

    def _sanitize_text(self, text: str) -> str:
        """Sanitizes text strings to prevent prompt injection or script injection."""
        if not text:
            return ""
        forbidden = ["<script>", "SYSTEM:", "IGNORE ALL PREVIOUS INSTRUCTIONS", "DROP TABLE", "exec("]
        clean = text
        for term in forbidden:
            clean = clean.replace(term, "[REDACTED]")
        return clean[:500]

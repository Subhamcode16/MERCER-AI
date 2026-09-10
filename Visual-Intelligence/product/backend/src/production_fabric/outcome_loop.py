"""
Phase 17 Production Outcome Loop.
Ingests provider execution outcomes, analytics, feedback, and trend observations.
Enforces INV-17-005: External Observation Is Not Truth (Tagged explicitly UNTRUSTED_EXTERNAL_OBSERVATION).
"""

import hashlib
import json
from typing import Dict, Any, List, Optional
from src.production_fabric.production_models import ProductionOutcome, ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import OutcomeObservationError

class ProductionOutcomeLoop:
    """Loop ingesting external observations with strict trust classification and provenance tracking."""

    def __init__(self):
        self._outcomes: Dict[str, ProductionOutcome] = {}
        self._payload_hashes: Dict[str, str] = {}

    def ingest_outcome(
        self,
        outcome_id: str,
        client_id: str,
        campaign_id: str,
        deliverable_id: str,
        provider: str,
        external_post_id: str,
        reach: int,
        engagement_rate: float,
        studio_orchestrator: Any,
        raw_payload: Optional[Dict[str, Any]] = None
    ) -> ProductionOutcome:
        """Ingests external platform outcome with payload commitment hashing and untrusted tagging."""
        if not outcome_id or not outcome_id.strip():
            raise OutcomeObservationError("outcome_id cannot be empty.")

        payload_bytes = json.dumps(raw_payload or {}, sort_keys=True).encode("utf-8")
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()

        outcome = ProductionOutcome(
            outcome_id=outcome_id,
            client_id=client_id,
            campaign_id=campaign_id,
            deliverable_id=deliverable_id,
            provider=provider,
            external_post_id=external_post_id,
            reach=reach,
            engagement_rate=engagement_rate,
            provenance="UNTRUSTED_EXTERNAL_OBSERVATION"
        )
        self._outcomes[outcome_id] = outcome
        self._payload_hashes[outcome_id] = payload_hash

        # Dispatch outcome to Phase 15 Studio Operations outcome observation engine
        studio_orchestrator.outcome_engine.record_outcome(
            requesting_client_id=client_id,
            outcome_id=outcome_id,
            client_id=client_id,
            campaign_id=campaign_id,
            deliverable_id=deliverable_id,
            platform=provider,
            metrics={"reach": reach, "engagement_rate": engagement_rate},
            raw_feedback=f"external_post_id:{external_post_id}"
        )

        return outcome

    def get_outcome(self, outcome_id: str) -> ProductionOutcome:
        if outcome_id not in self._outcomes:
            raise OutcomeObservationError(f"Outcome '{outcome_id}' not found.")
        return self._outcomes[outcome_id]

    def list_outcomes_for_client(self, client_id: str) -> List[ProductionOutcome]:
        return [o for o in self._outcomes.values() if o.client_id == client_id]

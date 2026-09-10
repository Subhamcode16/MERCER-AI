"""
Phase 18 Creative Outcome Attribution Engine.

Links external outcome observations to creative direction, staff assignments,
visual DNA, copy strategy, trend observations, human approvals, and execution timing.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import uuid

from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.exceptions import (
    AttributionError,
    CrossClientIntelligenceViolation,
)


@dataclass(frozen=True)
class AttributionRecord:
    """Immutable attribution record linking outcome observation to artifact lineage."""
    attribution_id: str
    observation_id: str
    client_id: str
    campaign_id: str
    deliverable_id: str
    work_item_id: str
    staff_ids: List[str]
    creative_direction_id: str
    visual_dna_summary: str
    copy_strategy_summary: str
    trend_observation_ids: List[str]
    approval_id: str
    provider_operation_id: str
    confidence_score: float = 0.9
    timestamp: float = field(default_factory=time.time)


class CreativeOutcomeAttributionEngine:
    """Attributes observed external outcomes to upstream creative and operational inputs."""

    def __init__(self):
        self._attributions: Dict[str, AttributionRecord] = {}

    def attribute_outcome(
        self,
        requesting_client_id: str,
        observation: OutcomeObservation,
        staff_ids: Optional[List[str]] = None,
        creative_direction_id: str = "cd_default",
        visual_dna_summary: str = "Standard Visual DNA",
        copy_strategy_summary: str = "Standard Copy Strategy",
        trend_observation_ids: Optional[List[str]] = None,
        approval_id: str = "appr_default",
        provider_operation_id: str = "op_default",
    ) -> AttributionRecord:
        """Constructs an attribution record preserving lineage without unsupported causal leaps."""
        if requesting_client_id != observation.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot attribute outcome for '{observation.client_id}'."
            )

        attribution_id = f"attr_{uuid.uuid4().hex[:12]}"
        record = AttributionRecord(
            attribution_id=attribution_id,
            observation_id=observation.observation_id,
            client_id=observation.client_id,
            campaign_id=observation.campaign_id,
            deliverable_id=observation.deliverable_id,
            work_item_id=observation.work_item_id,
            staff_ids=staff_ids or ["staff_cd_1", "staff_designer_1"],
            creative_direction_id=creative_direction_id,
            visual_dna_summary=visual_dna_summary,
            copy_strategy_summary=copy_strategy_summary,
            trend_observation_ids=trend_observation_ids or [],
            approval_id=approval_id,
            provider_operation_id=provider_operation_id,
            confidence_score=0.9,
        )

        self._attributions[attribution_id] = record
        return record

    def get_attribution(
        self, requesting_client_id: str, attribution_id: str
    ) -> Optional[AttributionRecord]:
        """Retrieves attribution record with strict client isolation."""
        rec = self._attributions.get(attribution_id)
        if not rec:
            return None
        if requesting_client_id != rec.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot access attribution owned by '{rec.client_id}'."
            )
        return rec

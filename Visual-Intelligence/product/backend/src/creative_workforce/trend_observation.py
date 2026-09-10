"""
Phase 14 Trend Intelligence Engine
----------------------------------
Collects real-world trend observations from external sources.
Enforces INV-14-W006: External observations are explicitly UNTRUSTED_EXTERNAL_OBSERVATION.
Sanitizes prompt injection and security policy mutation attempts.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid

from src.creative_workforce.exceptions import UntrustedObservationInjectionError

FORBIDDEN_KEYWORDS = [
    "allow capability",
    "grant admin",
    "override policy",
    "bypass auth",
    "disable security",
    "unlock gate",
    "sudo",
]

@dataclass(frozen=True)
class TrendObservation:
    """Immutable record of an external creative trend observation."""
    observation_id: str
    source_url: str
    category: str
    raw_content: str
    extracted_patterns: List[str]
    confidence: float = 0.8
    trust_status: str = "UNTRUSTED_EXTERNAL_OBSERVATION"
    collected_at: float = field(default_factory=time.time)

class TrendIntelligenceEngine:
    """Engine ingesting external trend intelligence safely."""

    def __init__(self):
        self._observations: Dict[str, TrendObservation] = {}

    def collect_observation(
        self,
        source_url: str,
        category: str,
        raw_content: str,
        extracted_patterns: Optional[List[str]] = None,
    ) -> TrendObservation:
        """Ingests an external observation, sanitizing prompt injection and enforcing untrusted status."""
        lowered = raw_content.lower()
        if any(kw in lowered for kw in FORBIDDEN_KEYWORDS):
            raise UntrustedObservationInjectionError(
                "External trend observation contains forbidden policy-mutation or prompt injection directives."
            )

        obs_id = f"obs-{uuid.uuid4().hex[:8]}"
        patterns = extracted_patterns or [category]

        obs = TrendObservation(
            observation_id=obs_id,
            source_url=source_url,
            category=category,
            raw_content=raw_content,
            extracted_patterns=patterns,
            trust_status="UNTRUSTED_EXTERNAL_OBSERVATION",
        )
        self._observations[obs_id] = obs
        return obs

    def list_observations(self, category: Optional[str] = None) -> List[TrendObservation]:
        """Lists collected trend observations."""
        if category:
            return [o for o in self._observations.values() if o.category == category]
        return list(self._observations.values())

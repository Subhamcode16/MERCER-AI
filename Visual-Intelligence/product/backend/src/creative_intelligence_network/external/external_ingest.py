"""
External Intelligence Ingestion Pipeline with prompt injection sanitization.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
import re
from .trust_model import ExternalObservation, SourceReliability
from ..graph.models import IntelligenceClassification, GraphEntity, EntityType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class ExternalIntelligenceIngest:
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"system\s+prompt\s*:",
        r"grant\s+(admin|operator|privilege)",
        r"execute\s+command\s*:",
        r"elevate\s+permission",
        r"set\s+is_admin\s*=\s*true",
        r"override\s+governance",
    ]

    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._observations: Dict[str, ExternalObservation] = {}

    def ingest_external_observation(
        self,
        source_url: str,
        source_name: str,
        source_reliability: SourceReliability,
        raw_content: str,
    ) -> ExternalObservation:
        detected_injections = []
        lower_raw = raw_content.lower()

        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, lower_raw):
                detected_injections.append(f"DETECTED_INJECTION_PATTERN: {pattern}")

        # Prompt Injection Defense: neutralize executable instructions
        sanitized = raw_content
        for pattern in self.INJECTION_PATTERNS:
            sanitized = re.sub(pattern, "[STRIPPED_DIRECTIVE]", sanitized, flags=re.IGNORECASE)

        is_safe = len(detected_injections) == 0 and source_reliability != SourceReliability.UNTRUSTED_ADVERSARIAL
        obs_id = f"EXT-OBS-{hashlib.sha256(f'{source_url}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"

        obs = ExternalObservation(
            observation_id=obs_id,
            source_url=source_url,
            source_name=source_name,
            source_reliability=source_reliability,
            raw_content=raw_content,
            sanitized_content=sanitized,
            detected_injection_patterns=detected_injections,
            is_safe_for_synthesis=is_safe,
            corroboration_state="UNCORROBORATED" if is_safe else "REJECTED_INJECTION",
        )

        self._observations[obs_id] = obs

        # Sync to graph as PUBLIC_EXTERNAL entity
        if is_safe:
            entity = GraphEntity(
                entity_id=obs_id,
                entity_type=EntityType.EXTERNAL_OBSERVATION,
                tenant_id="PUBLIC_EXTERNAL",
                classification=IntelligenceClassification.PUBLIC_EXTERNAL,
                name=f"External Observation: {source_name}",
                properties={
                    "source_url": source_url,
                    "reliability": source_reliability.value,
                    "content": sanitized[:200],
                },
            )
            self.graph.add_entity(entity)

        return obs

    def get_observation(self, obs_id: str) -> Optional[ExternalObservation]:
        return self._observations.get(obs_id)

    def list_observations(self) -> List[ExternalObservation]:
        return list(self._observations.values())

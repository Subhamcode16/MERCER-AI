"""
Organizational Intelligence Graph Models & Types for Phase 29.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import hashlib
import json
from pydantic import BaseModel, Field


class IntelligenceClassification(str, Enum):
    CLIENT_PRIVATE = "CLIENT_PRIVATE"
    INSTITUTIONAL = "INSTITUTIONAL"
    PUBLIC_EXTERNAL = "PUBLIC_EXTERNAL"
    SYSTEM_GENERATED_INFERENCE = "SYSTEM_GENERATED_INFERENCE"


class EntityType(str, Enum):
    CLIENT = "CLIENT"
    BRAND = "BRAND"
    PRODUCT = "PRODUCT"
    AUDIENCE = "AUDIENCE"
    CAMPAIGN = "CAMPAIGN"
    CAMPAIGN_DECISION = "CAMPAIGN_DECISION"
    CREATIVE_DIRECTION = "CREATIVE_DIRECTION"
    ASSET = "ASSET"
    ASSET_VERSION = "ASSET_VERSION"
    OUTCOME = "OUTCOME"
    EXPERIMENT = "EXPERIMENT"
    LEARNING_SIGNAL = "LEARNING_SIGNAL"
    KNOWLEDGE_CLAIM = "KNOWLEDGE_CLAIM"
    VISUAL_DNA_TOKEN = "VISUAL_DNA_TOKEN"
    WORKER = "WORKER"
    SKILL = "SKILL"
    HYPOTHESIS = "HYPOTHESIS"
    STRATEGIC_SIGNAL = "STRATEGIC_SIGNAL"
    SCENARIO = "SCENARIO"
    RECOMMENDATION = "RECOMMENDATION"
    HUMAN_DECISION = "HUMAN_DECISION"
    RISK = "RISK"
    OPPORTUNITY = "OPPORTUNITY"
    EXTERNAL_OBSERVATION = "EXTERNAL_OBSERVATION"


class RelationType(str, Enum):
    INFORMS = "INFORMS"
    CONTRADICTS = "CONTRADICTS"
    SUPPORTS = "SUPPORTS"
    DERIVED_FROM = "DERIVED_FROM"
    APPLIES_TO = "APPLIES_TO"
    EVALUATED_BY = "EVALUATED_BY"
    DECIDED_BY = "DECIDED_BY"
    TESTED_IN = "TESTED_IN"
    PRECEDED_BY = "PRECEDED_BY"
    BOUND_BY = "BOUND_BY"
    LEADS_TO = "LEADS_TO"


class GraphEntity(BaseModel):
    entity_id: str
    entity_type: EntityType
    tenant_id: str
    classification: IntelligenceClassification
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    provenance_hashes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    def compute_hash(self) -> str:
        payload = {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "tenant_id": self.tenant_id,
            "classification": self.classification.value,
            "properties": self.properties,
            "provenance_hashes": self.provenance_hashes,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


class GraphRelationship(BaseModel):
    relationship_id: str
    source_id: str
    target_id: str
    relation_type: RelationType
    tenant_id: str
    classification: IntelligenceClassification
    scope: str
    confidence: float = 1.0
    evidence_refs: List[str] = Field(default_factory=list)
    provenance_hash: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lifecycle_status: str = "ACTIVE"

    def compute_hash(self) -> str:
        payload = {
            "relationship_id": self.relationship_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type.value,
            "tenant_id": self.tenant_id,
            "classification": self.classification.value,
            "scope": self.scope,
            "confidence": self.confidence,
            "evidence_refs": self.evidence_refs,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

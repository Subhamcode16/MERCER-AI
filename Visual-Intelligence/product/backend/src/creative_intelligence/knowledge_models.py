"""
Phase 19 - Knowledge Models & Schemas.

Defines typed structures for knowledge graph nodes, edges, provenance records,
generalized patterns, institutional strategies, workforce recommendations, and metrics.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional, Set
from pydantic import BaseModel, Field


class ProvenanceRecord(BaseModel):
    """Immutable hash-chained provenance trace for institutional knowledge assets."""
    record_id: str = Field(default_factory=lambda: f"prov_{uuid.uuid4().hex[:12]}")
    source_client_id: Optional[str] = None  # None if anonymized/generalized
    source_phase: str  # e.g., "Phase18", "Phase17", "Phase15"
    evidence_hash: str  # SHA-256 hash of original telemetry/deliverable
    parent_provenance_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    provenance_hash: str = ""

    def compute_hash(self) -> str:
        content = f"{self.record_id}:{self.source_client_id}:{self.source_phase}:{self.evidence_hash}:{self.parent_provenance_id}:{self.created_at}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: Any) -> None:
        if not self.provenance_hash:
            self.provenance_hash = self.compute_hash()


class GraphNode(BaseModel):
    """Node in the Institutional Knowledge Graph (Dual-Namespace: Client vs Global)."""
    node_id: str
    namespace: str  # "client" or "global"
    node_type: str  # "Client", "Campaign", "Deliverable", "Artifact", "InstitutionalPattern", "ValidatedStrategy"
    attributes: Dict[str, Any] = Field(default_factory=dict)
    provenance_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class GraphEdge(BaseModel):
    """Directed edge in the Institutional Knowledge Graph."""
    edge_id: str = Field(default_factory=lambda: f"edge_{uuid.uuid4().hex[:12]}")
    source_node_id: str
    target_node_id: str
    relation_type: str  # "PRODUCED", "EVALUATED_BY", "DERIVED_FROM", "GENERALIZED_TO", "EVOLVED_FROM"
    confidence_score: float = 1.0
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: float = Field(default_factory=time.time)


class InstitutionalPattern(BaseModel):
    """Cross-client abstract pattern scrubbed of all PII/client identifiers."""
    pattern_id: str = Field(default_factory=lambda: f"pat_{uuid.uuid4().hex[:12]}")
    pattern_name: str
    domain: str  # e.g., "fashion_ecom", "luxury_campaign", "video_production"
    abstract_structure: Dict[str, Any]
    support_count: int = 1
    confidence_score: float = 0.5
    provenance_ids: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    last_validated_at: float = Field(default_factory=time.time)


class ValidatedStrategy(BaseModel):
    """Versioned institutional strategy entry in the strategy registry."""
    strategy_id: str = Field(default_factory=lambda: f"strat_{uuid.uuid4().hex[:12]}")
    strategy_name: str
    version: str = "1.0.0"
    pattern_id: str
    domain: str
    parameters: Dict[str, Any]
    status: str = "PROPOSED"  # "PROPOSED", "VALIDATED", "ACTIVE", "STALE", "RETIRED", "ROLLED_BACK"
    accuracy_score: float = 0.0
    latency_ms: float = 0.0
    failure_rate: float = 0.0
    usage_count: int = 0
    created_at: float = Field(default_factory=time.time)
    retired_at: Optional[float] = None
    retirement_reason: Optional[str] = None


class WorkforceRecommendation(BaseModel):
    """Workforce structure or skill refinement proposal (NON-EXECUTABLE)."""
    recommendation_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:12]}")
    target_agent_id: str
    recommendation_type: str  # "SKILL_REFINEMENT", "PROMPT_OPTIMIZATION", "WORKFLOW_ROUTING"
    rationale: str
    suggested_changes: Dict[str, Any]
    evidence_pattern_ids: List[str] = Field(default_factory=list)
    requires_human_approval: bool = True
    executed: bool = False  # Always False from intelligence layer
    created_at: float = Field(default_factory=time.time)


class CreativeIntelligenceMetrics(BaseModel):
    """Dashboard telemetry metrics snapshot."""
    total_nodes: int = 0
    client_nodes: int = 0
    global_nodes: int = 0
    total_edges: int = 0
    discovered_patterns: int = 0
    active_strategies: int = 0
    retired_strategies: int = 0
    workforce_recommendations: int = 0
    provenance_chain_integrity: bool = True
    data_confidentiality_passed: bool = True
    policy_isolation_passed: bool = True

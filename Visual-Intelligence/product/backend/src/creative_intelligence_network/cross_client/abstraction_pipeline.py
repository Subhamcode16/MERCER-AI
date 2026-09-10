"""
Cross-Client Abstraction Pipeline enforcing strict de-identification, k-anonymity, and leakage gates.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
from pydantic import BaseModel, Field
from .leakage_analyzer import SemanticLeakageAnalyzer
from ..graph.models import IntelligenceClassification, GraphEntity, EntityType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class CrossClientAbstractionRequest(BaseModel):
    source_tenant_id: str
    source_entity_id: str
    raw_insight: str
    client_private_tokens: List[str]
    sample_size_campaigns: int
    requested_by: str


class AbstractionResult(BaseModel):
    success: bool
    generalized_knowledge_id: Optional[str] = None
    abstracted_insight: Optional[str] = None
    classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE
    leakage_risk_score: float = 0.0
    violations: List[str] = Field(default_factory=list)
    operator_approved: bool = False


class CrossClientAbstractionPipeline:
    MIN_K_ANONYMITY_CAMPAIGNS = 5

    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._institutional_knowledge: Dict[str, str] = {}

    def process_abstraction(
        self,
        req: CrossClientAbstractionRequest,
        operator_approved: bool = False,
    ) -> AbstractionResult:
        # Step 1: Eligibility & K-Anonymity Check
        if req.sample_size_campaigns < self.MIN_K_ANONYMITY_CAMPAIGNS:
            return AbstractionResult(
                success=False,
                violations=[f"INSUFFICIENT_K_ANONYMITY: Requires at least {self.MIN_K_ANONYMITY_CAMPAIGNS} aggregated campaigns, got {req.sample_size_campaigns}."],
            )

        # Step 2: Redaction & Generalization
        generalized_text = req.raw_insight
        for token in req.client_private_tokens:
            generalized_text = generalized_text.replace(token, "[REDACTED_ENTITY]")

        # Step 3: Semantic Leakage Analysis
        is_safe, risk_score, violations = SemanticLeakageAnalyzer.evaluate_leakage(
            generalized_text, req.client_private_tokens
        )

        if not is_safe:
            return AbstractionResult(
                success=False,
                leakage_risk_score=risk_score,
                violations=violations,
            )

        # Step 4: Governance Gate
        if not operator_approved:
            return AbstractionResult(
                success=False,
                abstracted_insight=generalized_text,
                leakage_risk_score=risk_score,
                violations=["AWAITING_OPERATOR_GOVERNANCE_APPROVAL"],
            )

        # Step 5: Promotion to INSTITUTIONAL
        inst_id = f"INST-KNOW-{hashlib.sha256(generalized_text.encode()).hexdigest()[:12]}"
        self._institutional_knowledge[inst_id] = generalized_text

        # Add to graph as INSTITUTIONAL entity
        entity = GraphEntity(
            entity_id=inst_id,
            entity_type=EntityType.KNOWLEDGE_CLAIM,
            tenant_id="GLOBAL_INSTITUTIONAL",
            classification=IntelligenceClassification.INSTITUTIONAL,
            name=f"Institutional Pattern: {inst_id}",
            properties={
                "abstracted_insight": generalized_text,
                "k_anonymity_campaigns": req.sample_size_campaigns,
                "approved_by": req.requested_by,
            },
        )
        self.graph.add_entity(entity)

        return AbstractionResult(
            success=True,
            generalized_knowledge_id=inst_id,
            abstracted_insight=generalized_text,
            classification=IntelligenceClassification.INSTITUTIONAL,
            leakage_risk_score=risk_score,
            operator_approved=True,
        )

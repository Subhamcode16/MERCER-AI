"""
Phase 28 Governed Knowledge Promotion Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone

from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.creative_learning.hypotheses.hypothesis_store import HypothesisScope


class PromotionLifecycleState(str, Enum):
    OBSERVED = "OBSERVED"
    PROVISIONAL = "PROVISIONAL"
    REVIEWED = "REVIEWED"
    VALIDATED = "VALIDATED"
    PROMOTED = "PROMOTED"
    ROLLED_BACK = "ROLLED_BACK"
    RETIRED = "RETIRED"


@dataclass
class KnowledgePromotionProposal:
    proposal_id: str
    claim: str
    scope: HypothesisScope
    client_id: Optional[str]
    brand_id: Optional[str]
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    confidence: float
    affected_knowledge_objects: List[str]
    expected_benefit: str
    known_risks: List[str]
    rollback_plan: str
    state: PromotionLifecycleState = PromotionLifecycleState.PROVISIONAL
    reviewed_by: Optional[str] = None
    review_comments: Optional[str] = None
    promoted_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class KnowledgePromotionEngine:
    """Manages knowledge promotion lifecycle, role-based approval gates, and rollback execution."""

    def __init__(self):
        self._proposals: Dict[str, KnowledgePromotionProposal] = {}

    def propose_promotion(
        self,
        claim: str,
        scope: HypothesisScope,
        supporting_evidence: List[str],
        affected_knowledge_objects: List[str],
        expected_benefit: str,
        known_risks: List[str],
        rollback_plan: str,
        client_id: Optional[str] = None,
        brand_id: Optional[str] = None,
        confidence: float = 0.88,
        contradicting_evidence: Optional[List[str]] = None,
    ) -> KnowledgePromotionProposal:
        # Cross-client privacy check: Global knowledge cannot include private client IDs without governed abstraction
        if scope == HypothesisScope.GLOBAL and client_id:
            raise PermissionError("Private client outcome cannot be promoted to GLOBAL scope directly. Invariant: Institutional Learning ≠ Cross-Client Leakage.")

        prop = KnowledgePromotionProposal(
            proposal_id=f"prm_{uuid.uuid4().hex[:8]}",
            claim=claim,
            scope=scope,
            client_id=client_id,
            brand_id=brand_id,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence or [],
            confidence=confidence,
            affected_knowledge_objects=affected_knowledge_objects,
            expected_benefit=expected_benefit,
            known_risks=known_risks,
            rollback_plan=rollback_plan,
        )
        self._proposals[prop.proposal_id] = prop
        return prop

    def review_and_decide(
        self,
        proposal_id: str,
        operator: OperatorContext,
        decision: str,  # "APPROVE", "REJECT", "REQUEST_REVISION"
        comments: str = "",
    ) -> KnowledgePromotionProposal:
        prop = self._proposals.get(proposal_id)
        if not prop:
            raise KeyError(f"Proposal '{proposal_id}' not found.")

        allowed_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.STUDIO_ADMIN, OperatorRole.SUPER_ADMIN}
        if operator.role not in allowed_roles:
            raise PermissionError(f"Operator '{operator.operator_id}' with role '{operator.role}' lacks authority to promote knowledge.")

        if decision == "APPROVE":
            prop.state = PromotionLifecycleState.PROMOTED
            prop.promoted_at = datetime.now(timezone.utc)
        elif decision == "REJECT":
            prop.state = PromotionLifecycleState.RETIRED
        else:
            prop.state = PromotionLifecycleState.REVIEWED

        prop.reviewed_by = operator.operator_id
        prop.review_comments = comments
        return prop

    def rollback_promotion(self, proposal_id: str, operator: OperatorContext, reason: str) -> KnowledgePromotionProposal:
        prop = self._proposals.get(proposal_id)
        if not prop:
            raise KeyError(f"Proposal '{proposal_id}' not found.")

        allowed_roles = {OperatorRole.CREATIVE_DIRECTOR, OperatorRole.BRAND_EXECUTIVE, OperatorRole.STUDIO_LEAD, OperatorRole.STUDIO_ADMIN, OperatorRole.SUPER_ADMIN}
        if operator.role not in allowed_roles:
            raise PermissionError(f"Operator '{operator.operator_id}' lacks authority to rollback knowledge.")

        prop.state = PromotionLifecycleState.ROLLED_BACK
        prop.review_comments = f"Rolled back: {reason}"
        return prop

    def get_proposal(self, proposal_id: str) -> Optional[KnowledgePromotionProposal]:
        return self._proposals.get(proposal_id)

    def list_proposals(self, state: Optional[PromotionLifecycleState] = None) -> List[KnowledgePromotionProposal]:
        if state:
            return [p for p in self._proposals.values() if p.state == state]
        return list(self._proposals.values())

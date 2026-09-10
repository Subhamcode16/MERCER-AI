"""
Tests for Phase 28 Knowledge Promotion and Contradiction Handling.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.creative_learning.hypotheses.hypothesis_store import HypothesisScope
from src.creative_learning.promotion import (
    KnowledgePromotionEngine,
    PromotionLifecycleState,
)
from src.creative_learning.contradiction import (
    ContradictionHandler,
    ContradictionStatus,
)


def test_knowledge_promotion_lifecycle_and_rollback():
    engine = KnowledgePromotionEngine()
    
    # Propose promotion
    prop = engine.propose_promotion(
        claim="Raking late sun lighting provides superior wool texture micro-contrast.",
        scope=HypothesisScope.BRAND,
        client_id="cli_01",
        brand_id="brd_01",
        supporting_evidence=["Autumn 2026 Lookbook A/B test results: +34% engagement lift."],
        affected_knowledge_objects=["Preset:Tailored_Outerwear_DNA"],
        expected_benefit="Higher aesthetic fidelity in luxury outerwear renders.",
        known_risks=["Excessive shadow clipping if contrast is over-amplified."],
        rollback_plan="Revert preset to balanced studio diffuse lighting baseline.",
    )
    assert prop.state == PromotionLifecycleState.PROVISIONAL

    # Unauthorized operator fails to approve
    unauth = OperatorContext(operator_id="op_intern", role=OperatorRole.STAFF_OPERATOR)
    with pytest.raises(PermissionError):
        engine.review_and_decide(prop.proposal_id, unauth, "APPROVE")

    # Authorized Creative Director approves
    cd = OperatorContext(operator_id="op_cd_01", role=OperatorRole.CREATIVE_DIRECTOR)
    approved = engine.review_and_decide(prop.proposal_id, cd, "APPROVE", "Validated against brand heritage guidelines.")
    assert approved.state == PromotionLifecycleState.PROMOTED

    # Rollback execution
    rolled_back = engine.rollback_promotion(prop.proposal_id, cd, "Observed texture clipping in print format.")
    assert rolled_back.state == PromotionLifecycleState.ROLLED_BACK


def test_contradiction_preservation_lifecycle():
    handler = ContradictionHandler()
    
    contra = handler.log_contradiction(
        existing_claim="Monochrome backgrounds always yield highest CTR.",
        existing_claim_source="2025 Summer Campaign Report",
        new_conflicting_evidence="Winter 2026 Gala campaign showed warm architectural lighting outperformed monochrome by +28%.",
        originating_campaign_id="camp_aw26",
    )
    assert contra.status == ContradictionStatus.OPEN_DISPUTE

    resolved = handler.resolve_contradiction(
        contra.contradiction_id,
        ContradictionStatus.REVISED_SCOPE,
        "Monochrome applies to digital accessories; warm architectural applies to luxury outerwear.",
    )
    assert resolved.status == ContradictionStatus.REVISED_SCOPE

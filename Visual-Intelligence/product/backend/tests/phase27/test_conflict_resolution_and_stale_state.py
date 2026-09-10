"""
Tests for Phase 27 Conflict Resolution and Stale State Guardrails.
"""
import pytest
from src.campaign_studio.conflict_resolution import (
    ConflictResolutionEngine,
    ConflictDomain,
    DepartmentPosition,
)
from src.campaign_studio.studio_governance import StudioGovernanceEngine
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole


def test_departmental_conflict_registration_and_resolution():
    engine = ConflictResolutionEngine()
    campaign_id = "camp_conf_01"

    pos1 = DepartmentPosition(
        department="Creative Direction",
        spokesperson_role="CREATIVE_DIRECTOR",
        standpoint="Strict Monochromatic Austerity",
        supporting_argument="Preserves luxury prestige and high-tailoring focus.",
        risk_assessment="Slightly lower viral engagement on TikTok.",
    )
    pos2 = DepartmentPosition(
        department="Performance Marketing",
        spokesperson_role="GROWTH_LEAD",
        standpoint="High-Chroma Neon Color Grading",
        supporting_argument="Boosts feed-stopping thumb scroll conversion by +15%.",
        risk_assessment="Dilutes heritage minimalist brand equity.",
    )

    conflict = engine.register_divergence(
        campaign_id=campaign_id,
        domain=ConflictDomain.AESTHETIC_VS_PERFORMANCE,
        topic="Hero Color Grading Strategy",
        positions=[pos1, pos2],
        recommended_compromise="Monochromatic Hero for Lookbook + High-Contrast Warm Accent for Story ads.",
    )
    assert conflict.resolved is False

    resolved = engine.resolve_conflict(
        campaign_id=campaign_id,
        conflict_id=conflict.conflict_id,
        resolution_decision="Approved recommended compromise.",
    )
    assert resolved.resolved is True
    assert resolved.resolution_notes == "Approved recommended compromise."


def test_governance_invariants_and_attribution_check():
    gov = StudioGovernanceEngine()
    
    # Check invalid causal attribution claim
    eval_causal = gov.evaluate_attribution_assertion("Campaign visual style proves causality and caused 100% of sales lift.")
    assert eval_causal.is_compliant is False
    assert any("Attribution ≠ Causal Proof" in v for v in eval_causal.violations)

    # Check valid transition governance
    op_intern = OperatorContext(operator_id="op_intern", role=OperatorRole.STAFF_OPERATOR, department="Ops")
    eval_trans = gov.evaluate_campaign_transition("STAGED", "LAUNCHED", op_intern, is_approved=False)
    assert eval_trans.is_compliant is False
    assert len(eval_trans.violations) == 2

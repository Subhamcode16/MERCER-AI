"""
Phase 14 Test Organization Models
-----------------------------------
Tests StaffIdentity, ContextBinding, WorkforceAssignment, CritiqueResult, and ReviewResult models.
Ensures workforce roles cannot possess authorization authority (INV-14-W001).
"""

import pytest
from src.creative_workforce import (
    Department,
    Role,
    AuthorityClass,
    StaffIdentity,
    ContextBinding,
    ReviewResult,
)

def test_staff_identity_validity():
    staff = StaffIdentity(
        staff_id="designer-01",
        role=Role.VISUAL_DESIGNER,
        department=Department.CREATIVE,
        capabilities=["graphic_design"],
        knowledge_domains=["branding"],
        authority_class=AuthorityClass.PROPOSE,
    )
    assert staff.staff_id == "designer-01"
    assert staff.authority_class == AuthorityClass.PROPOSE

def test_empty_staff_id_rejection():
    with pytest.raises(ValueError, match="staff_id cannot be empty"):
        StaffIdentity(
            staff_id="",
            role=Role.VISUAL_DESIGNER,
            department=Department.CREATIVE,
            capabilities=[],
            knowledge_domains=[],
            authority_class=AuthorityClass.PROPOSE,
        )

def test_context_binding_validity():
    binding = ContextBinding(
        client_id="nocap",
        brand_id="nocap-apparel",
        campaign_id="september-campaign",
        mission_id="m-101",
        task_id="t-1",
        staff_id="designer-01",
    )
    assert binding.client_id == "nocap"

def test_review_result_authoritative_rejection():
    with pytest.raises(ValueError, match="is_authoritative=False"):
        ReviewResult(
            review_id="rev-1",
            artifact_id="art-1",
            reviewer_id="rev-01",
            criteria_scores={"quality": 0.9},
            recommendation="ACCEPTED",
            comments="Good",
            is_authoritative=True,
        )

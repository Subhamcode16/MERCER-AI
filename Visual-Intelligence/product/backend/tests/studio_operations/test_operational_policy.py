"""
Unit tests for Phase 15 Operational Policy Engine.
"""

import pytest
from src.studio_operations.operational_policy import StudioOperationalPolicyEngine
from src.studio_operations.studio_models import ClientOperatingPolicy
from src.studio_operations.exceptions import OperationalPolicyViolation

def test_operational_policy_enforcement():
    engine = StudioOperationalPolicyEngine()
    policy = ClientOperatingPolicy(
        policy_id="pol_001",
        client_id="client_nocap",
        allowed_platforms=["instagram", "twitter"],
        allowed_capabilities=["draft_content", "review_content"]
    )

    assert engine.validate_action("client_nocap", policy, "draft", target_platform="instagram", capability="draft_content")

    # Forbidden platform
    with pytest.raises(OperationalPolicyViolation):
        engine.validate_action("client_nocap", policy, "draft", target_platform="tiktok")

    # Revision limit check
    engine.validate_revision_limit(policy, current_revisions=2)
    with pytest.raises(OperationalPolicyViolation):
        engine.validate_revision_limit(policy, current_revisions=3)

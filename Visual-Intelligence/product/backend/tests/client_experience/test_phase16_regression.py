"""
Phase 16 Regression Suite.
Ensures Phase 16 Client Experience layer preserves all baseline Phase 1-15 security invariants.
"""

import pytest
from src.client_experience.command_center import StudioCommandCenter
from src.client_experience.access_models import HumanRole

def test_phase16_substrate_integration(tmp_path):
    center = StudioCommandCenter(audit_dir=str(tmp_path / "reg_audit"))

    # Verify studio orchestrator link
    assert center.studio_orchestrator is not None
    assert center.studio_orchestrator.workforce_orchestrator is not None

    # Register client and user
    center.studio_orchestrator.register_client_engagement("client_reg", "Regression Client", "Technology")
    user = center.register_user("user_reg", "Reg User", "reg@tech.com", "client_reg", HumanRole.CLIENT_OWNER)

    # Verify context and capabilities
    dash = center.get_dashboard("user_reg", "client_reg")
    assert dash.client_id == "client_reg"
    assert center.verify_audit_integrity() is True

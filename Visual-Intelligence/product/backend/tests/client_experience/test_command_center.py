"""
Unit tests for Phase 16 Studio Command Center.
"""

import pytest
from src.client_experience.command_center import StudioCommandCenter
from src.client_experience.access_models import HumanRole

def test_command_center_flow(tmp_path):
    audit_dir = str(tmp_path / "cmd_audit")
    center = StudioCommandCenter(audit_dir=audit_dir)

    # 1. Register Studio Client & Brand in Phase 15 orchestrator
    center.studio_orchestrator.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    center.studio_orchestrator.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")

    # 2. Register Human User in Phase 16 Command Center
    user = center.register_user("user_owner", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    # 3. Get Dashboard
    dash = center.get_dashboard("user_owner", "client_nocap")
    assert dash.client_id == "client_nocap"

    # 4. Request Campaign
    camp = center.request_campaign("user_owner", "client_nocap", "camp_001", "brand_nocap", "September Drop", "Growth")
    assert camp.campaign_id == "camp_001"

    # 5. Verify Audit
    assert center.verify_audit_integrity() is True

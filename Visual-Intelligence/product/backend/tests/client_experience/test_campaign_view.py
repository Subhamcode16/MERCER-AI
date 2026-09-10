"""
Unit tests for Phase 16 Campaign Command Center View.
"""

import pytest
from src.client_experience.campaign_view import CampaignCommandCenterView
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_campaign_view_launch_and_list(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "camp_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")

    view = CampaignCommandCenterView()
    user = UserIdentity("user_a", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    dto = view.request_campaign(user, orch, "camp_001", "brand_nocap", "September Campaign", "Brand growth")
    assert dto.campaign_id == "camp_001"
    assert dto.status == "ACTIVE"

    list_dtos = view.list_campaigns(user, orch)
    assert len(list_dtos) == 1
    assert list_dtos[0].title == "September Campaign"

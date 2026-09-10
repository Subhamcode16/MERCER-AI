"""
Unit tests for Phase 15 Campaign Lifecycle Manager.
"""

import pytest
from src.studio_operations.campaign_manager import CampaignLifecycleManager
from src.studio_operations.studio_models import CampaignStatus
from src.studio_operations.exceptions import CampaignStateViolation, ClientContextViolation

def test_campaign_lifecycle_transitions():
    mgr = CampaignLifecycleManager()
    camp = mgr.create_campaign("client_nocap", "camp_001", "client_nocap", "brand_nocap", "Fall Campaign", "Increase engagement")
    assert camp.status == CampaignStatus.PLANNED

    camp = mgr.transition_campaign("client_nocap", "camp_001", CampaignStatus.ACTIVE)
    assert camp.status == CampaignStatus.ACTIVE

    camp = mgr.transition_campaign("client_nocap", "camp_001", CampaignStatus.PAUSED)
    assert camp.status == CampaignStatus.PAUSED

    # Cannot transition directly from PAUSED to COMPLETED without RESUMED / ACTIVE
    with pytest.raises(CampaignStateViolation):
        mgr.transition_campaign("client_nocap", "camp_001", CampaignStatus.COMPLETED)

    # Cross-client leakage check
    with pytest.raises(ClientContextViolation):
        mgr.get_campaign("client_other", "camp_001")

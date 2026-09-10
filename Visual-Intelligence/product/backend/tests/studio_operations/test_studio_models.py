"""
Unit tests for Phase 15 Studio Operations Data Models and Validation Guards.
"""

import pytest
from src.studio_operations.studio_models import (
    StudioClient, StudioBrand, ClientOperatingPolicy, Campaign, Workstream, Deliverable,
    DeliverableStatus, CampaignStatus, DeliverableType, OperationalPriority, CampaignCadence
)
from src.studio_operations.exceptions import ClientContextViolation, DeliverableStateViolation

def test_studio_client_validation():
    client = StudioClient(client_id="client_nocap", name="NOCAP Studio", industry="Fashion")
    assert client.client_id == "client_nocap"
    assert client.name == "NOCAP Studio"

    with pytest.raises(ClientContextViolation):
        StudioClient(client_id="", name="Invalid", industry="Fashion")

    with pytest.raises(ClientContextViolation):
        StudioClient(client_id="client_x", name="   ", industry="Fashion")

def test_studio_brand_validation():
    brand = StudioBrand(brand_id="brand_nocap", client_id="client_nocap", brand_name="NOCAP")
    assert brand.brand_id == "brand_nocap"

    with pytest.raises(ClientContextViolation):
        StudioBrand(brand_id="", client_id="client_nocap", brand_name="NOCAP")

def test_deliverable_state_machine():
    d = Deliverable(
        deliverable_id="del_001",
        workstream_id="ws_001",
        campaign_id="camp_001",
        client_id="client_nocap",
        title="Hero Social Post"
    )
    assert d.status == DeliverableStatus.PLANNED

    # Valid transitions: PLANNED -> IN_PROGRESS -> DRAFT -> CRITIQUE -> REVIEW -> APPROVED -> READY_FOR_EXECUTION -> EXECUTED -> OBSERVED -> LEARNED
    d.transition_to(DeliverableStatus.IN_PROGRESS)
    assert d.status == DeliverableStatus.IN_PROGRESS

    d.transition_to(DeliverableStatus.DRAFT)
    assert d.status == DeliverableStatus.DRAFT

    d.transition_to(DeliverableStatus.CRITIQUE)
    assert d.status == DeliverableStatus.CRITIQUE

    d.transition_to(DeliverableStatus.REVIEW)
    assert d.status == DeliverableStatus.REVIEW

    d.transition_to(DeliverableStatus.APPROVED)
    assert d.status == DeliverableStatus.APPROVED

    # Invalid transition directly from APPROVED to OBSERVED should fail
    with pytest.raises(DeliverableStateViolation):
        d.transition_to(DeliverableStatus.OBSERVED)

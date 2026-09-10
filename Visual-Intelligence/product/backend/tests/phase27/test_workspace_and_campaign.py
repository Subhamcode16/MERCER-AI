"""
Tests for Phase 27 Workspace Store and Campaign Lifecycle Management.
"""
import pytest
from src.campaign_studio.workspace import WorkspaceStore
from src.campaign_studio.campaign_workspace import (
    CampaignWorkspaceManager,
    StudioCampaignStatus,
)


def test_workspace_client_brand_product_hierarchy():
    store = WorkspaceStore()
    client = store.create_client("cli_lux_01", "Maison Vanguard", "Haute Couture")
    assert client.client_id == "cli_lux_01"
    assert client.name == "Maison Vanguard"

    brand = store.create_brand("brd_01", "cli_lux_01", "Vanguard Atelier", "Quiet Architectural Luxury")
    assert brand.brand_id == "brd_01"
    assert brand.client_id == "cli_lux_01"

    product = store.create_product("prd_01", "brd_01", "Monolith Wool Overcoat", "Outerwear", ["#1A1A1A", "#E5E0D8"])
    assert product.product_id == "prd_01"
    assert "Monolith Wool Overcoat" == product.name

    clients = store.list_clients()
    assert len(clients) == 1
    brands = store.list_brands("cli_lux_01")
    assert len(brands) == 1
    products = store.list_products("brd_01")
    assert len(products) == 1


def test_campaign_creation_and_optimistic_locking_transitions():
    mgr = CampaignWorkspaceManager()
    camp = mgr.create_campaign(
        campaign_id="camp_aw26_01",
        client_id="cli_lux_01",
        brand_id="brd_01",
        title="Autumn/Winter 2026 Campaign",
        created_by="op_cd_01",
    )
    assert camp.status == StudioCampaignStatus.INTAKE_DISCOVERY
    assert camp.version == 1

    # Valid transition with correct version
    camp2 = mgr.transition_status(
        campaign_id="camp_aw26_01",
        target_status=StudioCampaignStatus.CREATIVE_INTELLIGENCE,
        operator_id="op_cd_01",
        expected_version=1,
    )
    assert camp2.status == StudioCampaignStatus.CREATIVE_INTELLIGENCE
    assert camp2.version == 2

    # Stale version transition must raise RuntimeError (optimistic lock rejection)
    with pytest.raises(RuntimeError) as exc_info:
        mgr.transition_status(
            campaign_id="camp_aw26_01",
            target_status=StudioCampaignStatus.DIRECTION_PROPOSALS,
            operator_id="op_cd_01",
            expected_version=1,  # Stale!
        )
    assert "Optimistic locking conflict" in str(exc_info.value)

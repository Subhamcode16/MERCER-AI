"""
Unit tests for Phase 15 Client Operations Manager.
"""

import pytest
from src.studio_operations.client_operations import ClientOperationsManager
from src.studio_operations.exceptions import ClientContextViolation

def test_client_operations_lifecycle():
    mgr = ClientOperationsManager()
    client = mgr.create_client("client_a", "Client Alpha", "Fashion")
    assert client.client_id == "client_a"

    brand = mgr.bind_brand("brand_a", "client_a", "Alpha Wear")
    assert brand.brand_id == "brand_a"

    # Cross-client isolation check
    with pytest.raises(ClientContextViolation):
        mgr.get_client("client_b", "client_a")

    summary = mgr.get_client_summary("client_a")
    assert summary["name"] == "Client Alpha"
    assert "Alpha Wear" in summary["brands"]

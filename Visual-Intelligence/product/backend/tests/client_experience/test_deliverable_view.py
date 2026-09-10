"""
Unit tests for Phase 16 Deliverable Review Surface.
"""

import pytest
from src.client_experience.deliverable_view import DeliverableReviewSurface
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_deliverable_view_projections(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "deliv_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    orch.bind_client_brand("client_nocap", "brand_nocap", "NOCAP")
    orch.launch_campaign("client_nocap", "camp_001", "brand_nocap", "Fall Drop", "Awareness")
    d1 = orch.deliverable_manager.create_deliverable("client_nocap", "del_001", "ws_001", "camp_001", "client_nocap", "Hero Post")

    surface = DeliverableReviewSurface()
    user = UserIdentity("user_a", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    dto = surface.get_deliverable(user, orch, "del_001")
    assert dto.deliverable_id == "del_001"
    assert dto.title == "Hero Post"
    assert dto.status == "PLANNED"

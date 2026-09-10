"""
Unit tests for Phase 16 Client Dashboard Projection Engine.
"""

import pytest
from src.client_experience.dashboard import ClientDashboardProjectionEngine
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_dashboard_projection(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "dash_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")

    engine = ClientDashboardProjectionEngine()
    user = UserIdentity("user_a", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    dto = engine.get_dashboard(user, orch)
    assert dto.client_id == "client_nocap"
    assert dto.name == "NOCAP Studio"
    assert dto.active_campaigns_count == 0

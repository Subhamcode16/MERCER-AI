"""
Unit tests for Phase 16 Performance & Outcome View.
"""

import pytest
from src.client_experience.performance_view import PerformanceOutcomeView
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_performance_view_summary(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "perf_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")

    view = PerformanceOutcomeView()
    user = UserIdentity("user_owner", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    summary = view.get_performance_summary(user, orch)
    assert summary.client_id == "client_nocap"
    assert summary.total_deliverables == 0

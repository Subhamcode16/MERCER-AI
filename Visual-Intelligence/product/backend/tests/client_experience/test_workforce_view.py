"""
Unit tests for Phase 16 Workforce Activity View.
"""

import pytest
from src.client_experience.workforce_view import WorkforceActivityView
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_workforce_activity_view(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "wf_ledger"))
    view = WorkforceActivityView()
    user = UserIdentity("user_op", "Operator", "op@studio.com", "client_nocap", HumanRole.STUDIO_OPERATOR)

    list_wf = view.list_workforce_activity(user, orch)
    assert len(list_wf) > 0
    assert list_wf[0].staff_id is not None

"""
Unit tests for Phase 16 Operations Timeline Engine.
"""

import pytest
from src.client_experience.timeline import OperationsTimelineEngine
from src.client_experience.access_models import UserIdentity, HumanRole
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_timeline_engine_projection(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "time_ledger"))
    orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")

    engine = OperationsTimelineEngine()
    user = UserIdentity("user_owner", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)

    timeline = engine.get_timeline(user, orch)
    assert len(timeline) == 1
    assert timeline[0].event_type == "CLIENT_REGISTERED"

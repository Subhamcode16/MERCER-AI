"""
Unit tests for Phase 17 Bounded Autonomy Controller.
"""

import pytest
from src.production_fabric.autonomy_controller import BoundedAutonomyController
from src.production_fabric.exceptions import ContinuationBoundaryError

def test_autonomy_controller_tiers():
    ctrl = BoundedAutonomyController()
    ctrl.set_tier("client_a", 1)
    assert ctrl.get_tier("client_a") == 1

    # Tier 1 cannot execute without authorization
    with pytest.raises(ContinuationBoundaryError):
        ctrl.verify_action_permitted("client_a", "EXECUTE_POST", requires_human_auth=True)

    with pytest.raises(ContinuationBoundaryError):
        ctrl.set_tier("client_a", 5)  # Invalid tier

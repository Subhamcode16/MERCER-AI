"""
Phase 14 Test Workforce Delegation
-----------------------------------
Tests WorkforceDelegationEngine objective decomposition and dependency DAG formulation.
"""

import pytest
from src.creative_workforce import WorkforceDelegationEngine, InvalidWorkforceRequestError

def test_delegation_decomposition():
    engine = WorkforceDelegationEngine()
    assignments = engine.decompose_objective(
        client_id="nocap",
        brand_id="nocap-apparel",
        campaign_id="cmp-sept",
        mission_id="m-1",
        objective="Create September campaign",
    )
    assert len(assignments) == 7
    assert assignments[0].context_binding.client_id == "nocap"

def test_empty_objective_rejection():
    engine = WorkforceDelegationEngine()
    with pytest.raises(InvalidWorkforceRequestError):
        engine.decompose_objective("nocap", "brand", "cmp", "m", "")

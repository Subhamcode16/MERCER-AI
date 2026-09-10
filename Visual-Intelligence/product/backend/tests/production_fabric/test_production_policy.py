"""
Unit tests for Phase 17 Production Policy Engine.
"""

import pytest
from src.production_fabric.production_policy import ProductionPolicyEngine
from src.production_fabric.exceptions import FabricPolicyViolation

def test_production_policy_validation():
    engine = ProductionPolicyEngine()

    # Valid adaptable strategy
    assert engine.validate_policy_mutation("task_ordering", ["w2", "w1"]) is True

    # Immutable security policy mutation MUST fail
    with pytest.raises(FabricPolicyViolation):
        engine.validate_policy_mutation("authorization_origin", "autonomous_model")

    with pytest.raises(FabricPolicyViolation):
        engine.validate_policy_mutation("capability_allowlists", ["bypass_auth"])

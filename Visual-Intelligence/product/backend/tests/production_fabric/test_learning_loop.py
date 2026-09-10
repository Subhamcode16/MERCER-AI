"""
Unit tests for Phase 17 Production Learning Loop.
"""

import pytest
from src.production_fabric.learning_loop import ProductionLearningLoop
from src.production_fabric.production_models import ProductionOutcome
from src.production_fabric.exceptions import FabricPolicyViolation

def test_learning_loop_candidate_generation():
    loop = ProductionLearningLoop()
    outcome = ProductionOutcome("o1", "client_a", "c1", "d1", "ig", "p1", 1000, 0.05)

    sig = loop.process_outcome_learning(outcome, "prompt_templates", "v2_template")
    assert sig["status"] == "CANDIDATE"

    with pytest.raises(FabricPolicyViolation):
        loop.process_outcome_learning(outcome, "security_policy", "permissive")

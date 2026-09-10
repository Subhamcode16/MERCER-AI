"""
Phase 14 Test Governed Self-Improvement
---------------------------------------
Tests GovernedImprovementEngine controlled experimentation, degradation rejection, and rollback (INV-14-W007).
"""

import pytest
from src.creative_workforce import (
    GovernedImprovementEngine,
    UntrustedObservationInjectionError,
)

def test_benchmark_adoption_and_degradation_rejection():
    engine = GovernedImprovementEngine()
    engine.propose_candidate_strategy("v1.1", {"critique_threshold": 0.85})

    # Benchmark superior candidate score (0.90 >= 0.80) -> Adopted
    res_good = engine.benchmark_candidate("v1.1", 0.90)
    assert res_good.is_adopted is True
    assert engine.get_active_strategy().version == "v1.1"

    # Benchmark degraded candidate score (0.60 < baseline) -> Rejected
    engine.propose_candidate_strategy("v1.2", {"critique_threshold": 0.50})
    res_bad = engine.benchmark_candidate("v1.2", 0.60)
    assert res_bad.is_adopted is False
    assert res_bad.rejection_reason is not None

def test_strategy_security_mutation_rejection():
    engine = GovernedImprovementEngine()
    with pytest.raises(UntrustedObservationInjectionError):
        engine.propose_candidate_strategy("v2.0", {"disable_security_check": True})

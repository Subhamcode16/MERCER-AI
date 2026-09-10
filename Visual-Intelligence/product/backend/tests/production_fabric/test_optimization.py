"""
Unit tests for Phase 17 Production Optimization Engine.
"""

from src.production_fabric.optimization import ProductionOptimizationEngine

def test_optimization_baseline_comparison():
    opt = ProductionOptimizationEngine()
    opt.set_baseline("client_a", "engagement_rate", 0.05)

    # Higher engagement adopted
    success = opt.evaluate_and_adopt("client_a", "engagement_rate", 0.08, "prompt_template", {"v": 2})
    assert success is True

    # Lower engagement rejected and rolled back
    success_degraded = opt.evaluate_and_adopt("client_a", "engagement_rate", 0.02, "prompt_template", {"v": 3})
    assert success_degraded is False

"""
Tests for ImprovementManager reversibility.
"""

from src.agentic_work import ImprovementManager, AdaptiveChange, AdaptiveStatus


def test_improvement_reversibility():
    mgr = ImprovementManager()
    change = AdaptiveChange(
        change_id="chg-01",
        target_component="PROMPT_TEMPLATE",
        previous_version="v1",
        proposed_version="v2",
        reason="Improvement",
        supporting_signals=["sig-1"],
        status=AdaptiveStatus.ACTIVE,
    )
    mgr.register_change(change)

    reverted = mgr.revert_last_change()
    assert reverted is not None
    assert reverted.status == AdaptiveStatus.ROLLED_BACK

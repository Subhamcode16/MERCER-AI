"""
Tests for Phase 19 exceptions hierarchy.
"""

import pytest
from src.creative_intelligence.exceptions import (
    CreativeIntelligenceError,
    ClientDataLeakageError,
    AuthorityEscalationError,
    ImmutablePolicyViolationError,
    LineageBrokenError,
    StaleIntelligenceError,
    UnvalidatedStrategyError,
    UnsafeGeneralizationError
)


def test_exception_hierarchy():
    """Verify all custom exceptions inherit from CreativeIntelligenceError."""
    exceptions = [
        ClientDataLeakageError("leak"),
        AuthorityEscalationError("escalate"),
        ImmutablePolicyViolationError("policy"),
        LineageBrokenError("lineage"),
        StaleIntelligenceError("stale"),
        UnvalidatedStrategyError("unvalidated"),
        UnsafeGeneralizationError("unsafe")
    ]

    for exc in exceptions:
        assert isinstance(exc, CreativeIntelligenceError)

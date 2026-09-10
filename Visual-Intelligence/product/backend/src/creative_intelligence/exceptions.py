"""
Phase 19 - Creative Intelligence Network Exceptions.

Defines all custom exceptions for institutional learning, knowledge provenance,
pattern generalization, workforce evolution recommendations, and strategy registry.
"""


class CreativeIntelligenceError(Exception):
    """Base exception for all Phase 19 Creative Intelligence errors."""
    pass


class ClientDataLeakageError(CreativeIntelligenceError):
    """Raised when cross-client pattern generalization detects un-scrubbed client-confidential data."""
    pass


class AuthorityEscalationError(CreativeIntelligenceError):
    """Raised when institutional intelligence attempts to execute actions or bypass authorization policy."""
    pass


class ImmutablePolicyViolationError(CreativeIntelligenceError):
    """Raised when institutional intelligence or workforce evolution attempts to mutate security policy."""
    pass


class LineageBrokenError(CreativeIntelligenceError):
    """Raised when knowledge graph or strategy provenance hash chain validation fails."""
    pass


class StaleIntelligenceError(CreativeIntelligenceError):
    """Raised when strategy or pattern has decayed past staleness threshold and must be retired."""
    pass


class UnvalidatedStrategyError(CreativeIntelligenceError):
    """Raised when attempting to deploy or register an unvalidated strategy."""
    pass


class UnsafeGeneralizationError(CreativeIntelligenceError):
    """Raised when a pattern generalization fails empirical validation or anonymization bounds."""
    pass

"""
Phase 18 Domain Exceptions: Real-World Provider Operations & Closed-Loop Studio Intelligence.

All exceptions fail closed and preserve security/isolation invariants.
"""

class StudioIntelligenceError(Exception):
    """Base exception for all Phase 18 Studio Intelligence failures."""
    pass


class OutcomeValidationError(StudioIntelligenceError):
    """Raised when external outcome schema, provenance, or timestamps are invalid."""
    pass


class AttributionError(StudioIntelligenceError):
    """Raised when outcome attribution lineage or artifact linkage fails."""
    pass


class EvaluationError(StudioIntelligenceError):
    """Raised when creative performance scoring fails or metrics are corrupted."""
    pass


class ProviderRuntimeError(StudioIntelligenceError):
    """Raised when provider runtime execution, capability checks, or sandboxes fail."""
    pass


class LearningBoundaryViolation(StudioIntelligenceError):
    """Raised when learning signals attempt to mutate security policy or escalate authority."""
    pass


class OptimizationRejectedError(StudioIntelligenceError):
    """Raised when a candidate strategy demonstrates degraded performance or fails benchmarks."""
    pass


class CrossClientIntelligenceViolation(StudioIntelligenceError):
    """Raised when cross-client intelligence, memory, or learning access is attempted."""
    pass


class ExperimentRaceError(StudioIntelligenceError):
    """Raised when concurrent experiments conflict or race on strategy parameters."""
    pass


class IntelligenceLedgerError(StudioIntelligenceError):
    """Raised when audit ledger hash-integrity or sequence validation fails."""
    pass

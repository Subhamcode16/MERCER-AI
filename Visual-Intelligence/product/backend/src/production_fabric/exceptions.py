"""
Phase 17 Production Fabric Fail-Closed Domain Exceptions.
Establishes explicit error types for production intake, workflow continuation, boundary violations,
approval orchestration, outcome loops, and recovery operations.
"""

class ProductionFabricError(Exception):
    """Base exception for all Phase 17 Production Fabric errors."""
    pass

class WorkIntakeError(ProductionFabricError):
    """Raised when work intake validation fails or client context is ambiguous."""
    pass

class ProductionStateViolation(ProductionFabricError):
    """Raised when an invalid production state transition is attempted."""
    pass

class ApprovalOrchestrationError(ProductionFabricError):
    """Raised when approval packaging, scope binding, or routing fails."""
    pass

class ContinuationBoundaryError(ProductionFabricError):
    """Raised when autonomous continuation attempts to exceed policy or authorization boundaries."""
    pass

class OutcomeObservationError(ProductionFabricError):
    """Raised when an external outcome record fails provenance or commitment validation."""
    pass

class OperationalRecoveryError(ProductionFabricError):
    """Raised when recovery procedures encounter corrupted state or unauthorized execution requests."""
    pass

class FabricPolicyViolation(ProductionFabricError):
    """Raised when operational actions violate production policy restrictions."""
    pass

class CrossClientFabricViolation(ProductionFabricError):
    """Raised when a production worker or runtime attempts cross-tenant context access."""
    pass

class StaleProductionStateError(ProductionFabricError):
    """Raised when an operation is requested on a stale production run or expired checkpoint."""
    pass

class ProductionReplayError(ProductionFabricError):
    """Raised when duplicate production execution or replayed payloads are detected."""
    pass

class FabricInvariantViolation(ProductionFabricError):
    """Raised when a non-negotiable Phase 17 invariant (INV-17-001 to INV-17-010) is violated."""
    pass

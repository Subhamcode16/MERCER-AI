"""
Phase 23 Production Runtime Exceptions.
"""

class ProductionRuntimeError(Exception):
    """Base exception for all production runtime errors."""
    pass

class RuntimeStartupError(ProductionRuntimeError):
    """Raised when runtime startup sequence fails dependency checks or validation."""
    pass

class WorkerLimitExceededError(ProductionRuntimeError):
    """Raised when tenant or global worker concurrency limit is exceeded."""
    pass

class QueueCapacityError(ProductionRuntimeError):
    """Raised when task queue capacity limit is reached."""
    pass

class ProcessCrashError(ProductionRuntimeError):
    """Raised when a managed worker process crashes or terminates unexpectedly."""
    pass

class InvalidStateTransitionError(ProductionRuntimeError):
    """Raised when an illegal state machine transition is attempted."""
    pass

class DependencyUnhealthyError(ProductionRuntimeError):
    """Raised when a critical dependency fails its health probe."""
    pass

class GracefulShutdownTimeout(ProductionRuntimeError):
    """Raised when graceful shutdown exceeds bounded deadline."""
    pass

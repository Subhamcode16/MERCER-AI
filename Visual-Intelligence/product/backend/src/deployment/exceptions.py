"""
Phase 23 Deployment & Environment Management Exceptions.
"""

class DeploymentError(Exception):
    """Base exception for deployment errors."""
    pass

class DeploymentGateError(DeploymentError):
    """Raised when release validation fails any required release gate."""
    pass

class CanaryDegradedError(DeploymentError):
    """Raised when canary stage metrics breach error rate or latency SLA thresholds."""
    pass

class RollbackFailedError(DeploymentError):
    """Raised when automated rollback procedure encounters an error."""
    pass

class ManifestMismatchError(DeploymentError):
    """Raised when artifact manifest hash or dependencies do not match signed lockfile."""
    pass

class UnauthorizedPromotionError(DeploymentError):
    """Raised when environment promotion lacks human approval or valid evidence."""
    pass

"""
Phase 24 Live Operations & Provider Validation Exceptions.
"""

class LiveOperationsError(Exception):
    """Base exception for all live operations errors."""
    pass

class ProviderConnectivityError(LiveOperationsError):
    """Raised when external provider connectivity fails or times out."""
    pass

class ProbeExecutionError(LiveOperationsError):
    """Raised when a live validation probe encounters an unhandled execution failure."""
    pass

class EvidenceTamperingError(LiveOperationsError):
    """Raised when a cryptographic evidence receipt or ledger entry fails hash verification."""
    pass

class IsolationLeakageError(LiveOperationsError):
    """Raised when cross-tenant context, visual reference, or resource leakage is detected."""
    pass

class UnauthorizedLiveMutationError(LiveOperationsError):
    """Raised when an external mutation is attempted without valid human authorization."""
    pass

class ProviderUnavailableError(LiveOperationsError):
    """Raised when provider credentials or endpoints are unconfigured."""
    pass

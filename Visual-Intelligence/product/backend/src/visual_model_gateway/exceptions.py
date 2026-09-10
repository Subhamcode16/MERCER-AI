"""
Phase 20 - Visual Model Gateway Exceptions.

Defines custom exception hierarchy for image generation and vision model operations.
"""


class VisualGatewayError(Exception):
    """Base exception for all Phase 20 Visual Model Gateway errors."""
    pass


class VisualModelNotFoundError(VisualGatewayError):
    """Raised when requested visual or image model is not found in registry."""
    pass


class VisualPolicyViolationError(VisualGatewayError):
    """Raised when an image generation or vision request violates visual policy."""
    pass


class ArtifactValidationFailedError(VisualGatewayError):
    """Raised when generated image artifact fails aspect ratio or resolution validation."""
    pass


class VisualLineageCorruptedError(VisualGatewayError):
    """Raised when artifact lineage hash or reference link is corrupted."""
    pass

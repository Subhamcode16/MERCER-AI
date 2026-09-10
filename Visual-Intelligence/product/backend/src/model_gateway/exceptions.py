"""
Phase 20 - Model Gateway Exceptions.

Defines custom exception hierarchy for LLM provider gateway operations.
"""


class ModelGatewayError(Exception):
    """Base exception for all Phase 20 Model Gateway errors."""
    pass


class ModelNotFoundError(ModelGatewayError):
    """Raised when an requested model or provider is not registered or supported."""
    pass


class ModelPolicyViolationError(ModelGatewayError):
    """Raised when a model request violates capability, context, or governance policies."""
    pass


class TokenBudgetExceededError(ModelGatewayError):
    """Raised when a request exceeds max token budget constraints."""
    pass


class ModelTimeoutError(ModelGatewayError):
    """Raised when a model provider request times out."""
    pass


class ModelProviderError(ModelGatewayError):
    """Raised when an external model provider returns an unrecoverable error."""
    pass


class StructuredOutputValidationError(ModelGatewayError):
    """Raised when model response fails JSON/schema validation."""
    pass


class CredentialLeakageError(ModelGatewayError):
    """Raised when sensitive API keys or credentials are detected in prompt context or output."""
    pass

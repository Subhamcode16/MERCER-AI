"""
Phase 14 Workflow Gateway Exceptions
-----------------------------------
Fail-closed exception hierarchy governing user workflow control plane operations.
"""

class WorkflowGatewayError(Exception):
    """Base exception for all workflow gateway errors."""
    pass

class WorkflowNotFoundError(WorkflowGatewayError):
    """Raised when a workflow ID cannot be found."""
    pass

class InvalidWorkflowRequestError(WorkflowGatewayError):
    """Raised when workflow creation parameters or objectives violate constraints."""
    pass

class WorkflowStateError(WorkflowGatewayError):
    """Raised when an illegal workflow state transition is attempted."""
    pass

class AuthorizationRequiredError(WorkflowGatewayError):
    """Raised when an external action is attempted without valid Phase 10 authorization."""
    pass

class CrossMissionLeakageError(WorkflowGatewayError):
    """Raised when authorization, resources, or artifacts from one mission are used in another."""
    pass

class SecretExposureError(WorkflowGatewayError):
    """Raised if provider secrets or private key material enter workflow projections or events."""
    pass

class ArtifactLineageError(WorkflowGatewayError):
    """Raised when artifact lineage verification fails or is tampered with."""
    pass

class FeedbackIngestionError(WorkflowGatewayError):
    """Raised when feedback submission is invalid or attempts policy mutation."""
    pass

"""
Phase 20 - MCP Gateway Schemas & Data Models.

Defines typed Pydantic models for MCP server manifests, tool capabilities,
invocation requests, sanitized tool results, and rate limit rules.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional, Set
from pydantic import BaseModel, Field


class MCPServerRegistration(BaseModel):
    """Manifest registration of an external MCP server."""
    server_id: str
    provider: str
    environment: str = "SANDBOX"  # "SANDBOX", "PRODUCTION"
    declared_capabilities: List[str]
    approved_capabilities: List[str]
    risk_class: str = "LOW"  # "LOW", "MEDIUM", "HIGH"
    credential_requirements: List[str] = Field(default_factory=list)
    data_scopes: List[str] = Field(default_factory=list)
    rate_limit_per_min: int = 60
    timeout_seconds: float = 10.0
    requires_human_approval: bool = False
    enabled: bool = True
    transport_url: Optional[str] = None


class MCPToolManifest(BaseModel):
    """Manifest structure for an individual MCP tool."""
    tool_name: str
    server_id: str
    description: str
    parameters_schema: Dict[str, Any]
    required_capability: str
    is_mutation: bool = False


class MCPInvocationRequest(BaseModel):
    """Request payload to invoke an MCP tool."""
    request_id: str = Field(default_factory=lambda: f"mcpreq_{uuid.uuid4().hex[:12]}")
    server_id: str
    tool_name: str
    arguments: Dict[str, Any]
    client_id: Optional[str] = None
    idempotency_key: str = Field(default_factory=lambda: f"ik_{uuid.uuid4().hex[:12]}")
    created_at: float = Field(default_factory=time.time)


class MCPInvocationResult(BaseModel):
    """Result payload returned from an MCP tool invocation."""
    invocation_id: str = Field(default_factory=lambda: f"mcpres_{uuid.uuid4().hex[:12]}")
    request_id: str
    server_id: str
    tool_name: str
    success: bool
    sanitized_output: Dict[str, Any]
    trust_classification: str = "UNTRUSTED_EXTERNAL_OBSERVATION"  # ALWAYS UNTRUSTED
    latency_ms: float = 0.0
    error_message: Optional[str] = None
    created_at: float = Field(default_factory=time.time)

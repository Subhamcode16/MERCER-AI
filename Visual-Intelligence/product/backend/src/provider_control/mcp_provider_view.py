"""
Phase 25 Model Context Protocol (MCP) Tool Registry and Capability Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class MCPToolCapabilityView:
    server_id: str
    server_name: str
    tool_name: str
    declared_capabilities: List[str]
    wildcard_permitted: bool = False # Always False per Phase 24/25 invariant
    risk_level: str = "LOW"
    denied_calls_count: int = 0
    total_invocations: int = 0
    status: str = "ACTIVE"

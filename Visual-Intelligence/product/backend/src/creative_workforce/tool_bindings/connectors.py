"""
Phase 26 Tool & Connector Capability Bindings.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from src.creative_workforce.worker_identity.models import WorkerIdentity
from src.creative_workforce.capability_binding.manifest import CapabilityResolver


class ToolAccessError(Exception):
    pass


@dataclass
class ToolDefinition:
    tool_id: str
    name: str
    description: str
    required_capability: str
    risk_level: str = "READ_ONLY"  # READ_ONLY, MUTATING, EXTERNAL_INTEGRATION


class ToolBindingManager:
    """Manages connector/tool access with explicit per-worker capability validation."""

    def __init__(self, capability_resolver: CapabilityResolver):
        self.capability_resolver = capability_resolver
        self._tools: Dict[str, ToolDefinition] = {}

    def register_tool(self, tool: ToolDefinition) -> ToolDefinition:
        self._tools[tool.tool_id] = tool
        return tool

    def get_tool(self, tool_id: str) -> Optional[ToolDefinition]:
        return self._tools.get(tool_id)

    def invoke_tool(
        self,
        tool_id: str,
        worker: WorkerIdentity,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        tool = self._tools.get(tool_id)
        if not tool:
            raise ToolAccessError(f"Tool '{tool_id}' not found in registry")

        # Check required capability on worker
        if not self.capability_resolver.has_capability(worker.worker_id, tool.required_capability):
            raise ToolAccessError(
                f"Worker '{worker.worker_id}' lacks capability '{tool.required_capability}' required for tool '{tool_id}'"
            )

        return {
            "tool_id": tool_id,
            "status": "SUCCESS",
            "worker_id": worker.worker_id,
            "result": f"Executed tool {tool.name} with params: {list(params.keys())}",
        }

"""
Governed Tool Registry for Agent Runtime.
Wraps tools in policy checks, audit logging, and epistemic output validation.
"""

from typing import Dict, List, Any, Callable
from src.agent_runtime.interfaces.agent_runtime import ToolRegistration, WorkerDefinition, AgentSession
from src.agent_runtime.policy.runtime_policy import RuntimePolicyValidator
from src.agent_runtime.errors.exceptions import UnauthorizedToolError


class GovernedToolRegistry:
    """Central registry of policy-governed tools accessible to Agent Runtime."""

    def __init__(self):
        self._tools: Dict[str, ToolRegistration] = {}
        self._handlers: Dict[str, Callable] = {}
        self._audit_log: List[Dict[str, Any]] = []

        # Register default governed tools
        self._register_default_tools()

    def register_tool(self, registration: ToolRegistration, handler: Callable):
        """Register a new tool and its underlying handler."""
        self._tools[registration.tool_id] = registration
        self._handlers[registration.tool_id] = handler

    def get_tool(self, tool_id: str) -> ToolRegistration:
        """Lookup tool definition."""
        if tool_id not in self._tools:
            raise UnauthorizedToolError(tool_id=tool_id, role="unknown", required_authority="registered")
        return self._tools[tool_id]

    def list_tools_for_worker(self, worker: WorkerDefinition) -> List[ToolRegistration]:
        """Filter tools permitted for the worker's role, tenant, and bindings."""
        permitted = []
        for tool in self._tools.values():
            try:
                RuntimePolicyValidator.validate_tool_access(worker, tool)
                permitted.append(tool)
            except Exception:
                continue
        return permitted

    async def execute_tool(
        self,
        session: AgentSession,
        worker: WorkerDefinition,
        tool_id: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute tool behind strict policy validation, error trapping, and audit logging."""
        tool = self.get_tool(tool_id)
        
        # 1. Enforce Tenant Boundary & Role Access
        RuntimePolicyValidator.validate_tenant_boundary(session, session.tenant_id)
        RuntimePolicyValidator.validate_tool_access(worker, tool)

        # 2. Invoke Handler
        handler = self._handlers[tool_id]
        raw_result = await handler(session=session, worker=worker, **arguments)

        # 3. Sanitize & Enforce Epistemic Status
        validated_result = RuntimePolicyValidator.validate_tool_output(tool_id, raw_result)

        # 4. Record Audit Log Entry
        audit_entry = {
            "session_id": session.session_id,
            "tenant_id": session.tenant_id,
            "worker_id": worker.worker_id,
            "tool_id": tool_id,
            "arguments": arguments,
            "status": "SUCCESS",
            "epistemic_status": validated_result.get("epistemic_status", "INFERRED")
        }
        self._audit_log.append(audit_entry)

        return validated_result

    def _register_default_tools(self):
        """Register initial vertical slice tools."""
        
        # Tool 1: research.search (Intelligence Worker)
        research_tool = ToolRegistration(
            tool_id="research.search",
            name="Research & Trend Discovery",
            description="Searches curated fashion intelligence, audience demographics, and textile benchmarks.",
            tenant_scope="global",
            allowed_roles=["intelligence_specialist", "creative_director", "researcher"],
            required_authority="read_only",
            read_write="read",
            data_classification="confidential",
            approval_required=False,
            evidence_requirement="grounded_citation",
            audit_requirement=True,
            parameters_schema={
                "query": {"type": "string", "description": "Search query for fashion trends or audience data"}
            }
        )

        async def research_search_handler(session: AgentSession, worker: WorkerDefinition, query: str = "", **kwargs):
            # Grounded knowledge search simulation
            q = query.lower()
            if "bridal" in q or "banarasi" in q or "heritage" in q:
                return {
                    "query": query,
                    "findings": [
                        {
                            "topic": "Gen Z Luxury Bridal Preferences",
                            "insight": "Modernized heritage silhouettes show +24.2% engagement lift over traditional ceremonial framing.",
                            "source": "Audience Intelligence Cohort 2026",
                            "confidence": 0.94,
                            "epistemic_status": "OBSERVED"
                        },
                        {
                            "topic": "Textile Drape Physics",
                            "insight": "Banarasi gold brocade requires tungsten warm edge lighting (2800K) to avoid optical glare.",
                            "source": "Textile Physics Calibration DB",
                            "confidence": 0.98,
                            "epistemic_status": "SUPPORTED"
                        }
                    ],
                    "epistemic_status": "OBSERVED",
                    "source_type": "curated_intelligence"
                }
            return {
                "query": query,
                "findings": [
                    {
                        "topic": "General Fashion Market Signal",
                        "insight": "Minimalist architectural tailoring continues to lead high-end luxury outerwear.",
                        "source": "Global Market Observatory",
                        "confidence": 0.88,
                        "epistemic_status": "INFERRED"
                    }
                ],
                "epistemic_status": "INFERRED",
                "source_type": "market_index"
            }

        self.register_tool(research_tool, research_search_handler)

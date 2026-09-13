"""
Provider-neutral Agent Runtime Interfaces.
Defines execution contracts decoupled from specific LLM or Agent providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, AsyncIterator
from pydantic import BaseModel, Field
import time


class ToolRegistration(BaseModel):
    tool_id: str
    name: str
    description: str
    tenant_scope: str = "global"
    allowed_roles: List[str] = Field(default_factory=lambda: ["intelligence_specialist", "creative_director"])
    required_authority: str = "read_only"
    read_write: str = "read"
    data_classification: str = "confidential"
    approval_required: bool = False
    evidence_requirement: str = "grounded_citation"
    audit_requirement: bool = True
    parameters_schema: Dict[str, Any] = Field(default_factory=dict)


class WorkerDefinition(BaseModel):
    worker_id: str
    name: str
    role: str
    skills: List[str] = Field(default_factory=list)
    memory_scope: str = "tenant_local"
    tenant_scope: str
    campaign_scope: Optional[str] = None
    tool_bindings: List[str] = Field(default_factory=list)
    authority_scope: str = "advisor"


class RuntimeEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt-{int(time.time()*1000)}")
    event_type: str
    session_id: str
    worker_id: str
    timestamp: float = Field(default_factory=time.time)
    payload: Dict[str, Any] = Field(default_factory=dict)


class AgentSession(BaseModel):
    session_id: str
    tenant_id: str
    worker_id: str
    created_at: float = Field(default_factory=time.time)
    is_active: bool = True
    context_tokens: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentRuntime(ABC):
    """Provider-neutral runtime interface."""

    @abstractmethod
    async def create_session(self, tenant_id: str, worker: WorkerDefinition, initial_context: Dict[str, Any]) -> AgentSession:
        """Create a new isolated runtime session."""
        pass

    @abstractmethod
    async def resume_session(self, session_id: str, tenant_id: str) -> AgentSession:
        """Resume an active session with cryptographic tenant verification."""
        pass

    @abstractmethod
    async def run(self, session: AgentSession, prompt: str, tools: List[ToolRegistration]) -> Dict[str, Any]:
        """Execute a prompt turn within the session."""
        pass

    @abstractmethod
    async def stream(self, session: AgentSession, prompt: str, tools: List[ToolRegistration]) -> AsyncIterator[RuntimeEvent]:
        """Stream execution events and tokens."""
        pass

    @abstractmethod
    async def delegate(self, parent_session: AgentSession, target_worker: WorkerDefinition, delegation_prompt: str) -> Dict[str, Any]:
        """Delegate a subtask to a specialist worker."""
        pass

    @abstractmethod
    async def stop(self, session_id: str) -> bool:
        """Gracefully stop execution."""
        pass

    @abstractmethod
    async def recover(self, session_id: str, safe_state: Dict[str, Any]) -> AgentSession:
        """Recover a failed session safely without authority escalation."""
        pass

    @abstractmethod
    async def close(self, session_id: str) -> bool:
        """Close and revoke the session."""
        pass

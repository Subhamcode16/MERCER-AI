"""
IF-AGENT-002 Hierarchical Context Scoping & Boundary Isolation.
Provides scoped context propagation across system, workflow, task, staff, review, and learning.
Prevents unrestricted memory leaks and global state mutation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .models import StaffRole


@dataclass
class SystemContext:
    """
    Top-level system configuration context (read-only for workers).
    """
    system_id: str
    environment: str = "PRODUCTION"
    policy_version: str = "8.0.0"
    max_workflow_latency_seconds: float = 300.0


@dataclass
class WorkflowContext:
    """
    Scoped context for a specific user workflow run.
    """
    workflow_id: str
    system_id: str
    user_id: str
    objective: str
    correlation_id: str
    created_at: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    brand_guidelines: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskContext:
    """
    Task-level context provided specifically to a worker task node.
    """
    task_id: str
    workflow_id: str
    role: StaffRole
    objective: str
    inputs: Dict[str, Any]
    parent_outputs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StaffContext:
    """
    Worker execution environment context.
    Strictly isolated per staff task execution.
    """
    staff_id: str
    role: StaffRole
    task_context: TaskContext
    allowed_tools: List[str]
    max_tokens: int = 4096


@dataclass
class ReviewContext:
    """
    Evaluation context provided to CRITIC and REVIEWER workers.
    """
    review_id: str
    workflow_id: str
    target_task_id: str
    artifact_data: Dict[str, Any]
    quality_criteria: Dict[str, Any]
    revision_iteration: int = 1

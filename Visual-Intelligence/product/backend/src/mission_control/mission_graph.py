"""
Phase 11 Mission Graph (Bounded DAG).

Constructs and validates directed acyclic graphs (DAGs) of workflows and tasks.
Enforces cycle detection, depth limits, task count bounds, dependency validation,
and deterministic topological ordering.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple

from .exceptions import InvalidMissionGraphError


@dataclass
class MissionTaskNode:
    """Node representing a discrete task within a mission graph."""
    task_id: str
    workflow_id: str
    assigned_role: str  # e.g., RESEARCHER, STRATEGIST, DESIGNER, etc.
    description: str
    dependencies: List[str] = field(default_factory=list)
    required_capabilities: Set[str] = field(default_factory=set)
    resource_targets: Set[str] = field(default_factory=set)
    estimated_tokens: int = 5000
    status: str = "PENDING"  # PENDING, READY, RUNNING, COMPLETED, FAILED, BLOCKED

    def __post_init__(self):
        if not self.task_id or not isinstance(self.task_id, str):
            raise InvalidMissionGraphError("task_id must be a non-empty string.")
        if not self.workflow_id or not isinstance(self.workflow_id, str):
            raise InvalidMissionGraphError("workflow_id must be a non-empty string.")
        if "*" in self.required_capabilities or "ALL" in self.required_capabilities:
            raise InvalidMissionGraphError("Wildcard capabilities in task node are prohibited.")


class MissionGraph:
    """Bounded Directed Acyclic Graph for mission orchestration."""

    def __init__(self, max_depth: int = 10, max_tasks: int = 50):
        self.max_depth = max_depth
        self.max_tasks = max_tasks
        self.nodes: Dict[str, MissionTaskNode] = {}
        self.adj_list: Dict[str, List[str]] = {}  # parent -> children
        self.in_degree: Dict[str, int] = {}       # task_id -> count of dependencies

    def add_task(self, node: MissionTaskNode) -> None:
        """Adds a task node to the graph and validates bounds and dependencies."""
        if node.task_id in self.nodes:
            raise InvalidMissionGraphError(f"Duplicate task_id '{node.task_id}' in graph.")

        if len(self.nodes) + 1 > self.max_tasks:
            raise InvalidMissionGraphError(
                f"Task count limit exceeded. Maximum allowed tasks: {self.max_tasks}."
            )

        self.nodes[node.task_id] = node
        self.in_degree[node.task_id] = 0
        if node.task_id not in self.adj_list:
            self.adj_list[node.task_id] = []

        for dep_id in node.dependencies:
            if dep_id not in self.nodes:
                raise InvalidMissionGraphError(
                    f"Task '{node.task_id}' references unknown dependency '{dep_id}'."
                )
            self.adj_list[dep_id].append(node.task_id)
            self.in_degree[node.task_id] += 1

        self.validate_graph()

    def validate_graph(self) -> None:
        """Validates cycle presence and maximum depth."""
        # 1. Topological sort & Cycle detection using Kahn's algorithm
        in_degree_copy = dict(self.in_degree)
        zero_in_degree = [node_id for node_id, deg in in_degree_copy.items() if deg == 0]
        zero_in_degree.sort()  # Deterministic ordering

        processed_count = 0
        depths: Dict[str, int] = {node_id: 1 for node_id in self.nodes}

        while zero_in_degree:
            curr = zero_in_degree.pop(0)
            processed_count += 1

            for child in self.adj_list.get(curr, []):
                depths[child] = max(depths[child], depths[curr] + 1)
                if depths[child] > self.max_depth:
                    raise InvalidMissionGraphError(
                        f"Graph maximum depth exceeded ({depths[child]} > {self.max_depth}) at node '{child}'."
                    )

                in_degree_copy[child] -= 1
                if in_degree_copy[child] == 0:
                    zero_in_degree.append(child)
                    zero_in_degree.sort()

        if processed_count != len(self.nodes):
            raise InvalidMissionGraphError("Cycle detected in mission graph DAG.")

    def get_execution_order(self) -> List[str]:
        """Returns deterministic topological execution order of task_ids."""
        in_degree_copy = dict(self.in_degree)
        zero_in_degree = [node_id for node_id, deg in in_degree_copy.items() if deg == 0]
        zero_in_degree.sort()

        order = []
        while zero_in_degree:
            curr = zero_in_degree.pop(0)
            order.append(curr)

            for child in self.adj_list.get(curr, []):
                in_degree_copy[child] -= 1
                if in_degree_copy[child] == 0:
                    zero_in_degree.append(child)
                    zero_in_degree.sort()

        return order

    def mark_task_failed(self, task_id: str) -> List[str]:
        """Marks task failed and propagates BLOCKED status to all downstream dependent tasks."""
        if task_id not in self.nodes:
            raise InvalidMissionGraphError(f"Task '{task_id}' not found in graph.")

        self.nodes[task_id].status = "FAILED"
        blocked_tasks = []

        queue = list(self.adj_list.get(task_id, []))
        while queue:
            child_id = queue.pop(0)
            if self.nodes[child_id].status not in ("FAILED", "BLOCKED"):
                self.nodes[child_id].status = "BLOCKED"
                blocked_tasks.append(child_id)
                queue.extend(self.adj_list.get(child_id, []))

        return blocked_tasks

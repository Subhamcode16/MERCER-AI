"""
Phase 25 Campaign Dependency Graph and Prerequisite Validator.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Set

@dataclass
class DependencyNode:
    node_id: str
    label: str
    node_type: str # TASK, DELIVERABLE, APPROVAL, RELEASE
    prerequisites: Set[str] = field(default_factory=set)
    completed: bool = False

class DependencyGraphViewer:
    """Computes dependency resolution and blocks actions if prerequisites are incomplete."""

    @staticmethod
    def evaluate_readiness(node: DependencyNode, completed_node_ids: Set[str]) -> bool:
        return node.prerequisites.issubset(completed_node_ids)

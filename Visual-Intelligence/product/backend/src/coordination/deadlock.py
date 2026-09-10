"""
Phase 12 Deadlock Detection Engine.

Detects cyclic resource waiting dependencies across concurrent missions
and selects a deterministic victim mission for safe preemption/checkpointing.
"""

from typing import List, Dict, Set, Optional, Tuple

from .models import CoordinationMission
from .exceptions import CoordinationDeadlock


class DeadlockDetector:
    """Detects cyclic resource dependency deadlocks across active missions."""

    def detect_deadlock(
        self,
        wait_for_graph: Dict[str, Set[str]]
    ) -> Optional[List[str]]:
        """Scans wait-for graph (mission_id -> set of mission_ids it is waiting on) for cycles."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycle_path: List[str] = []

        def dfs(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in wait_for_graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    # Cycle detected
                    idx = path.index(neighbor)
                    cycle_path.extend(path[idx:])
                    return True

            path.pop()
            rec_stack.remove(node)
            return False

        for mission_id in list(wait_for_graph.keys()):
            if mission_id not in visited:
                if dfs(mission_id, []):
                    return cycle_path

        return None

    def select_victim_mission(
        self,
        cycle_mission_ids: List[str],
        active_missions: List[CoordinationMission]
    ) -> CoordinationMission:
        """Selects deterministic victim mission (lowest priority or newest admission time) to preempt."""
        candidates = [m for m in active_missions if m.mission_id in cycle_mission_ids]
        if not candidates:
            raise CoordinationDeadlock(f"Deadlock cycle detected in {cycle_mission_ids}, but no candidate missions found.")

        # Sort by priority rank descending (numerical higher = lower priority), then admission timestamp descending (newest first)
        candidates.sort(key=lambda m: (m.priority.value, -m.admission_timestamp.timestamp()), reverse=True)
        return candidates[0]

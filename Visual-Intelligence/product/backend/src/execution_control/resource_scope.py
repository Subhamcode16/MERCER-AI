"""
Phase 10 — Resource Scope & Boundary Matcher

Defines hierarchical resource scope contracts and enforces strict resource boundary matching
to prevent cross-resource escalation or unauthorized scope expansion.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from src.execution_control.exceptions import ResourceScopeViolationError


@dataclass(frozen=True)
class ResourceScope:
    """Hierarchical Resource Scope representation (e.g. 'brand:aura/campaign:fall2026/asset:01')."""

    scope_string: str

    def __post_init__(self):
        if isinstance(self.scope_string, bool) or not isinstance(self.scope_string, str) or not self.scope_string.strip():
            raise ResourceScopeViolationError("Resource scope string must be a non-empty string.")

    def parse_components(self) -> Dict[str, str]:
        """Parses resource scope string into component key-value pairs."""
        components: Dict[str, str] = {}
        segments = self.scope_string.strip().split("/")
        for seg in segments:
            if ":" in seg:
                k, v = seg.split(":", 1)
                components[k.strip().lower()] = v.strip().lower()
            else:
                components[seg.strip().lower()] = "*"
        return components

    def matches(self, target_scope: "ResourceScope") -> bool:
        """Checks if this scope grants access to target_scope."""
        if self.scope_string == "*" or self.scope_string == target_scope.scope_string:
            return True

        self_comp = self.parse_components()
        target_comp = target_scope.parse_components()

        # All self_comp constraints must match target_comp
        for k, v in self_comp.items():
            if v == "*":
                continue
            if k not in target_comp:
                return False
            if target_comp[k] != v and target_comp[k] != "*":
                return False

        return True

    def validate_boundary(self, target_scope: "ResourceScope") -> None:
        """Validates that this scope covers target_scope; raises ResourceScopeViolationError if breached."""
        if not self.matches(target_scope):
            raise ResourceScopeViolationError(
                f"Resource boundary violation: Authorized scope '{self.scope_string}' does not permit action on target scope '{target_scope.scope_string}'."
            )

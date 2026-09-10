"""
Phase 9 — Adaptive Strategy & Allowlist Engine

Defines versioned AdaptiveStrategy configurations, enforcing an explicit Operational & Tactical Allowlist
and raising SecurityBoundaryViolation if security substrate parameters are targeted for mutation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
import os
from pathlib import Path
import tempfile
import threading
from typing import Any, Dict, List, Optional


class StrategyStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    OFFLINE_EVALUATION = "OFFLINE_EVALUATION"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


class SecurityBoundaryViolation(PermissionError):
    """Raised when an adaptive strategy attempts to mutate forbidden security substrate parameters."""

    pass


# Explicit Operational & Tactical Allowlist confirmed during Mandatory Understanding Phase
MUTABLE_FIELD_ALLOWLIST = {
    "staff_ordering",
    "task_graph_depth",
    "critique_weights",
    "context_limits",
    "research_depth",
    "versioned_role_prompts",
    "revision_iteration_cap",
    "benchmark_selection_weights",
}

# Forbidden Security Substrate Fields (Must NEVER be mutated by learning or strategy adaptation)
FORBIDDEN_SECURITY_FIELDS = {
    "execution_gate",
    "execution_gate_permitted",
    "epistemic_state",
    "audit_integrity",
    "recovery_manager",
    "attestation_registry",
    "trust_anchors",
    "security_policy",
    "hardware_custody",
}


@dataclass(frozen=True)
class AdaptiveStrategy:
    """Versioned orchestration strategy configuration."""

    strategy_version_id: str
    parent_version_id: Optional[str]
    parameters: Dict[str, Any]
    status: StrategyStatus = StrategyStatus.CANDIDATE
    rationale: str = ""
    benchmark_score: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def validate_allowlist(self) -> None:
        """Validates that parameters contain only allowlisted operational fields and zero security targets."""
        for param_key in self.parameters.keys():
            lower_key = str(param_key).lower()

            # Check if attempting to mutate forbidden security fields
            if any(forbidden in lower_key for forbidden in FORBIDDEN_SECURITY_FIELDS):
                raise SecurityBoundaryViolation(
                    f"Adaptive strategy '{self.strategy_version_id}' attempted to mutate forbidden security field '{param_key}'."
                )

            # Check if param key is within explicit allowlist
            if lower_key not in MUTABLE_FIELD_ALLOWLIST:
                raise SecurityBoundaryViolation(
                    f"Parameter '{param_key}' is not in the explicit Phase 9 MUTABLE_FIELD_ALLOWLIST."
                )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_version_id": self.strategy_version_id,
            "parent_version_id": self.parent_version_id,
            "parameters": self.parameters,
            "status": self.status.value if isinstance(self.status, Enum) else str(self.status),
            "rationale": self.rationale,
            "benchmark_score": self.benchmark_score,
            "timestamp": self.timestamp,
        }


class AdaptiveStrategyStore:
    """File-backed storage engine for versioned Adaptive Strategy configurations."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "data", "phase9_strategies")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_default_v1_strategy()

    def _init_default_v1_strategy(self) -> None:
        """Ensures default Strategy V1 exists."""
        v1_path = self.base_dir / "strat_v1_default.json"
        if not v1_path.exists():
            v1_strategy = AdaptiveStrategy(
                strategy_version_id="strat_v1_default",
                parent_version_id=None,
                parameters={
                    "staff_ordering": [
                        "RESEARCHER",
                        "STRATEGIST",
                        "DESIGNER",
                        "CONTENT_SPECIALIST",
                        "TREND_ANALYST",
                        "CRITIC",
                        "REVIEWER",
                    ],
                    "task_graph_depth": 7,
                    "critique_weights": {
                        "visual_consistency": 0.25,
                        "brand_alignment": 0.25,
                        "typography_hierarchy": 0.25,
                        "market_relevance": 0.25,
                    },
                    "context_limits": {"max_tokens_per_task": 4096},
                    "research_depth": "STANDARD",
                    "revision_iteration_cap": 3,
                    "benchmark_selection_weights": {"default": 1.0},
                    "versioned_role_prompts": {},
                },
                status=StrategyStatus.ACTIVE,
                rationale="Default Baseline Phase 8 Strategy V1",
                benchmark_score=78.5,
            )
            self.save_strategy(v1_strategy)

    def save_strategy(self, strategy: AdaptiveStrategy) -> str:
        """Validates security allowlist and saves strategy atomically."""
        strategy.validate_allowlist()

        file_path = self.base_dir / f"{strategy.strategy_version_id}.json"
        strat_dict = strategy.to_dict()

        with self._lock:
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.base_dir, prefix="strat_tmp_", suffix=".tmp"
            )
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(strat_dict, f, indent=2)
                os.replace(temp_path, file_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

        return str(file_path)

    def get_strategy(self, strategy_version_id: str) -> AdaptiveStrategy:
        """Loads a versioned strategy."""
        file_path = self.base_dir / f"{strategy_version_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Strategy '{strategy_version_id}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return AdaptiveStrategy(
            strategy_version_id=data["strategy_version_id"],
            parent_version_id=data["parent_version_id"],
            parameters=data["parameters"],
            status=StrategyStatus(data["status"]),
            rationale=data["rationale"],
            benchmark_score=data["benchmark_score"],
            timestamp=data["timestamp"],
        )

    def get_active_strategy(self) -> AdaptiveStrategy:
        """Returns the currently ACTIVE strategy, defaulting to strat_v1_default."""
        active_strats = []
        for file_path in self.base_dir.glob("*.json"):
            try:
                strat = self.get_strategy(file_path.stem)
                if strat.status == StrategyStatus.ACTIVE:
                    active_strats.append(strat)
            except Exception:
                continue

        if not active_strats:
            return self.get_strategy("strat_v1_default")

        # Sort by timestamp descending
        active_strats.sort(key=lambda s: s.timestamp, reverse=True)
        return active_strats[0]

    def clear(self) -> None:
        """Removes non-default strategies."""
        with self._lock:
            for file_path in self.base_dir.glob("*.json"):
                if file_path.name != "strat_v1_default.json":
                    try:
                        file_path.unlink()
                    except OSError:
                        pass

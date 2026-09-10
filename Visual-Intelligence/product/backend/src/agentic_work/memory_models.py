"""
Phase 9 — Memory Models & Data Contracts

Defines immutable data contracts for persistent workflow memory, structured feedback records,
aggregated learning patterns, artifact lineage records, and workflow execution outcomes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Dict, List, Optional


class FeedbackSource(str, Enum):
    USER = "USER"
    EVALUATOR = "EVALUATOR"
    CRITIC_SYSTEM = "CRITIC_SYSTEM"
    REVIEWER_SYSTEM = "REVIEWER_SYSTEM"


class LearningPatternType(str, Enum):
    RECURRING_DEFECT = "RECURRING_DEFECT"
    QUALITY_IMPROVEMENT = "QUALITY_IMPROVEMENT"
    TREND_INTEGRATION = "TREND_INTEGRATION"
    REVISION_REDUCTION = "REVISION_REDUCTION"
    CONTEXT_OPTIMIZATION = "CONTEXT_OPTIMIZATION"


@dataclass(frozen=True)
class ArtifactLineageRecord:
    """Immutable record tracking complete artifact provenance and ancestry."""

    artifact_id: str
    workflow_id: str
    task_id: str
    task_graph_version: str
    staff_contributions: List[str]
    knowledge_observation_ids: List[str]
    critique_scores: Dict[str, float]
    review_scores: Dict[str, float]
    revision_count: int
    active_strategy_version: str
    payload_hash: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def compute_hash(self) -> str:
        data = {
            "artifact_id": self.artifact_id,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id,
            "task_graph_version": self.task_graph_version,
            "staff_contributions": sorted(self.staff_contributions),
            "knowledge_observation_ids": sorted(self.knowledge_observation_ids),
            "critique_scores": self.critique_scores,
            "review_scores": self.review_scores,
            "revision_count": self.revision_count,
            "active_strategy_version": self.active_strategy_version,
            "payload_hash": self.payload_hash,
        }
        raw_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id,
            "task_graph_version": self.task_graph_version,
            "staff_contributions": self.staff_contributions,
            "knowledge_observation_ids": self.knowledge_observation_ids,
            "critique_scores": self.critique_scores,
            "review_scores": self.review_scores,
            "revision_count": self.revision_count,
            "active_strategy_version": self.active_strategy_version,
            "payload_hash": self.payload_hash,
            "timestamp": self.timestamp,
            "lineage_hash": self.compute_hash(),
        }


@dataclass(frozen=True)
class FeedbackRecord:
    """Structured feedback record captured from users, evaluators, or staff critique."""

    feedback_id: str
    workflow_id: str
    source: FeedbackSource
    category: str
    target_role: str
    rating: float  # 0.0 to 1.0 or scale
    comments: str
    defect_code: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feedback_id": self.feedback_id,
            "workflow_id": self.workflow_id,
            "source": self.source.value if isinstance(self.source, Enum) else str(self.source),
            "category": self.category,
            "target_role": self.target_role,
            "rating": self.rating,
            "comments": self.comments,
            "defect_code": self.defect_code,
            "timestamp": self.timestamp,
        }


@dataclass(frozen=True)
class LearningPattern:
    """Aggregated learning pattern generated from N >= 3 consistent feedback signals."""

    pattern_id: str
    pattern_type: LearningPatternType
    target_role: str
    trigger_defect_code: str
    occurrence_count: int
    supporting_feedback_ids: List[str]
    suggested_adaptation: Dict[str, Any]
    confidence_score: float
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type.value if isinstance(self.pattern_type, Enum) else str(self.pattern_type),
            "target_role": self.target_role,
            "trigger_defect_code": self.trigger_defect_code,
            "occurrence_count": self.occurrence_count,
            "supporting_feedback_ids": self.supporting_feedback_ids,
            "suggested_adaptation": self.suggested_adaptation,
            "confidence_score": self.confidence_score,
            "timestamp": self.timestamp,
        }


@dataclass(frozen=True)
class WorkflowMemoryRecord:
    """Durable record of a completed workflow execution."""

    memory_id: str
    workflow_id: str
    task_type: str
    staff_participation: List[str]
    task_graph_version: str
    input_metadata: Dict[str, Any]
    output_artifact_ids: List[str]
    critique_scores: Dict[str, float]
    review_scores: Dict[str, float]
    feedback_ids: List[str]
    failure_signals: List[str]
    revision_count: int
    active_strategy_version: str
    benchmark_scores: Dict[str, float]
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def compute_hash(self) -> str:
        data = {
            "memory_id": self.memory_id,
            "workflow_id": self.workflow_id,
            "task_type": self.task_type,
            "staff_participation": sorted(self.staff_participation),
            "task_graph_version": self.task_graph_version,
            "output_artifact_ids": sorted(self.output_artifact_ids),
            "revision_count": self.revision_count,
            "active_strategy_version": self.active_strategy_version,
        }
        raw_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "workflow_id": self.workflow_id,
            "task_type": self.task_type,
            "staff_participation": self.staff_participation,
            "task_graph_version": self.task_graph_version,
            "input_metadata": self.input_metadata,
            "output_artifact_ids": self.output_artifact_ids,
            "critique_scores": self.critique_scores,
            "review_scores": self.review_scores,
            "feedback_ids": self.feedback_ids,
            "failure_signals": self.failure_signals,
            "revision_count": self.revision_count,
            "active_strategy_version": self.active_strategy_version,
            "benchmark_scores": self.benchmark_scores,
            "timestamp": self.timestamp,
            "record_hash": self.compute_hash(),
        }

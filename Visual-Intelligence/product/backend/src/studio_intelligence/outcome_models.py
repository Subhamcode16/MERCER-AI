"""
Phase 18 Outcome & Intelligence Models.

Immutable contracts and dataclasses for closed-loop studio intelligence,
outcome observations, performance evaluations, learning signals, and strategy experiments.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import hashlib
import json

from src.studio_intelligence.exceptions import OutcomeValidationError


class OutcomeProvenance(str, Enum):
    UNTRUSTED_EXTERNAL_OBSERVATION = "UNTRUSTED_EXTERNAL_OBSERVATION"
    SIMULATED_SANDBOX_OBSERVATION = "SIMULATED_SANDBOX_OBSERVATION"
    INTERNAL_TELEMETRY = "INTERNAL_TELEMETRY"


class LearningStage(str, Enum):
    OBSERVED = "OBSERVED"
    ATTRIBUTED = "ATTRIBUTED"
    EVALUATED = "EVALUATED"
    LEARNING_SIGNAL = "LEARNING_SIGNAL"
    HYPOTHESIS = "HYPOTHESIS"
    CANDIDATE_STRATEGY = "CANDIDATE_STRATEGY"
    BENCHMARKED = "BENCHMARKED"
    ADOPTED = "ADOPTED"
    REJECTED = "REJECTED"


class ExperimentStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    BENCHMARKING = "BENCHMARKING"
    PROMOTED = "PROMOTED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass(frozen=True)
class OutcomeObservation:
    """Immutable external outcome metric payload tagged with provenance."""
    observation_id: str
    client_id: str
    campaign_id: str
    deliverable_id: str
    work_item_id: str
    platform: str
    metrics: Dict[str, float]
    raw_payload: Dict[str, Any]
    provenance: OutcomeProvenance = OutcomeProvenance.UNTRUSTED_EXTERNAL_OBSERVATION
    timestamp: float = field(default_factory=time.time)
    hash_signature: str = ""

    def __post_init__(self):
        if not self.observation_id or not self.client_id:
            raise OutcomeValidationError("Observation ID and Client ID must be specified.")
        if not isinstance(self.metrics, dict):
            raise OutcomeValidationError("Metrics must be a dictionary of numerical scores.")
        
        # Compute signature if empty
        if not self.hash_signature:
            payload_str = f"{self.observation_id}:{self.client_id}:{self.deliverable_id}:{json.dumps(self.metrics, sort_keys=True)}"
            computed_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
            object.__setattr__(self, "hash_signature", computed_hash)


@dataclass(frozen=True)
class OutcomeEvaluation:
    """Evaluated performance metrics calculated from an observation."""
    evaluation_id: str
    observation_id: str
    client_id: str
    objective_attainment_score: float
    engagement_efficiency_score: float
    revision_efficiency_score: float
    approval_latency_sec: float
    reliability_score: float
    overall_score: float
    metrics_breakdown: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if not self.evaluation_id or not self.client_id:
            raise OutcomeValidationError("Evaluation ID and Client ID are required.")


@dataclass(frozen=True)
class LearningSignal:
    """Extracted learning signal linking evaluation to candidate hypothesis."""
    signal_id: str
    evaluation_id: str
    client_id: str
    stage: LearningStage
    category: str
    observation_summary: str
    proposed_hypothesis: str
    strategy_variables: Dict[str, Any]
    confidence_score: float = 0.8
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if not self.signal_id or not self.client_id:
            raise OutcomeValidationError("Signal ID and Client ID are required.")


@dataclass(frozen=True)
class CandidateStrategy:
    """Candidate operational/creative strategy proposed for benchmarking."""
    strategy_id: str
    client_id: str
    version: int
    name: str
    hypothesis: str
    strategy_variables: Dict[str, Any]
    baseline_metrics: Dict[str, float]
    status: ExperimentStatus = ExperimentStatus.CREATED
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class StrategyExperiment:
    """A/B or sequential experiment evaluating candidate strategy against baseline."""
    experiment_id: str
    candidate_id: str
    client_id: str
    baseline_metrics: Dict[str, float]
    candidate_metrics: Dict[str, float]
    status: ExperimentStatus = ExperimentStatus.RUNNING
    evidence_window_days: int = 7
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class PromotionRecord:
    """Audit record of candidate strategy promotion to active baseline."""
    promotion_id: str
    candidate_id: str
    client_id: str
    approved_by: str
    benchmark_summary: Dict[str, Any]
    policy_compliance_checked: bool = True
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class IntelligenceKnowledgeItem:
    """Structured reusable knowledge item derived from adopted strategies."""
    item_id: str
    client_id: str
    category: str
    title: str
    content: str
    confidence_score: float
    source_signal_ids: List[str]
    timestamp: float = field(default_factory=time.time)

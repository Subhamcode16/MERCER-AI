"""
Phase 28 Governed Experiment Registry.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone


class ExperimentStatus(str, Enum):
    HYPOTHESIS = "HYPOTHESIS"
    DESIGN = "DESIGN"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    RUNNING = "RUNNING"
    COLLECTING = "COLLECTING"
    ANALYZED = "ANALYZED"
    PROMOTED = "PROMOTED"
    REJECTED = "REJECTED"
    RETAINED_AS_PROVISIONAL = "RETAINED_AS_PROVISIONAL"


@dataclass
class ExperimentVariant:
    variant_id: str
    name: str  # e.g. "Variant A: Monolithic Late Sun", "Variant B: Studio Neon Noir"
    allocation_percent: float
    asset_id: str


@dataclass
class ControlledExperiment:
    experiment_id: str
    campaign_id: str
    hypothesis_id: str
    title: str
    variants: List[ExperimentVariant]
    target_metric: str  # e.g. "CTR", "DWELL_TIME"
    status: ExperimentStatus
    sample_size_collected: int = 0
    variant_results: Dict[str, float] = field(default_factory=dict)
    statistical_significance: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ExperimentRegistry:
    """Manages controlled experiment lifecycle, traffic allocation, and statistical validation."""

    def __init__(self):
        self._experiments: Dict[str, ControlledExperiment] = {}

    def register_experiment(
        self,
        campaign_id: str,
        hypothesis_id: str,
        title: str,
        variants: List[Dict[str, Any]],
        target_metric: str = "CTR",
    ) -> ControlledExperiment:
        exp_variants = [
            ExperimentVariant(
                variant_id=f"var_{uuid.uuid4().hex[:6]}",
                name=v.get("name", f"Variant {i+1}"),
                allocation_percent=v.get("allocation", 50.0),
                asset_id=v.get("asset_id", f"ast_v{i+1}"),
            )
            for i, v in enumerate(variants)
        ]

        exp = ControlledExperiment(
            experiment_id=f"exp_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            hypothesis_id=hypothesis_id,
            title=title,
            variants=exp_variants,
            target_metric=target_metric,
            status=ExperimentStatus.DESIGN,
        )
        self._experiments[exp.experiment_id] = exp
        return exp

    def transition_status(self, experiment_id: str, target_status: ExperimentStatus) -> ControlledExperiment:
        exp = self._experiments.get(experiment_id)
        if not exp:
            raise KeyError(f"Experiment '{experiment_id}' not found.")
        exp.status = target_status
        return exp

    def record_results(
        self,
        experiment_id: str,
        results: Dict[str, float],
        sample_size: int,
        p_value: float = 0.02,
    ) -> ControlledExperiment:
        exp = self._experiments.get(experiment_id)
        if not exp:
            raise KeyError(f"Experiment '{experiment_id}' not found.")
        exp.variant_results = results
        exp.sample_size_collected = sample_size
        exp.statistical_significance = round(1.0 - p_value, 3)
        exp.status = ExperimentStatus.ANALYZED
        return exp

    def get_experiment(self, experiment_id: str) -> Optional[ControlledExperiment]:
        return self._experiments.get(experiment_id)

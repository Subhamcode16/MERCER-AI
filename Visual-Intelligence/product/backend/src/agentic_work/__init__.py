"""
Visual Intelligence Agentic Work Layer — Package Exports.
"""

from .models import (
    StaffRole,
    TaskStatus,
    AdaptiveStatus,
    StaffCapability,
    StaffProfile,
    StaffTask,
    StaffResult,
    CritiqueResult,
    ReviewResult,
    LearningSignal,
    AdaptiveChange,
    VisualObservation,
    ObservationClassification,
    ObservationCommitment,
    ObservationStatus,
)
from .context import (
    SystemContext,
    WorkflowContext,
    TaskContext,
    StaffContext,
    ReviewContext,
)
from .staff import (
    BaseStaff,
    ResearcherStaff,
    StrategistStaff,
    DesignerStaff,
    ContentSpecialistStaff,
    TrendAnalystStaff,
    CriticStaff,
    ReviewerStaff,
)
from .staff_registry import StaffRegistry
from .task_graph import TaskGraph
from .critique import CritiqueEngine
from .review import ReviewEngine
from .feedback import FeedbackEngine
from .learning import LearningEngine
from .knowledge import KnowledgeStore
from .trend_intelligence import TrendIntelligenceEngine
from .improvement import ImprovementManager
from .evaluation import EvaluationEngine, WorkflowEvaluationMetrics
from .orchestrator import WorkOrchestrator

# Phase 9 Exports
from .memory_models import (
    WorkflowMemoryRecord,
    FeedbackRecord,
    FeedbackSource,
    LearningPattern,
    LearningPatternType,
    ArtifactLineageRecord,
)
from .memory_store import WorkflowMemoryStore, SecretStorageForbiddenError, MemoryIntegrityError
from .persistent_feedback import PersistentFeedbackEngine, DuplicateFeedbackError
from .persistent_knowledge import PersistentKnowledgeStore
from .artifact_lineage import ArtifactLineageTracker, LineageTamperError
from .adaptive_strategy import (
    AdaptiveStrategy,
    AdaptiveStrategyStore,
    StrategyStatus,
    SecurityBoundaryViolation,
    MUTABLE_FIELD_ALLOWLIST,
)
from .benchmark_suite import (
    BenchmarkCategory,
    CategoryBenchmarkResult,
    BenchmarkSuiteResult,
    BenchmarkSuiteRunner,
)
from .persistent_improvement import PersistentImprovementEngine, DegradationRejectedError
from .learning_governance import LearningGovernanceBarrier

__all__ = [
    "StaffRole",
    "TaskStatus",
    "AdaptiveStatus",
    "StaffCapability",
    "StaffProfile",
    "StaffTask",
    "StaffResult",
    "CritiqueResult",
    "ReviewResult",
    "LearningSignal",
    "AdaptiveChange",
    "VisualObservation",
    "SystemContext",
    "WorkflowContext",
    "TaskContext",
    "StaffContext",
    "ReviewContext",
    "BaseStaff",
    "ResearcherStaff",
    "StrategistStaff",
    "DesignerStaff",
    "ContentSpecialistStaff",
    "TrendAnalystStaff",
    "CriticStaff",
    "ReviewerStaff",
    "StaffRegistry",
    "TaskGraph",
    "CritiqueEngine",
    "ReviewEngine",
    "FeedbackEngine",
    "LearningEngine",
    "KnowledgeStore",
    "TrendIntelligenceEngine",
    "ImprovementManager",
    "EvaluationEngine",
    "WorkflowEvaluationMetrics",
    "WorkOrchestrator",
    # Phase 9
    "WorkflowMemoryRecord",
    "FeedbackRecord",
    "FeedbackSource",
    "LearningPattern",
    "LearningPatternType",
    "ArtifactLineageRecord",
    "WorkflowMemoryStore",
    "SecretStorageForbiddenError",
    "MemoryIntegrityError",
    "PersistentFeedbackEngine",
    "DuplicateFeedbackError",
    "PersistentKnowledgeStore",
    "ArtifactLineageTracker",
    "LineageTamperError",
    "AdaptiveStrategy",
    "AdaptiveStrategyStore",
    "StrategyStatus",
    "SecurityBoundaryViolation",
    "MUTABLE_FIELD_ALLOWLIST",
    "BenchmarkCategory",
    "CategoryBenchmarkResult",
    "BenchmarkSuiteResult",
    "BenchmarkSuiteRunner",
    "PersistentImprovementEngine",
    "DegradationRejectedError",
    "LearningGovernanceBarrier",
]

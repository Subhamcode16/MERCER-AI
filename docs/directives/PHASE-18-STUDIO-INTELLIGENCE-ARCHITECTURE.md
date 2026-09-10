# Phase 18 — ILYREN Studio Intelligence Architecture

**Document Status:** RATIFIED & APPROVED  
**Phase:** 18  
**Architectural Layer:** Closed-Loop Studio Intelligence & Provider Operations  

---

## 1. Architectural Principles & Governing Invariants

Phase 18 establishes the **Real-World Provider Operations & Closed-Loop Studio Intelligence Boundary** above Phase 17 Production Fabric and Phase 16 Client Command Center.

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$

$$\mathbf{Outcome \neq Truth} \quad \Big| \quad \mathbf{Learning \neq Policy\ Mutation}$$

$$\mathbf{Optimization \neq Self\ Authorization} \quad \Big| \quad \mathbf{External\ Provider\ Access \neq Blanket\ Access}$$

---

## 2. Core Closed-Loop Intelligence Progression

```text
CLIENT OBJECTIVE
       ↓
PHASE 16 CLIENT EXPERIENCE
       ↓
PHASE 17 PRODUCTION FABRIC
       ↓
PHASE 14 CREATIVE WORKFORCE
       ↓
PHASE 15 STUDIO OPERATIONS
       ↓
PHASE 10 HUMAN AUTHORIZATION
       ↓
PHASE 13 PROVIDER INTEGRATION / SANDBOX PROVIDERS
       ↓
OUTCOME OBSERVATION (UNTRUSTED_EXTERNAL_OBSERVATION)
       ↓
ATTRIBUTION ENGINE
       ↓
PERFORMANCE EVALUATOR
       ↓
FEEDBACK FUSION ENGINE
       ↓
LEARNING SIGNAL
       ↓
STRATEGY EXPERIMENT ENGINE (A/B / Sequential)
       ↓
PROMOTION CONTROLLER (Benchmark vs Baseline)
       ↓
ADOPTION OR DEGRADATION ROLLBACK
       ↓
STUDIO INTELLIGENCE MEMORY
       ↓
IMPROVED FUTURE WORK
```

---

## 3. Core Component Inventory (`src/studio_intelligence/`)

1. **`exceptions.py`**: Fail-closed exception hierarchy (`StudioIntelligenceError`, `OutcomeValidationError`, `AttributionError`, `EvaluationError`, `ProviderRuntimeError`, `LearningBoundaryViolation`, `OptimizationRejectedError`, `CrossClientIntelligenceViolation`, `ExperimentRaceError`, `IntelligenceLedgerError`).
2. **`outcome_models.py`**: Immutable dataclasses (`OutcomeObservation`, `OutcomeEvaluation`, `LearningSignal`, `CandidateStrategy`, `StrategyExperiment`, `PromotionRecord`, `IntelligenceKnowledgeItem`) and FSM state machines.
3. **`outcome_store.py`**: `OutcomeStore` providing atomic, hash-linked observation storage with anti-replay defense and multi-client isolation.
4. **`attribution.py`**: `CreativeOutcomeAttributionEngine` linking observations to staff assignments, creative direction, visual DNA, copy strategy, trend observations, and approvals without unproven causal leaps.
5. **`evaluation.py`**: `CreativePerformanceEvaluator` scoring objective attainment, engagement efficiency, revision efficiency, approval latency, and reliability.
6. **`provider_contracts.py`**: Abstract interfaces (`ISocialProvider`, `IAnalyticsProvider`, `IAssetProvider`, `INotificationProvider`, `ISchedulingProvider`).
7. **`sandbox_providers.py`**: Deterministic sandbox implementations supporting creation, publishing, scheduling, analytics, rate limits (429), timeouts (504), duplicates (409), and stale data.
8. **`provider_runtime.py`**: `StudioProviderRuntime` delegating all provider operations through Phase 13 `IntegrationController` controls.
9. **`feedback_fusion.py`**: `FeedbackFusionEngine` fusing client feedback, human review scores, and performance metrics into `LearningSignal`s without policy mutations.
10. **`experiment.py`**: `StrategyExperimentEngine` managing candidate hypotheses, baseline metrics, evidence windows, and race defense.
11. **`promotion.py`**: `StrategyPromotionController` evaluating candidate benchmarks against baseline, promoting proven candidates and rejecting degraded candidates.
12. **`intelligence_memory.py`**: `StudioIntelligenceMemory` storing reusable creative patterns per client context under unshared isolation.
13. **`studio_learning.py`**: `StudioLearningEngine` enforcing the explicit progression `OBSERVED -> ATTRIBUTED -> EVALUATED -> LEARNING_SIGNAL -> HYPOTHESIS -> CANDIDATE_STRATEGY -> BENCHMARKED -> ADOPTED/REJECTED`.
14. **`continuous_optimizer.py`**: `ContinuousStudioOptimizer` coordinating candidate selection, benchmarking, degradation rejection (`OptimizationRejectedError`), promotion, and deterministic rollback.
15. **`intelligence_dashboard.py`**: `StudioIntelligenceDashboard` rendering safe DTO projections without credentials or CoT reasoning leakage.
16. **`intelligence_ledger.py`**: `StudioIntelligenceLedger` maintaining an append-only SHA-256 hash-linked audit log in `data/phase18_intelligence_ledger/`.
17. **`orchestrator.py`**: `StudioIntelligenceOrchestrator` primary facade integrating Phases 8–18.
18. **`__init__.py`**: Clean exports.

# STRATEGIC-DECISION-MEMORY.md
## Phase 29 Architecture Specification: Strategic Decision Memory & Quality Decoupling

---

### 1. Overview

**Strategic Decision Memory** persists the contextual state, rationale, and accepted uncertainties of human decisions, explicitly separating **Decision Quality** from subsequent **Outcome Quality**.

A high-rigor decision can encounter market shocks and yield negative lift; a low-rigor guess can stumble into lucky positive lift. ILYREN records both independently to prevent hindsight bias and outcome bias.

---

### 2. Decision Memory Record Topology

```python
class StrategicDecisionMemoryRecord:
    record_id: str
    tenant_id: str
    decision_record: HumanDecisionRecord
    decision_quality_grade: DecisionQualityGrade  # HIGH_RIGOR / MODERATE_RIGOR / LOW_RIGOR
    subsequent_outcome_metrics: Dict[str, Any]    # Recorded weeks/months later
    outcome_observed_at: Optional[datetime]
    outcome_alignment: Optional[str]              # ALIGNED / DIVERGED / INCONCLUSIVE
    retrospective_learnings: List[str]
```

---

### 3. Decision Quality Grading Rubric

- **`HIGH_RIGOR_EVIDENCE_BOUND`:** Decision backed by experimental evidence, explicit falsification criteria, bounded reversibility, and accounted counter-theses.
- **`MODERATE_RIGOR_ASSUMPTIONS_CONTAINED`:** Decision based on observational correlations with documented assumptions and risk limits.
- **`LOW_RIGOR_SPECULATIVE`:** Intuitive decision with minimal empirical support, flagged for tight monitoring.

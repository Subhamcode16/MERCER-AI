# STRATEGIC-SIGNAL-ENGINE.md
## Phase 29 Architecture Specification: Strategic Signal Engine

---

### 1. Overview

The **Strategic Signal Engine** processes raw observations, empirical campaign shifts, and market trends into bounded, contextualized **Strategic Signals**.

Under the core invariant:
$$\mathbf{Signal \neq Fact} \quad \mathbf{Correlation \neq Causal\ Proof}$$

---

### 2. Signal Taxonomy (15 Classes)

1. `EMERGING_PATTERN`: Rapidly developing creative or channel correlation.
2. `DECLINING_PATTERN`: Decreasing engagement on legacy visual configurations.
3. `PERFORMANCE_SHIFT`: Statistically significant lift or drop in campaign conversions.
4. `CREATIVE_FATIGUE`: Ad burnout caused by frequency saturation.
5. `AUDIENCE_SHIFT`: Demographic or channel migration.
6. `PRODUCT_OPPORTUNITY`: Under-served product line or category fit.
7. `MARKET_SIGNAL`: Macro industry shifts or competitive movements.
8. `VISUAL_SHIFT`: Visual DNA cluster transitions.
9. `KNOWLEDGE_CONTRADICTION`: Conflicting evidence across distinct sub-scopes.
10. `KNOWLEDGE_DECAY`: Stale historical models experiencing half-life decay.
11. `ENVIRONMENT_DRIFT`: Population Stability Index (PSI) platform shifts.
12. `MODEL_DRIFT`: Shift in AI generator or embedding distributions.
13. `RISK_SIGNAL`: Material threat to brand equity or budget efficiency.
14. `EXPERIMENT_OPPORTUNITY`: High-value hypothesis ready for randomized A/B trial.
15. `UNCERTAINTY_CLUSTER`: Ambiguity requiring experimental clarity.

---

### 3. Epistemic Metadata Contract

No strategic signal may be emitted without:
- `signal_id` & `provenance_hash`
- `epistemic_status` (`OBSERVATIONAL_CORRELATION`, `EXPERIMENTAL_EVIDENCE`, etc.)
- `confidence` (calibrated between 0.0 and 1.0)
- `supporting_evidence` & `contradicting_evidence`
- `assumptions`
- `unknowns` (must survive and never be empty)
- `freshness` (exponential decay score)

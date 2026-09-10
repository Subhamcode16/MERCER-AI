# Phase 28: Epistemic Attribution & Confounder Model

## 1. Causal Separation & Taxonomy
Observed performance data is strictly partitioned into:
- **Observation:** Raw metric value (e.g. CTR = 4.2%).
- **Measurement:** Normalized calculation against baseline.
- **Attribution:** Multi-touch allocation across campaign touchpoints.
- **Interpretation:** Qualitative rationale (e.g. "Raking lighting increased silhouette clarity").
- **Hypothesis:** Testable prediction for future campaigns.
- **Causal Status:** `CORRELATIONAL_OBSERVATIONAL`, `CONFOUNDED`, or `CONTROLLED_EXPERIMENT`.

## 2. Confounder Detection
The engine scans for external anomalies including macro seasonality, ad spend surges, pricing shifts, and inventory fluctuations, attaching mandatory epistemic disclaimers to prevent false causal assertions.

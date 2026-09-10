# PRODUCT-LEARNING-SURFACE-AND-EXPLAINABILITY-UX.md
## Phase 28 Architecture Specification: Product Learning Surface & Explainability UX

---

### 1. Executive Overview

The ILYREN Creative Intelligence operating loop is not a black-box optimizer. It exposes an operator-grade **Learning & Calibration Command Surface** that provides full transparent inspection into:
1. Every attribution decision and its underlying confounder score.
2. Every active hypothesis and its counterfactual integrity.
3. Live calibration tracking across AI models vs empirical outcomes.
4. One-click human approval / rejection / rollback controls for knowledge promotion.

---

### 2. Learning Surface UI / UX Topology

```
+-----------------------------------------------------------------------------------------+
| ILYREN Creative Intelligence: Learning & Calibration Command Surface                   |
+-----------------------------------------------------------------------------------------+
| [Overview]   [Attribution Explorer]   [Calibration Radar]   [Knowledge Promotion Queue] |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
| 1. EPISTEMIC ATTRIBUTION EXPLORER                                                       |
|    Campaign: "Summer Drop 2026" | Asset: "HERO-001.mp4" | Lift: +34%                    |
|    Epistemic Grade: [ CORRELATIONAL_OBSERVATIONAL ]                                    |
|    Confounders Detected: [ Seasonality: High ] [ Price Promo: Active (-20%) ]           |
|    Raw CTR Lift: +34% ====> Adjusted Isolated Lift: +8.2%                              |
|    Counterfactual Status: [ COUNTERFACTUAL_UNKNOWN (Unobserved Baseline) ]               |
|                                                                                         |
| 2. MODEL CALIBRATION RADAR                                                              |
|    Model: gemini-2.5-flash | Skill: luxury-copywriter                                   |
|    Brier Score: 0.142 (Well-Calibrated) | Overconfidence Penalty: 0.03                 |
|    Calibration Curve: [ Empirical 78% vs Predicted 81% ]                               |
|                                                                                         |
| 3. KNOWLEDGE PROMOTION QUEUE (Requires Operator Sign-off)                               |
|    Hypothesis: "Serif minimal typography improves luxury retention by 12%"              |
|    Evidence Base: 14 campaigns, 2 A/B experiments | P-value: 0.012                      |
|    [ APPROVE PROMOTION ]       [ REJECT ]       [ QUARANTINE ]                          |
+-----------------------------------------------------------------------------------------+
```

---

### 3. API Contract Endpoints

The dedicated Phase 28 Learning API router exposes the following REST endpoints:

- `GET /api/v1/learning/ledger/blocks` - Retrieve cryptographic decision ledger chain.
- `POST /api/v1/learning/outcomes/ingest` - Ingest raw platform campaign outcome data.
- `POST /api/v1/learning/attribution/evaluate` - Compute multi-factor epistemic attribution.
- `GET /api/v1/learning/hypotheses/active` - List active hypotheses under evaluation.
- `GET /api/v1/learning/calibration/metrics` - Fetch Brier scores and calibration radar telemetry.
- `POST /api/v1/learning/promotion/promote` - Operator promotion of hypothesis to governed knowledge.
- `POST /api/v1/learning/promotion/rollback` - Instant cryptographic rollback of learned knowledge.
- `GET /api/v1/learning/drift/status` - View current environment drift & PSI alerts.

---

### 4. Explainability & Human-in-the-Loop Governance

Every recommendation rendered in the UI contains an expandable **Epistemic Trace**:
```json
{
  "recommendation_id": "REC-9081",
  "suggested_action": "Use Asymmetric Grid for Gen-Z Denim Campaign",
  "epistemic_trace": {
    "source_knowledge_id": "KNOW-DENIM-09",
    "empirical_evidence_count": 8,
    "confidence_score": 0.81,
    "decay_adjusted_freshness": 0.74,
    "confounder_disclaimer": "Observational correlation only. Influenced by TikTok seasonal trends.",
    "governance_approval": {
      "approved_by": "operator_sarah@ilyren.ai",
      "timestamp": "2026-09-08T14:30:00Z"
    }
  }
}
```

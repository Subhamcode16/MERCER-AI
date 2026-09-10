# INTELLIGENCE-EXPLAINABILITY-CONTRACT.md
## Phase 29 Architecture Specification: Intelligence Explainability Contract & Lineage Graph

---

### 1. Overview

Every strategic signal, hypothesis, and recommendation in Phase 29 provides an inspectable, mathematically complete **Epistemic Trace**.

$$\mathbf{Recommendation \longrightarrow Scenario \longrightarrow Signal \longrightarrow Hypothesis \longrightarrow Evidence \longrightarrow Campaign\ Decision}$$

---

### 2. Required Trace Fields

```json
{
  "recommendation_id": "REC-7890",
  "title": "Deploy Asymmetric Framing Capsule",
  "epistemic_trace": {
    "epistemic_status": "EXPERIMENTAL_EVIDENCE",
    "confidence_score": 0.82,
    "quality_audit": {
      "observational_cap_applied": false,
      "contradiction_ratio": 0.25,
      "assumptions_count": 2,
      "unknowns_count": 1
    },
    "supporting_evidence_nodes": [
      {
        "id": "SIG-8901",
        "type": "STRATEGIC_SIGNAL",
        "pattern": "Asymmetric visual framing lift (+16%)"
      },
      {
        "id": "EXP-ASYM-01",
        "type": "EXPERIMENT",
        "p_value": 0.018,
        "sample_size": 24000
      }
    ],
    "contradicting_evidence_nodes": [
      {
        "id": "SURVEY-TRAD-01",
        "type": "AUDIENCE_SURVEY",
        "note": "Traditional buyers prefer centered symmetric framing"
      }
    ],
    "human_review": {
      "challenged": true,
      "challenged_by": "elena_creative_lead",
      "resolution": "Scoped strictly to modern luxury capsule segment"
    }
  }
}
```

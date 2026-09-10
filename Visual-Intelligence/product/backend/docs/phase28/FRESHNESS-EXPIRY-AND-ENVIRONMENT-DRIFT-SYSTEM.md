# FRESHNESS-EXPIRY-AND-ENVIRONMENT-DRIFT-SYSTEM.md
## Phase 28 Architecture Specification: Freshness Expiry & Environment Drift Detection

---

### 1. Executive Overview

Learned marketing and visual knowledge degrades over time due to ad platform algorithm updates, consumer visual fatigue, macro-economic shifts, and seasonal dynamics. Under the core invariant:
$$\mathbf{Historical\ Record \neq Current\ Recommendation}$$

The `FreshnessEvaluator` and `EnvironmentDriftDetector` systems continuously monitor all active knowledge objects, applying automatic half-life decay, calculating freshness scores, and flagging environment distribution shifts with explicit confounder warnings.

---

### 2. Knowledge Freshness & Decay Dynamics

Knowledge freshness is modeled as an exponential decay function parameterized by domain volatility:

$$\text{Freshness}(t) = \text{InitialConfidence} \times e^{-\lambda (t - t_0)}$$

Where:
- $\lambda_{\text{fast-fashion}} = 0.05\ \text{day}^{-1}$ (Half-life ~ 14 days)
- $\lambda_{\text{luxury-heritage}} = 0.005\ \text{day}^{-1}$ (Half-life ~ 140 days)
- $\lambda_{\text{platform-ad-specs}} = 0.02\ \text{day}^{-1}$ (Half-life ~ 35 days)

```python
class FreshnessEvaluator:
    def evaluate_freshness(self, knowledge: GovernedKnowledgeObject, current_time: datetime) -> FreshnessReport:
        age_days = (current_time - knowledge.created_at).total_seconds() / 86400.0
        decay_rate = DOMAIN_DECAY_RATES.get(knowledge.domain, DEFAULT_DECAY_RATE)
        
        freshness_score = max(0.0, knowledge.confidence_score * math.exp(-decay_rate * age_days))
        is_expired = freshness_score < MIN_USABLE_FRESHNESS or age_days > MAX_LIFETIME_DAYS
        
        return FreshnessReport(
            knowledge_id=knowledge.id,
            age_days=age_days,
            freshness_score=freshness_score,
            is_expired=is_expired,
            recommendation="RECALIBRATE" if is_expired else "MAINTAIN"
        )
```

---

### 3. Environment Drift Detection

When external platform metrics or market benchmarks deviate significantly from baseline distributions, `EnvironmentDriftDetector` computes the Population Stability Index (PSI) or Wasserstein distance:

```
Baseline Campaign Distribution               Current Live Distribution
       (Mean CTR: 3.2%)                           (Mean CTR: 1.4%)
    [====|======|====]                         [==|===|==]
             \                                      /
              \---------> Drift PSI = 0.28 --------/
                                |
                   [ CONFOUNDER WARNING TRIGGERED ]
         "Confounder Warning: Drift detected in Meta Ad Platform CTR baseline.
          Historical conversion models are suspended pending recalibration."
```

```python
class EnvironmentDriftDetector:
    def detect_drift(self, baseline_distribution: List[float], current_distribution: List[float]) -> DriftAnalysis:
        psi = calculate_psi(baseline_distribution, current_distribution)
        drift_detected = psi > DRIFT_THRESHOLD_PSI
        
        warning_msg = None
        if drift_detected:
            warning_msg = f"Confounder Warning: Drift detected in environment telemetry (PSI={psi:.3f})."
            
        return DriftAnalysis(
            metric="conversion_rate",
            psi=psi,
            drift_detected=drift_detected,
            alert_message=warning_msg
        )
```

---

### 4. Automated Safety Controls

1. **Stale Knowledge Deprecation:** Expired knowledge is automatically flagged as `STALE` and excluded from top-tier generation prompts.
2. **Drift-Induced Quarantine:** If a high-drift alert is confirmed, dependent hypotheses transition to `QUARANTINED_PENDING_EXPERIMENT`.
3. **Audit Log Record:** Every state transition is recorded into the cryptographic ledger.

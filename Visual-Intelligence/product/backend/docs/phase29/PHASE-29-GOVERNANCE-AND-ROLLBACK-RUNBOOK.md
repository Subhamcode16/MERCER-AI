# PHASE-29-GOVERNANCE-AND-ROLLBACK-RUNBOOK.md
## Phase 29 Operational Runbook: Governance, Authorization & Instant Rollback

---

### 1. Operational Overview

This runbook outlines operational procedures for managing strategic signals, processing operator challenges, handling institutional knowledge promotions, and executing instant cryptographic rollbacks.

---

### 2. Standard Operating Procedures (SOP)

#### SOP 1: Reviewing and Challenging a Recommendation
1. Open the **Foresight Workspace**.
2. Select the proposed recommendation (`REC-...`).
3. Click **"Challenge Recommendation"**.
4. Enter operator dissent notes and attach any relevant market or brand equity counterevidence.
5. The `RecommendationQualityContract` automatically recalculates confidence and transitions the proposal to `DOWNGRADED`.

#### SOP 2: Authorizing Campaign Execution
1. Verify the operator possesses authorized role credentials (`STRATEGIC_OPERATOR`, `CAMPAIGN_DIRECTOR`, `ADMIN`).
2. Review the 12-stage recommendation structure, reversibility score, and proposed experiment.
3. Submit decision with explicit rationale.
4. The bridge provisions a campaign/experiment ID (`CAMP-...` or `EXP-...`) and records a `StrategicDecisionMemoryRecord`.

#### SOP 3: Instant Strategic Rollback
1. To withdraw an active signal, hypothesis, or recommendation:
2. Execute `StrategicRollbackManager.withdraw_recommendation(rec, operator_id, reason)`.
3. The object is deactivated (`is_active = False`) and transitions to `WITHDRAWN`.
4. Downstream generative systems immediately refuse citations of the withdrawn recommendation.
5. An immutable audit record (`AUD-...`) is permanently appended to `StrategicTelemetryEngine`.

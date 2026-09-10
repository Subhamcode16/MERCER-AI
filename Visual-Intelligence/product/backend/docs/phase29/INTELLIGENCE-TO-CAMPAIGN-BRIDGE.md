# INTELLIGENCE-TO-CAMPAIGN-BRIDGE.md
## Phase 29 Architecture Specification: Intelligence-to-Campaign Bridge

---

### 1. Overview

The **Intelligence-to-Campaign Bridge** enforces the strict human authorization gate between strategic recommendations and campaign execution.

Forbidden Architectural Flow:
$$\mathbf{Intelligence \longrightarrow Autonomous\ Campaign\ Launch\ (STRICTLY\ FORBIDDEN)}$$

Enforced Governed Flow:
$$\mathbf{Intelligence \longrightarrow Recommendation \longrightarrow Human\ Review \longrightarrow Decision \longrightarrow Campaign/Experiment}$$

---

### 2. Human Decision Contract

Every consequential decision records:
- `decision_id` & `tenant_id`
- `decision_maker` & `decision_maker_role` (`CAMPAIGN_DIRECTOR`, `STRATEGIC_OPERATOR`, `ADMIN`)
- `selected_recommendation_id` & `action_approved`
- `rejected_alternatives` & `accepted_assumptions`
- `operator_rationale`
- `resulting_campaign_id` or `resulting_experiment_id`
- `dissent_or_uncertainty_notes`

# Phase 28: Decision Ledger & Provenance Specification

## 1. Decision Ledger Schema
Every material campaign decision is recorded immutably:
- `decision_id`: Unique identifier.
- `campaign_id`: Campaign context binding.
- `decision_type`: `AUDIENCE_SELECTION`, `CREATIVE_TERRITORY`, `VISUAL_DIRECTION`, `CHANNEL_SELECTION`, `COPY_DIRECTION`, `ASSET_VARIANT`, `LAUNCH_TIMING`, `TOKEN_LOCK`, `MODEL_SELECTION`.
- `decision_version`: Sequential 1-indexed version.
- `actor_id`: Authenticated operator who authorized the decision.
- `context_snapshot`: Complete brand guideline and market state snapshot.
- `decision`: Concrete choice selected.
- `rationale`: Detailed strategic reasoning.
- `alternatives`: Rejected alternatives with rejection rationale and risk estimates.
- `assumptions` & `unknowns`: Explicit uncertainties preserved.
- `parent_hash` & `record_hash`: SHA-256 cryptographic chain.

## 2. Cryptographic Immutability Formula
For decision $i$:

$$H_i = \mathrm{SHA256}\Big(\mathrm{CanonicalJSON}\big(D_i, C_i, T_i, V_i, H(P_i), \text{Decision}_i, \text{Rationale}_i, S_i\big)\Big)$$

If any historical record is modified, `verify_ledger_integrity()` fails immediately.

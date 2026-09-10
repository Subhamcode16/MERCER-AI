# HELD-OUT-AND-MUTATION-VALIDATION.md
## Phase 29 Validation Report: Held-Out Evaluation & Mutation Testing

---

### 1. Held-Out Evaluation on Unseen Evidence

To prevent overfitting to known test scenarios, Phase 29 includes a dedicated held-out evaluation suite validating 5 dimensions:

1. **Evidence Fidelity:** Evaluates signal generation against unseen regional campaign data (`HELD-OUT-EV-0` through `9`), preserving exact sample counts and confidence parameters.
2. **Contradiction Preservation:** When unseen counterevidence outnumbers supporting observations, the system consistently transitions recommendations to `DOWNGRADED`.
3. **Uncertainty Calibration:** Validates that unseen complex inquiries preserve the `UNKNOWN` scenario archetype with uncertainty $\ge 0.90$.
4. **Tenant Isolation Barrier:** Asserts that held-out foreign tenants cannot access private knowledge claims.
5. **Human Authority Boundary:** Validates that held-out recommendations require explicit human decision records before creating downstream campaigns.

---

### 2. Mutation Testing Report

Deliberate fault-injection and invariant mutations were executed against the codebase:

| Mutation Tested | Expected Response | Observed Result | Status |
| :--- | :--- | :--- | :--- |
| Direct cross-tenant boundary breach | `GovernanceViolation` raised | Blocked fail-closed | **PASS** |
| Empty `unknowns` passed to signal engine | Automatic repair / population | Unknowns preserved | **PASS** |
| Unauthorized role approving campaign | `PermissionError` raised | Blocked fail-closed | **PASS** |
| Execution attempt on `WITHDRAWN` recommendation | `ValueError` raised | Blocked fail-closed | **PASS** |
| Malicious prompt injection in external blog | Directives stripped to `[STRIPPED_DIRECTIVE]` | Neutralized | **PASS** |

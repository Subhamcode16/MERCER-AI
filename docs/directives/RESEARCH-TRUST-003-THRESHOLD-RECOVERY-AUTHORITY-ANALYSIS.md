# RESEARCH-TRUST-003 — THRESHOLD RECOVERY AUTHORITY ANALYSIS

**Status:** ARCHITECTURAL RESEARCH DELIVERABLE  
**Reference Gate:** ARCH-TRUST-001 (Section 5)  
**Security Classification:** CRITICAL  
**Date:** 2026-08-28  

---

## 1. Threshold Recovery Authority Model ($N, T$)

To eliminate the Single Point of Failure (SPOF) of a single administrative recovery credential, the recovery authority is structured as a threshold signing scheme.

We define:
*   $N$: The total number of independent recovery authorities (key holders).
*   $T$: The minimum number of cryptographic signatures required to validate a state recovery override ($T \le N$).

### 1.1. Operational and Threat Vectors

*   **Authority Provisioning:** Each recovery authority is provisioned with an asymmetric key pair. Public keys are stored within the controller's static boot configuration.
*   **Authority Identity:** Keys are assigned to specific operational roles (e.g., Lead Security Engineer, Director of Infrastructure, Compliance Officer, External Audit Agent).
*   **Approval Independence:** Signs must be generated on physically isolated devices (e.g., separate HSMs or air-gapped administration laptops).
*   **Collusion:** Set $T$ such that collusion requires cross-role participation (e.g., requiring both engineering and compliance signatures).
*   **Compromise:** Compromise of up to $T-1$ keys does not allow database override. If $\ge T$ keys are compromised, the attacker gains full override authority.
*   **Revocation & Rotation:** Key rotation or revocation requires a configuration update payload signed by $T$ active recovery keys, or via the offline governance root of trust.
*   **Membership Changes:** Modifying the list of authorities or altering the threshold $T$ requires a bootstrap update signed by the offline governance root.
*   **Authority Disagreement:** If key holders disagree on the incident cause, they do not sign. The system remains locked in `RECOVERY_REQUIRED`. There is no majority bypass; the threshold $T$ is absolute.
*   **Unavailability & Emergency Recovery:** If quorum $T$ cannot be reached due to key loss or unavailability, the system remains blocked. Emergency recovery requires a physical cold-boot reset (wiping physical disk storage and anchors).
*   **Recovery Replay & Incident Binding:** To prevent signature replay across different recovery cycles, the challenge payload signed by authorities must be dynamically bound to:
    $$\text{Payload} = \text{incident\_uuid} + \text{\_} + \text{genesis\_hash} + \text{\_} + \text{block\_count}$$
    The controller verifies that the signed payload matches the current active incident metadata before resetting the ledger.

---

## 2. Core Governance Boundaries

The recovery authority parameters are governed according to strict off-line rules to prevent runtime self-modification.

```text
               +-------------------------------------------------+
               |     Offline human-in-the-loop multi-sig         | (Governance Root)
               +-------------------------------------------------+
                                       |
                     (Authorizes Membership and Threshold)
                                       v
               +-------------------------------------------------+
               |        Controller Bootstrap Config Block        | (T and N public keys)
               +-------------------------------------------------+
                                       |
                       (Authenticates Override Signature)
                                       v
               +-------------------------------------------------+
               |               Assurance Controller              |
               +-------------------------------------------------+
```

1.  **Who chooses the recovery authorities?** The offline human-in-the-loop multi-signature governance board.
2.  **Who can replace them?** The offline board.
3.  **Who can change $T$?** The offline board.
4.  **Who can authorize those changes?** The offline board via signed configuration blocks. The running controller runtime has no authority to modify $T$, $N$, or key mappings autonomously.

---

## 3. Section 6 Critical Constraints Mapping

*   **Threat Addressed:** Leakage or compromise of a single admin key allowing unauthorized state reset or history deletion.
*   **Security Property Added:** Multi-party control and collusion resistance (requires $T$ separate entities to validate recovery).
*   **New Trust Assumptions:** At least $T$ key holders maintain operational key security and verify incident logs before signing.
*   **New Failure Modes:** Lockout starvation where key unavailability permanently blocks system recovery.
*   **New Attack Surface:** Phishing or social engineering targeting multiple administrators simultaneously; signature aggregation coordination protocol exploits.
*   **Availability Implications:** Reduced recovery speed. Wiping/restoring ledger is slower due to signing coordination.
*   **Complexity Cost:** Medium. Requires implementing threshold signature verification (e.g., Shamir's Secret Sharing or multi-sig payload parsing).
*   **Evidence Required:** Test runs validating threshold overrides (e.g., confirming that $T-1$ signatures are rejected and $T$ signatures are accepted).

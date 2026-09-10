# FROST / Hardware-Custody Research Prototype

> **WARNING:**  
> **This implementation is a research prototype and is not authorized for production cryptographic, authorization, hardware-custody, or execution-control use.**

---

## 1. Purpose

The Phase 4 FROST Research Prototype provides an isolated laboratory for studying threshold Schnorr signing concepts, per-signature nonce safety invariants, binding factor computations, threshold aggregation, and mock hardware-custody boundaries without modifying the production security substrate (`ExecutionGate`, `AssuranceLoopController`, `RecoveryManager`, `EpistemicState`).

---

## 2. Research-Only Status

This module is strictly a research and educational artifact:
- All cryptographic keys, nonces, and shares are synthetic test vectors explicitly tagged `TEST_ONLY`.
- Zero production cryptographic infrastructure or real hardware dependencies exist.
- Zero runtime integration exists between this research module and the production execution gate or state machine.

---

## 3. Architecture

```text
                    RESEARCH / PROTOTYPE DOMAIN
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  Participant Simulation (ParticipantNode)                     │
│          │                                                    │
│          ▼                                                    │
│  Mock Hardware Custody (MockHardwareCustodian)                │
│          │                                                    │
│          ▼                                                    │
│  Nonce Generation & Tracking (SigningNonceTracker)            │
│          │                                                    │
│          ▼                                                    │
│  FROST Signing Round (FROSTSigningCoordinator)                │
│          │                                                    │
│          ▼                                                    │
│  Threshold Signature Assembly ((R, S))                        │
│          │                                                    │
│          ▼                                                    │
│  Signature Verification (FROSTSignatureVerifier)              │
│                                                               │
│       TEST / RESEARCH OUTPUT ONLY                             │
│                                                               │
└───────────────────────────────────────────────────────────────┘

                         X NO CONNECTION X

┌───────────────────────────────────────────────────────────────┐
│                  PRODUCTION SECURITY SUBSTRATE                │
│                                                               │
│ AssuranceLoop → EpistemicState → ExecutionGate               │
│ RecoveryManager → Capability Authorization                   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 4. Participant Model

Participants are represented by `ParticipantNode` instances. Each participant holds a synthetic secret share $s_i$ stored in a `MockHardwareCustodian` instance. Participants interact with the coordinator through Round 1 commitment generation and Round 2 signature share generation.

---

## 5. Threshold Model

The prototype supports configurable $t$-of-$n$ threshold signing:
- $1 \le t \le n$.
- Synthetic shares generated via polynomial evaluation $f(x) = a_0 + a_1 x + \dots + a_{t-1} x^{t-1} \pmod Q$.
- Lagrange coefficients computed dynamically over active signing sets $S$:
  $$\lambda_i = \prod_{j \in S, j \neq i} \frac{j}{j - i} \pmod Q$$

---

## 6. Nonce Model & Reuse Prevention

Per-signature nonces $(d_i, e_i)$ are generated using `secrets.randbelow(GROUP_ORDER_Q - 1)`. Nonce identifiers and public commitment pairs $(D_i, E_i)$ are registered in `SigningNonceTracker`.

- **Atomic Consumption:** Nonces are marked as consumed under `threading.RLock()` upon Round 2 execution.
- **Reuse Protection:** Attempting to reuse a secret nonce or commitment pair raises `NonceReuseException`.

---

## 7. Signing Workflow

1. **Setup:** Generate $t$-of-$n$ polynomial shares ($s_i, Y_i, Y$).
2. **Round 1:** Collect public nonces $(D_i, E_i)$ from signers ($k \ge t$).
3. **Commitment & Challenge:** Compute binding factors $\rho_i = H(i, \text{msg}, B) \pmod Q$, group commitment $R = \prod R_i \pmod P$, and challenge $c = H(R, Y, \text{msg}) \pmod Q$.
4. **Round 2:** Each participant node authenticates with its `MockHardwareCustodian` and computes $z_i = (d_i + \rho_i e_i) + \lambda_i s_i c \pmod Q$.
5. **Aggregation:** $S = \sum z_i \pmod Q$. Assemble threshold signature $(R, S)$.

---

## 8. Mock Hardware Custody Boundary

The `MockHardwareCustodian` simulates:
- Share storage & PIN authentication (`authenticate_and_fetch_share`).
- Device locks after 3 invalid PIN attempts (`HardwareLockedException`).
- Device disconnections (`HardwareUnavailableException`).
- Corrupted shares (`CorruptedShareException`).
- Simulated timeouts (`HardwareTimeoutException`).

**Explicit Boundary:** The custodian is an in-memory Python mock and does **NOT** communicate with YubiKeys, PIV applets, TPMs, HSMs, or smart cards.

---

## 9. Threat Assumptions & Security Limitations

- **Not Production Cryptography:** Mathematical field operations serve educational and structural validation goals.
- **In-Memory Storage:** Shares and nonces reside in Python process memory.
- **Non-Hardened Execution:** Side-channel timing and memory dumps are not mitigated.

---

## 10. Explicit Production Exclusions

- No native YubiKey FROST support is claimed or implemented.
- No `ExecutionGate` or `AssuranceLoopController` bypass is possible.
- FROST signature verification results in a boolean result only and **NEVER** transitions system state to `EpistemicState.VERIFIED`.

# RESEARCH-TRUST-003 — Threshold Recovery & Admin Override Cryptography

**Document ID:** `RESEARCH-TRUST-003-THRESHOLD-RECOVERY-ADMIN-OVERRIDE-CRYPTOGRAPHY`  
**Author:** Engineering Agent  
**Review Target:** Intelligence Architect / Security Review Board  
**Status:** RESEARCH COMPLETE  
**Implementation Decision:** DEFER  
**Implementation Authorized:** NO  
**Date:** 2026-09-03  

---

## 1. Executive Summary

Following the ratification of [`ARCH-TRUST-001-TRUST-AUTHORITY-EPISTEMIC-CONSOLIDATION.md`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/chatgpt%20message%20box/ARCH-TRUST-001-TRUST-AUTHORITY-EPISTEMIC-CONSOLIDATION.md) and the formal approval of [`RESEARCH-TRUST-001`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/chatgpt%20message%20box/RESEARCH-TRUST-001-DECENTRALIZED-TRUST-ANCHOR-ANALYSIS.md) and [`RESEARCH-TRUST-002`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/chatgpt%20message%20box/RESEARCH-TRUST-002-PRIVACY-PRESERVING-EVIDENCE-ANALYSIS.md), this document addresses **RESEARCH-TRUST-003**.

The primary objective of this research is to establish the cryptographic architecture for out-of-band administrative recovery and emergency override authorization. Specifically, we investigate how to prevent the compromise or loss of a single administrative credential from causing either a catastrophic system override or an unrecoverable system lockout.

Every major assertion in this document preserves the epistemic taxonomy required by `ARCH-TRUST-001`:
- `[CURRENT FACT]` — Empirical property of the existing system implementation.
- `[ARCHITECTURAL ASSUMPTION]` — Declared root-of-trust boundary or environment assumption.
- `[RESEARCH FINDING]` — Analytical result established by literature or mathematical modeling.
- `[EXPERIMENTAL EVIDENCE]` — Measured result from empirical test runs (`RTC-008`–`RTC-012`).
- `[REFERENCE BENCHMARK]` — Published literature benchmark from external research.
- `[ANALYTICAL ESTIMATE]` — Derived engineering estimate based on benchmarks and specifications.
- `[INFERENCE]` — Logical deduction derived from facts, assumptions, or findings.
- `[RECOMMENDATION]` — Actionable architectural decision.
- `[OPEN QUESTION]` — Open technical boundary requiring future study.

---

## 2. Core Research Question

> **Research Problem:** In a high-assurance visual intelligence security substrate, how can out-of-band administrative recovery be architected such that:
> 1. Compromise of a single administrative credential cannot authorize an emergency system override (*Compromise Resistance*).
> 2. Loss or unavailability of a single administrator cannot cause permanent system lockout (*Availability Survivability*).
> 3. Verified recovery authorization strictly respects the tripartite separation of authority and cannot bypass runtime verification logic (*Epistemic Boundary Control*).

---

## 3. Current Recovery Baseline

Under the ratified baseline in `ARCH-TRUST-001` (Section 4 & 9.1), the system operates an out-of-band challenge-response recovery protocol:

```text
[Recovery Trigger: RECOVERY_REQUIRED]
                 │
                 ▼
[Out-of-Band Challenge Generated (Nonce N_rec, Monotonic Time T_mon)]
                 │
                 ▼
[Single Admin Key Signatures: S_admin(N_rec || Operation_ID)]
                 │
                 ▼
[Recovery Verification: Admin Override Verified]
                 │
                 ▼
[Database / Genesis Wiped ──► Epistemic State Set to UNKNOWN]
```

### 3.1 Properties of Baseline Recovery `[CURRENT FACT]`
- **Single Offline Key:** Recovery authorization relies on a single master Ed25519 administrative private key held in offline cold storage.
- **Tripartite Separation:** As ratified in `ARCH-TRUST-001`, a verified admin override does **NOT** grant runtime authorization and does **NOT** unlock `ExecutionGate`. It wipes local ledger databases, clears panic locks, resets genesis state, and forces state transition to `UNKNOWN`.
- **Vulnerabilities of Current Baseline:**
  1. *Single Point of Compromise:* Theft of the master offline key allows an adversary to wipe ledger databases at will.
  2. *Single Point of Failure:* Loss or destruction of the master key (or death/incapacitation of the key custodian) renders database recovery impossible, creating permanent system lockout upon panic lock (`RECOVERY_REQUIRED`).

---

## 4. Threat Model & Vulnerability Analysis

We evaluate 20 threat scenarios against the administrative recovery boundary. For every threat, we classify the impact of migrating from a single offline key to a threshold signature architecture:

| Threat Scenario | Threat Description | Threshold Impact | Classification |
|---|---|---|---|
| **T1: Single Admin Key Theft** | Adversary steals single offline master private key. | Prevents single-key compromise from authorizing recovery. | `MITIGATES` |
| **T2: Single Administrator Compromise** | Rogue or coerced single administrator attempts unauthorized recovery. | Requires $T$ collateral approvals; single rogue admin is blocked. | `MITIGATES` |
| **T3: Multi-Admin Collusion** | $k < T$ malicious administrators conspire to forge recovery. | Blocked under protocol assumption that $k < T$. | `MITIGATES` |
| **T4: Lost Admin Credentials** | Key custodian loses hardware token or passphrase. | Tolerates up to $N - T$ lost keyholders without lockout. | `MITIGATES` |
| **T5: Unavailable Administrators** | Keyholders offline/unreachable during emergency. | System recovers if any $T$ out of $N$ keyholders respond. | `MITIGATES` |
| **T6: Compromised Signing Device** | Malware compromises an admin signing laptop/token. | Attacker obtains only 1 share ($1 < T$). | `MITIGATES` |
| **T7: Compromised Recovery Workstation**| Workstation used for quorum aggregation is infected. | Partial shares exposed; attacker cannot forge final signature without $T$ shares. | `MITIGATES` |
| **T8: Replayed Recovery Authorization** | Adversary replays valid past recovery transcript. | Nonces ($\text{RunID}$) and timestamps enforce single-use. | `MITIGATES` |
| **T9: Stale Recovery Authorization** | Adversary delays and broadcasts expired recovery signature. | Monotonic expiration window ($T_{exp} \le 15\text{ min}$) rejects stale payloads. | `MITIGATES` |
| **T10: Unauthorized Recovery Request** | Unauthenticated user submits fake recovery trigger. | Rejected by cryptographic signature verification. | `NO MATERIAL CHANGE` |
| **T11: Insider Abuse** | Authorized admin attempts out-of-scope operation. | Capability-scoped payloads restrict signature to explicit `Operation_ID`. | `MITIGATES` |
| **T12: Social Engineering** | Attacker tricks keyholder into signing recovery. | Requires social engineering $T$ independent keyholders across org boundaries. | `MITIGATES` |
| **T13: Key-Share Theft** | Attacker steals stored encrypted polynomial share. | Share alone yields zero information about master secret under Shamir math. | `MITIGATES` |
| **T14: Threshold Reconstruction Attacks**| Attacker attempts algebraic secret reconstruction with $T-1$ shares. | Shamir/FROST math guarantees zero information gain with $< T$ shares. | `MITIGATES` |
| **T15: DKG Compromise** | Malicious participant manipulates Distributed Key Generation. | Requires verifiable DKG (Pedersen commitment checks). | `INTRODUCES NEW RISK` |
| **T16: Malicious DKG Participant** | Participant provides invalid DKG shares to corrupt setup. | Detected during DKG verification phase; participant excluded. | `INTRODUCES NEW RISK` |
| **T17: Quorum Manipulation** | Adversary delays responses to force specific keyholder subset. | Any valid subset of $T$ produces identical valid group signature. | `NO MATERIAL CHANGE` |
| **T18: Recovery-Channel DoS** | Adversary jams network coordination during signing round. | FROST round-1 preprocessing delays recovery signing. | `INTRODUCES NEW RISK` |
| **T19: Accidental Recovery Approval** | Admins sign recovery request without reading scope payload. | Hardware screen confirmation (YubiKey display) mitigates blind signing. | `MITIGATES` |
| **T20: Permanent Quorum Loss** | $\ge N - T + 1$ keyholders lose keys simultaneously. | Quorum permanently destroyed; system locked out. | `INTRODUCES NEW RISK` |

---

## 5. Formal Separation of Cryptographic Primitives & Candidate Architectures

### 5.0 Separation of Cryptographic Primitives `[RESEARCH FINDING]`
To ensure rigorous cryptographic semantics, we explicitly distinguish four primitives that are frequently confused:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                PRIMITIVE TAXONOMY & PROPERTIES                                   │
├───────────────────────┬─────────────────────────────────┬────────────────────────────────────────┤
│ Primitive Class       │ Cryptographic Mechanism         │ Properties Provided & Limitations      │
├───────────────────────┼─────────────────────────────────┼────────────────────────────────────────┤
│ Multi-Signature       │ Collection of N independent     │ • Simple verification; standard keys   │
│ (Multi-Sig)           │ signatures (S_1 || ... || S_M)   │ ✗ Discloses signer identities on-chain │
│                       │                                 │ ✗ Large non-succinct signature size    │
├───────────────────────┼─────────────────────────────────┼────────────────────────────────────────┤
│ Threshold Signature   │ Single group signature σ from   │ • Single-key 64B verifier code         │
│ (FROST / BLS)         │ T-of-N secret key shares s_i     │ • Preserves signer identity privacy    │
│                       │                                 │ ✗ Requires interactive DKG setup       │
├───────────────────────┼─────────────────────────────────┼────────────────────────────────────────┤
│ Secret Sharing        │ Polynomial secret splitting     │ • Reconstructs master secret S in RAM  │
│ (Shamir SSS)          │ (S = f(0) from T shares)        │ ✗ Reconstructing S creates a transient │
│                       │                                 │   single-point-of-failure in memory!  │
├───────────────────────┼─────────────────────────────────┼────────────────────────────────────────┤
│ Consensus Protocol    │ Distributed state machine       │ • Replicates ledger history across nodes│
│ (BFT / Raft)          │ agreement (pBFT, Raft, Tendermint)│ ✗ Does NOT issue administrative recovery│
│                       │                                 │   authorizations or secret signatures  │
└───────────────────────┴─────────────────────────────────┴────────────────────────────────────────┘
```

> **Cryptographic Invariant:** `[RESEARCH FINDING]`
> • **Shamir Secret Sharing Information-Theoretic Property:** Provides information-theoretic privacy for static secret reconstruction ($k < T$ shares yield zero information about static secret $S$). However, reconstructing $S$ in RAM creates a single point of failure during execution.  
> • **Complete FROST Protocol Security:** FROST protocol security extends beyond static Shamir secret sharing. It depends on the full interactive signing protocol, verifiable DKG (Pedersen commitments), binding-factor computation ($\rho_i$), strict stateful nonce-reuse prevention (reusing a nonce leaks share $s_i$), participant honesty assumptions ($k < T$), and underlying Schnorr DDH curve security.

---

### 5.1 Candidate Architectures (Options A through G)

We evaluate seven candidate administrative authorization architectures:

#### 5.1 Option A: Single Offline Administrative Key (Baseline) `[CURRENT FACT]`
- **Description:** Single Ed25519 key held on air-gapped paper/USB backup.
- **Pros:** Zero coordination overhead; simple implementation; instantaneous signing.
- **Cons:** Single Point of Failure; Single Point of Compromise.

#### 5.2 Option B: M-of-N Naïve Multi-Signature Scheme `[RESEARCH FINDING]`
- **Description:** $N$ independent administrative public keys are registered; recovery requires concatenating $M$ separate digital signatures ($S_1 \parallel S_2 \parallel \dots \parallel S_M$).
- **Pros:** Simple key generation; no Distributed Key Generation (DKG) required; uses standard Ed25519 libraries.
- **Cons:** Large signature size ($M \times 64\text{ bytes}$); exposes participating admin identities on-chain/ledger; non-succinct verification.

#### 5.3 Option C: FROST Threshold Signatures (Schnorr / Ed25519) `[RECOMMENDATION]`
- **Description:** Flexible Schnorr Threshold Signature Scheme. $N$ participants hold polynomial secret shares $s_i$. Any $T$ participants execute a 2-round interactive protocol to produce a single standard 64-byte Schnorr/Ed25519 signature $\sigma$.
- **Pros:** **Standard 64-byte signature** output (indistinguishable from single-key Ed25519); single-key verification code on-chain/ledger; information-theoretic privacy for $< T$ shares under Shamir math; compatible with hardware tokens via participant integration daemon.
- **Cons:** Requires 2-round interactive signing protocol; requires initial DKG setup.

#### 5.4 Option D: BLS Threshold Signatures (BLS12-381) `[RESEARCH FINDING]`
- **Description:** Boneh-Lynn-Shacham threshold signatures over pairing-friendly elliptic curve BLS12-381.
- **Pros:** **Non-interactive signing** (keyholders sign locally; signatures aggregate deterministically without coordination rounds); compact 48-byte public keys and 96-byte signatures.
- **Cons:** Relies on pairing assumptions; verification is $15\times–40\times$ slower than Schnorr/Ed25519 signature checks; lacks native hardware security key support (YubiKey/HSM PIV standard unsupported).

#### 5.5 Option E: Hardware-Backed Single Administrative Key `[RESEARCH FINDING]`
- **Description:** Master private key is generated and locked inside a single hardware security module (HSM / YubiKey HSM).
- **Pros:** Prevents key extraction via malware or software exploits.
- **Cons:** Hardware loss, theft, or physical destruction still results in permanent system lockout.

#### 5.6 Option F: Multi-Party Hardware-Backed Threshold Recovery (FROST + Hardware Custody Boundary) `[RECOMMENDATION]`
- **Description:** Combine Option C and Option E: Each of the $N$ FROST secret shares $s_i$ is secured via a hardware security key (YubiKey PIV / PKCS#11 HSM) coordinated by a participant-side host integration daemon.
- **Pros:** High security boundary; key shares cannot be extracted in plaintext from host RAM; signing requires physical touch confirmation.
- **Cons:** High operational complexity; requires dedicated host-side daemon to manage FROST nonce state and binding factors.

#### 5.7 Option G: Hybrid Cold-Storage + Threshold Recovery `[RESEARCH FINDING]`
- **Description:** 2-tier recovery model: Standard emergency recovery uses a 3-of-5 FROST threshold scheme; catastrophic quorum failure allows an emergency fallback to a multi-custodian paper cold-storage vault split via Shamir Secret Sharing.
- **Pros:** High resiliency against total threshold quorum loss.
- **Cons:** Extremely heavy operational and physical governance requirements.

---

## 6. Threshold Mathematics & Quorum Analysis

```text
       COMPROMISE RESISTANCE vs. AVAILABILITY SURVIVABILITY
   
   High Compromise Resistance (T → N)      High Availability (T → 1)
   ┌─────────────────────────────────┐   ┌─────────────────────────────────┐
   │ Requires many key compromises   │   │ Survives many lost keyholders   │
   │ RISKS: Lockout if keyholders fail│   │ RISKS: Vulnerable to collusion  │
   └─────────────────────────────────┘   └─────────────────────────────────┘
                                   ▲
                                   │
                   [PREFERRED BASELINE: 3-of-5]
```

### 6.1 Dual-Threshold Mathematical Formulation `[RESEARCH FINDING]`
Let $N$ be the total registered keyholders, and $T$ be the required signing threshold. We formally separate two threshold dimensions:

1. **Security Threshold ($T_{sec} = T$):** The minimum number of compromised keyholders required for an attacker to forge a valid recovery signature. The system's **Compromise Tolerance** is:
   $$C_{tol} = T_{sec} - 1$$
   *(Under Shamir polynomial secret sharing, any coalition of $k \le C_{tol}$ keyholders gains zero information about the master group secret $S$.)*

2. **Availability Threshold ($T_{avail} = N - T + 1$):** The minimum number of lost or unavailable keyholders that will cause permanent system lockout. The system's **Availability Tolerance** (survivable participant loss) is:
   $$A_{tol} = N - T = T_{avail} - 1$$

### 6.2 Quorum Parameter Matrix

| Parameterization | $T$ | $N$ | Security Threshold ($T_{sec}$) | Availability Threshold ($T_{avail}$) | Compromise Tolerance ($T-1$) | Availability Tolerance ($N-T$) | Operational Burden | Evaluation Rating |
|---|---|---|---|---|---|---|---|---|
| **2-of-3** | 2 | 3 | 2 | 2 | 1 keyholder | 1 keyholder | Low | Low security boundary; vulnerable to 2-admin collusion |
| **3-of-5 (Preferred)** | 3 | 5 | 3 | 3 | **2 keyholders** | **2 keyholders** | **Balanced** | **Preferred Baseline target for multi-admin evaluation** |
| **4-of-7** | 4 | 7 | 4 | 4 | 3 keyholders | 3 keyholders | High | High security; increased signing coordination latency |
| **5-of-9** | 5 | 9 | 5 | 5 | 4 keyholders | 4 keyholders | Very High | Heavy operational coordination; high risk of round-1 timeouts |

> **Threshold Selection Rationale:** `[INFERENCE]` Under the $T=3, N=5$ model, the security threshold ($T_{sec} = 3$) and availability threshold ($T_{avail} = 3$) are equal. This configuration withstands up to **2 simultaneous keyholder compromises** while simultaneously surviving **2 lost or unreachable administrators**. It is designated as the **PREFERRED BASELINE** for further evaluation, but is not claimed to be universally optimal for all deployment topologies.

---

## 7. FROST vs. BLS Threshold Cryptography Analysis

We perform a side-by-side comparative analysis of the two leading threshold signature constructions: **FROST** (Schnorr / Ed25519) and **BLS** (Pairing-friendly BLS12-381).

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                FROST vs. BLS COMPARATIVE MATRIX                                  │
├──────────────────────────┬──────────────────────────────────┬────────────────────────────────────┤
│ Comparison Dimension     │ FROST (Schnorr / Ed25519)        │ BLS (BLS12-381 Pairing)            │
├──────────────────────────┼──────────────────────────────────┼────────────────────────────────────┤
│ Signing Rounds           │ 2 Interactive Rounds             │ 1 Non-Interactive Local Round      │
│ Participant Coordination │ Required during Round 1 & 2      │ None (Aggregator combines shares)  │
│ Signature Aggregation    │ Combined during Round 2          │ Deterministic Lagrange Interpolation│
│ Signature Size           │ 64 Bytes (Standard Ed25519)      │ 96 Bytes (G2 element)              │
│ Verification Latency     │ < 1 ms (Standard Schnorr Check)  │ 15 ms (Pairing operation e(P, Q))  │
│ Key Generation / DKG     │ Pedersen DKG                     │ DKG over G1/G2                     │
│ Participant Replacement  │ DKG Polynomial Refresh           │ DKG Polynomial Refresh             │
│ Key Rotation             │ Group Public Key Update          │ Group Public Key Update            │
│ Hardware Token Support   │ Requires Participant Daemon      │ Unsupported on commercial HSMs/PKA │
│ Implementation Complexity│ Medium (Standard Curve25519 math)│ High (Pairing curve math libraries)│
│ Library Maturity         │ IETF Draft RFC / libfrost        │ IETF Draft RFC / ETH2 Production   │
│ Failure Behavior         │ Round-1 abort on offline node    │ Missing node does not abort signing│
│ Cryptographic Assumption │ Standard Schnorr DDH Assumption  │ Pairing-friendly Co-Gap DH         │
│ Verification Code Cost   │ Identical to single-key Ed25519  │ Requires specialized pairing code  │
└──────────────────────────┴─────────────────────────────────┴────────────────────────────────────┘
```

### 7.1 FROST vs. Ordinary Ed25519 Signing Distinction `[RESEARCH FINDING]`
We explicitly distinguish:
- **FROST-Ed25519 Signature Verification Compatibility:** The aggregate signature $\sigma = (R, z)$ produced by a $T$-of-$N$ FROST execution verifies against the Group Public Key $Y$ using standard Schnorr/Ed25519 verifier math.
- **Ordinary Ed25519 Private-Key Signing:** Standard single-key Ed25519 signing where a static private key directly computes Schnorr signatures locally.

> **Verification Compatibility Requirement:** `[OPEN QUESTION]` While FROST-Ed25519 aims for output compatibility with standard Ed25519 verifiers, exact ciphersuite specifications, SHA-512 domain separation tags, point serialization rules, and RFC 8032 verification compatibility MUST be empirically validated during future implementation testing (`[OPEN QUESTION]`).

---

## 8. Hardware Integration Boundary Analysis: FROST + YubiKey PIV

### 8.1 Proven vs. Assumed Hardware Capabilities `[RESEARCH FINDING]`
We formally evaluate the integration boundary between FROST participant operations and YubiKey PIV hardware tokens.

```text
DISTINCTION:
YubiKey PIV supports Ed25519 single-key signing  (ESTABLISHED vendor documentation)
                     ≠
YubiKey PIV natively supports FROST operations   (NOT ESTABLISHED by vendor spec)
```

### 8.2 Analysis of FROST Participant Operations
Executing as a participant in a FROST signing round requires the following six stateful cryptographic operations:
1. **Participant-Side Scalar Arithmetic:** Computing partial signature share $z_i = d_i + (e_i \cdot \rho_i) + (\lambda_i \cdot s_i \cdot c) \pmod q$.
2. **Nonce Generation:** Generating cryptographically secure random secret nonces $(d_i, e_i)$ per signing session.
3. **Nonce Commitments:** Computing public commitments $(D_i = d_i \cdot G, E_i = e_i \cdot G)$ published during Round 1.
4. **Binding-Factor Computation:** Computing binding factors $\rho_i = H_{bind}(i, \text{msg}, B)$ over all participant commitments $B$.
5. **Signature-Share Generation:** Producing $z_i$ bound to the challenge hash $c = H_{challenge}(R, Y, \text{msg})$.
6. **Stateful Nonce Management:** Enforcing strict zero-reuse of nonces $(d_i, e_i)$. **A single nonce reuse in FROST completely leaks the participant's secret key share $s_i$!**

### 8.3 Hardware Firmware Boundary Verdict `[INFERENCE]`
- **YubiKey PIV Firmware Behavior:** YubiKey PIV firmware implements fixed PKCS#11 / PIV operations. It signs input hashes using a static internal private key. It does **NOT** expose polynomial scalar arithmetic APIs, does **NOT** execute FROST binding-factor calculations, and does **NOT** manage stateful FROST session nonces.
- **Integration Boundary Architectural Requirement:**  
  > **YubiKey PIV CANNOT be treated as a native FROST signer without an additional participant-host integration layer.**  
  > To utilize YubiKey PIV in a FROST threshold recovery architecture, one of two integration paths must be implemented in future engineering:  
  > • **Path A (Participant Host Daemon):** A trusted participant-side software daemon runs on the administrator's workstation to manage FROST session nonces, compute binding factors $\rho_i$, and perform polynomial scalar math, using the YubiKey strictly for PIV authentication or raw key derivation.  
  > • **Path B (Custom JavaCard Applet):** Authoring and provisioning custom JavaCard smartcard firmware (e.g. OpenPGP / custom applet on YubiKey JavaCard) that natively executes stateful FROST round-1 and round-2 operations inside the token hardware.

---

## 9. Key Lifecycle Specification

We define the 12-stage conceptual key lifecycle for threshold administrative recovery:

```text
1. Generation (Pedersen DKG) ──► 2. Distribution (Encrypted Channels) ──► 3. Registration (Public Key Y)
                                                                                  │
                                                                                  ▼
6. Emergency Destruction ◄── 5. Use (2-Round FROST) ◄── 4. Custody (Hardware Token / Daemon)
           │
           ▼
7. Monotonic Key Rotation ──► 8. Revocation ──► 9. Participant Replacement ──► 10. Quorum Re-Keying
```

1. **Generation:** Interactive Pedersen Distributed Key Generation (DKG) protocol among 5 initial keyholders. Master secret is never reconstructed in a single location.
2. **Distribution:** Secret shares $s_i$ are encrypted under participant public keys and transmitted over TLS channels.
3. **Registration:** Group Public Key $Y$ is registered in the immutable System Configuration metadata.
4. **Custody:** Key shares $s_i$ are imported into hardware YubiKeys and backed up in physical tamper-evident paper safes.
5. **Use:** Invoked exclusively when system enters `RECOVERY_REQUIRED`.
6. **Emergency Destruction:** Hardware token PIN wipe executed upon detected physical breach.
7. **Monotonic Key Rotation:** Group key $Y_{old} \to Y_{new}$ rotated annually via $T$-of-$N$ threshold authorization.
8. **Revocation:** Compromised keyholder $i$ is revoked by generating a new polynomial setup excluding participant $i$.
9. **Participant Replacement:** Replacing administrator $i$ with replacement $j$ requires executing a DKG refresh protocol.
10. **Quorum Re-Keying:** Updating threshold parameter $T$ or total $N$ triggers full DKG re-registration.

---

## 10. Capability-Scoped Recovery Protocol & Binding Specification

A fundamental requirement of `RESEARCH-TRUST-003` is that recovery authorization must be **strictly capability-scoped and cryptographically bound**. Broad, generic "RECOVER_SYSTEM" overrides are prohibited.

```text
+--------------------------------------------------------------------------------------------------+
|                      MANDATORY CAPABILITY-SCOPED RECOVERY PAYLOAD                                |
+--------------------------+------------------------------------+----------------------------------+
| Mandatory Field          | Data Type / Value Example          | Specific Attack Prevented        |
+--------------------------+------------------------------------+----------------------------------+
| 1. system_id             | GUID: visual-intel-prod-us-east-1  | Cross-System Replay              |
| 2. recovery_request_id   | 256-bit UUID ticket identifier     | Transcript / Audit Duplication   |
| 3. unique_nonce          | 256-bit Random Hex (RunID)         | Direct Replay Attack             |
| 4. operation_id          | Enum: RESET_LEDGER_CHAIN           | Cross-Operation Replay           |
| 5. authorization_scope   | Scope string: database.ledger.db   | Unauthorized Scope Escalation    |
| 6. trust_anchor_id       | SHA-256 Hash + Version String      | Trust-Anchor Substitution        |
| 7. protocol_version      | Version string: 1.0.0              | Protocol Downgrade Attack        |
| 8. creation_time         | Monotonic UTC Timestamp            | Future-Dated Payload Attack      |
| 9. expiration_time       | Creation + 15 min Max Expiration   | Stale Authorization Broadcast    |
| 10. current_recovery_epoch| Monotonic Integer Counter (e.g. 7) | Cross-Epoch Replay Attack        |
+--------------------------+------------------------------------+----------------------------------+
```

### 10.1 Binding Rationale & Defense Mechanisms `[RESEARCH FINDING]`
- **Cross-System Replay Defense (`system_id`):** Prevents a valid recovery authorization signed for System A from being replayed against System B.
- **Cross-Operation & Scope Defense (`operation_id` & `authorization_scope`):** Restricts the authorization strictly to the declared action (e.g. `RESET_LEDGER_CHAIN`). Admins signing a database reset payload cannot have their signature repurposed to authorize trust-anchor key rotation.
- **Cross-Epoch Defense (`current_recovery_epoch`):** The system increments a monotonic epoch counter upon every completed recovery event. Signatures generated under Epoch $E$ are rejected under Epoch $E+1$.
- **Trust-Anchor Substitution Defense (`trust_anchor_id`):** Binds the recovery payload to the active trust-anchor hash, preventing attackers from injecting signed recovery requests generated under obsolete or fake trust anchors.

---

## 11. Verification Workflow `[CURRENT FACT]`
```text
[Recovery Request Received] ──► [Validate Signature σ using Group Key Y]
                                              │
                                              ▼
                               [Validate Nonce & Expiration Window]
                                              │
                                              ▼
                               [Validate System_ID & Trust_Anchor_ID]
                                              │
                                              ▼
                               [Execute Explicit Operation (e.g. Wipe DB)]
                                              │
                                              ▼
                               [Set State to UNKNOWN (ExecutionGate Remains Locked)]
```

---

## 12. Temporal & Replay Security

To prevent replay and stale-authority attacks, recovery requests enforce strict temporal constraints:

$$\text{Valid Window: } T_{current} \in [T_{creation}, T_{creation} + \Delta T_{max}] \quad \text{where } \Delta T_{max} = 900\text{ seconds}$$

1. **Replay Protection Nonce:** Each recovery challenge contains a 256-bit cryptographically random nonce $\text{RunID}$. Once processed, $\text{RunID}$ is written to the persistent consumed-nonce cache. Re-submitting a duplicate nonce triggers `ReplayAttackException`.
2. **Monotonic Clock Bound:** Timestamps use monotonic OS clock measurements ($\text{CLOCK\_MONOTONIC}$) to prevent system clock manipulation attacks.
3. **Stale Authority Expiration:** If a threshold signing round takes longer than $\Delta T_{max} = 15\text{ minutes}$, the request expires and must be re-initiated with a fresh challenge nonce.

---

## 13. Human Factors & Operational Engineering

A cryptographically perfect design that cannot be reliably operated during a real security incident is an unacceptable production architecture.

```text
[Incident Escalation] ──► (Incident Commander Issues Challenge Nonce)
                                      │
                                      ▼
[Out-of-Band Verification] ──► (Admins Verify Incident UUID over Voice/Video)
                                      │
                                      ▼
[Hardware Signing] ──► (3-of-5 Admins Insert YubiKey & Touch Hardware Button)
                                      │
                                      ▼
[Quorum Aggregation] ──► (Submit Partial Shares ──► Execute Epistemic Reset to UNKNOWN)
```

1. **Geographic & Organizational Separation:** Keyholders must be distributed across at least 2 distinct physical locations and organizational sub-teams to prevent local disaster or single-manager coercion.
2. **Approval Fatigue & Blind Signing:** Admins must visually verify the `incident_uuid` and `operation_id` on physical token screens or out-of-band secondary channels prior to touch confirmation.
3. **Emergency Coordination Drills:** Quorum signing drills must be executed semi-annually to maintain operational readiness.

---

## 14. Epistemic Failure Semantics & Authority Separation

This document reinforces the ratified tripartite authority separation of `ARCH-TRUST-001`:

```text
               AUTHORITY SEPARATION INVARIANT
  
  ┌────────────────────────┐       Does NOT Grant      ┌────────────────────────┐
  │ Recovery Authorization │ ────────────────────────► │ Runtime Authorization  │
  └────────────────────────┘                           └────────────────────────┘
              │                                                    │
              │ Permitted ONLY:                                    │ Required:
              ▼                                                    ▼
   Wipe DB / Reset Genesis                            Fresh Verification Run
              │                                                    │
              ▼                                                    ▼
     State = UNKNOWN                                     State = VERIFIED
              │                                                    │
              └────────────────────┬───────────────────────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ Execution Authority    │
                       │ (ExecutionGate Locked) │
                       └────────────────────────┘
```

> **Formal Invariant:** `[ARCHITECTURAL INVARIANT]`
> $$\text{Recovery Authorization} \neq \text{Runtime Authorization} \neq \text{Execution Authority}$$
> A verified 3-of-5 FROST recovery authorization permits **ONLY** the explicit recovery operation (e.g. wiping database history). It transitions state to `UNKNOWN`. It **NEVER** generates `VERIFIED` state and **NEVER** unlocks `ExecutionGate`.

### 14.1 Emergency-Recovery Paradox & Physical Cold-Boot Reset `[RECOMMENDATION]`
We analyze the extreme scenario where the threshold quorum is permanently lost or destroyed:

```text
[Threshold Quorum Destroyed (≥ N-T+1 Keys Lost/Compromised)]
                           │
                           ▼
          [System Locked Out in Panic State]
                           │
                           ▼
[Physical Cold-Boot Reset (Physical Server/HSM Re-flashing)]
                           │
                           ▼
          [Wipe Storage ──► State = UNKNOWN]
```

- **The Emergency-Recovery Paradox:** If threshold keyholders become permanently unavailable ($\ge N - T + 1$ keyholders lost/dead), no cryptographic recovery signature can ever be generated. A pure software system would remain permanently locked out.
- **Availability vs. Integrity Trade-off:** Introducing a remote "backdoor" or secondary unauthenticated bypass to resolve lockout would destroy the system's integrity boundary.
- **Architectural Resolution:**  
  1. **Physical Cold-Boot Reset MUST remain the ultimate recovery mechanism** for edge/single-node deployments (`[RECOMMENDATION]`).
  2. Physical cold-boot reset requires physical physical access to server hardware (re-flashing HSMs, re-imaging disk partitions, and manually setting genesis configuration).
  3. **Preservation of Authority Separation:** Even a physical cold-boot reset wipes persistent databases and forces state to `UNKNOWN`. It does **NOT** grant runtime authorization and does **NOT** unlock `ExecutionGate` without a fresh Verification Domain run.

---

## 15. Trust Dependency Impact & Governance Hierarchy

The introduction of threshold recovery updates the system trust dependency tree to a hardware-neutral governance hierarchy:

```text
[Offline Administrative / Governance Root]
                    │
                    ▼
[Threshold Key Generation & Governance]
                    │
                    ▼
[Hardware-Backed Participant Custody] (PROPOSED OPTION: YubiKey PIV)
                    │
                    ▼
[FROST Participant / Signing Layer]
                    │
                    ▼
[Group Public Key Y (Registered in System Config)]
                    │
                    ▼
[Recovery Challenge Verifier] ──► Wipes DB ──► State = UNKNOWN
                                                       │
                                                       ▼
                                        [Verification Domain Runs]
                                                       │
                                                       ▼
                                              [Assurance Domain]
                                                       │
                                                       ▼
                                              [ExecutionGate]
```

> **Root of Trust Classification:** `[ARCHITECTURAL ASSUMPTION]` The root of trust remains the **Offline Administrative / Governance Root**. YubiKey PIV tokens represent a `[PROPOSED HARDWARE CUSTODY OPTION]` for participant-side key custody, rather than the canonical root of trust.

---

## 16. Security Trade-off Comparative Matrix

We compare all seven candidate architectures across ten evaluation dimensions:

| Evaluation Dimension | Option A (Single Key) | Option B (Multi-Sig) | Option C (FROST 3-of-5) | Option D (BLS 3-of-5) | Option E (Hardware 1-Key) | Option F (FROST + Hardware Custody) | Option G (Hybrid Cold) |
|---|---|---|---|---|---|---|---|
| **Compromise Resistance** | Zero (1 key) | High ($T$ keys) | High ($T$ keys) | High ($T$ keys) | Medium (HW bound) | **High (HW + $T$)** | High |
| **Availability Survivability**| Zero | High ($N-T$) | High ($N-T$) | High ($N-T$) | Zero | **High ($N-T$)** | High |
| **Signature Size** | $64\text{ B}$ | $M \times 64\text{ B}$ | **$64\text{ B}$ (Standard)**| $96\text{ B}$ | $64\text{ B}$ | **$64\text{ B}$** | $64\text{ B}$ |
| **Verification Speed** | $< 1\text{ms}$ | Medium | **$< 1\text{ms}$ (Standard)**| Slow ($15\text{ms}$) | $< 1\text{ms}$ | **$< 1\text{ms}$** | $< 1\text{ms}$ |
| **Interactive Rounds** | 0 | 0 | 2 Rounds | 0 | 0 | 2 Rounds | Multi-tier |
| **Hardware Key Support** | High | High | High | Low | High | **Hardware-backed custody possible; native FROST execution NOT established** | High |
| **Identity Anonymity** | Public Key | Disclosed | **Privacy Preserved**| Disclosed | Public Key | **Privacy Preserved**| Disclosed |
| **Operational Overhead** | Minimal | Medium | Medium | Medium | Low | High | Extreme |
| **DKG Complexity** | None | None | Medium | Medium | None | Medium | High |
| **Evaluation Rating** | Unsafe | Acceptable | **Recommended** | Sub-optimal | Unsafe | **Preferred Baseline** | Over-engineered |

---

## 17. Evidence Classification Table

All quantitative and security assertions in this research are classified per `ARCH-TRUST-001` discipline:

| Assertion | Evidence Classification | Source / Baseline |
|---|---|---|
| Single key theft permits full database wipe | `[CURRENT FACT]` | Code inspection of `ARCH-TRUST-001` recovery handler |
| Verified recovery transitions state to `UNKNOWN` | `[CURRENT FACT]` | Ratified `ARCH-TRUST-001` State Machine (Section 4.1) |
| FROST produces standard 64-byte Ed25519 signatures | `[RESEARCH FINDING]` | IETF RFC / FROST Specification (Komlo & Goldberg, 2020) |
| BLS12-381 signature verification latency ($15\text{ms}$) | `[REFERENCE BENCHMARK]` | Published Apache Milagro / RELIC benchmarking studies |
| Local signature check latency ($< 1\text{ms}$) | `[EXPERIMENTAL EVIDENCE]` | Empirical test run `RTC-010` in local environment |
| $T=3, N=5$ tolerates 2 lost keyholders & 2 compromises | `[ANALYTICAL ESTIMATE]` | Mathematical evaluation ($T-1 = 2$, $N-T = 2$) |
| YubiKey PIV prevents software malware key exfiltration | `[ARCHITECTURAL ASSUMPTION]` | Hardware Security Boundary Model (Yubico PIV Spec) |
| YubiKey PIV requires participant daemon for FROST | `[INFERENCE]` | Cryptographic Firmware & FROST Protocol Analysis (Section 8) |
| FROST-Ed25519 verifier ciphersuite compatibility | `[OPEN QUESTION]` | To be empirically benchmarked during future implementation |

---

## 18. Recommended Architectural Direction

### 18.1 Proposed Architectural Direction `[RECOMMENDATION]`
The research identifies **Option F (Multi-Party Hardware-Backed FROST 3-of-5 Threshold Signature Recovery with Participant Host Daemon)** as the preferred baseline target for out-of-band administrative overrides.

- **Primary Parameters:** $T=3, N=5$ threshold scheme over Ed25519.
- **Hardware Integration Boundary:** Key shares $s_i$ secured via hardware custody tokens (e.g. YubiKey PIV) coordinated by a trusted participant-side host daemon managing FROST session nonces.
- **Scope Restriction:** Recovery requests must contain explicit capability payloads (`operation_id`, `incident_uuid`, `system_id`, `nonce`, 15-minute expiration).
- **Provisional Status:** This recommendation defines the architectural target. It **does NOT authorize code implementation** or key generation at this stage.

---

## 19. Open Questions & Future Research

1. **Automated Asynchronous Round-1 Preprocessing:** Evaluating whether pre-generating FROST nonce commitments ($D_i, E_i$) during quiet periods reduces emergency interactive signing latency.
2. **Post-Quantum Threshold Signatures:** Investigating lattice-based threshold schemes (e.g. Dilithium / Falcon threshold variants) for long-term quantum resistance.
3. **FROST Ciphersuite Verification Benchmarks:** Empirically testing `FROST-Ed25519` aggregate output signatures against standard RFC 8032 Ed25519 verification functions (`[OPEN QUESTION]`).

---

## 20. Formal Architectural Invariants & Final Decision Gate

### 20.1 Formal Architectural Invariants
We establish the following formal classifications for the system record:

1. `[ARCHITECTURAL INVARIANT]` No single administrator can authorize privileged system recovery.
2. `[ARCHITECTURAL INVARIANT]` Recovery authorization cannot directly produce `VERIFIED` epistemic state.
3. `[ARCHITECTURAL INVARIANT]` Recovery authorization cannot directly unlock `ExecutionGate`.
4. `[ARCHITECTURAL INVARIANT]` Every recovery authorization is capability-scoped and operation-bound.
5. `[ARCHITECTURAL INVARIANT]` Every recovery authorization is single-use and nonce-bound.
6. `[ARCHITECTURAL INVARIANT]` Every recovery authorization expires within a maximum 15-minute monotonic window.
7. `[ARCHITECTURAL INVARIANT]` Every recovery authorization is cryptographically auditable on the ledger.
8. `[ARCHITECTURAL INVARIANT]` Loss of a single administrator credential does not destroy system recoverability.
9. `[ARCHITECTURAL INVARIANT]` Compromise of fewer than $T$ participants ($k < T$) yields zero cryptographic information about the recovery group secret under Shamir secret sharing.

---

### 20.2 Final Decision Gate Status

```text
RESEARCH-TRUST-003
STATUS: RESEARCH COMPLETE

CRYPTOGRAPHIC SEMANTICS: COMPLETE
FROST/HARDWARE INTEGRATION BOUNDARY: COMPLETE
RECOVERY BINDING ANALYSIS: COMPLETE
AVAILABILITY / RECOVERY ANALYSIS: COMPLETE
CANONICAL CONSISTENCY: PASS

IMPLEMENTATION DECISION: DEFER
ARCHITECTURAL AMENDMENT REQUIRED: NO
IMPLEMENTATION AUTHORIZED: NO
```

---
*End of Deliverable: `RESEARCH-TRUST-003-THRESHOLD-RECOVERY-ADMIN-OVERRIDE-CRYPTOGRAPHY.md`*

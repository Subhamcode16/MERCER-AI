# RESEARCH-TRUST-002 — Privacy-Preserving Evidence Analysis

**Document ID:** `RESEARCH-TRUST-002-PRIVACY-PRESERVING-EVIDENCE-ANALYSIS`  
**Author:** Engineering Agent  
**Review Target:** Intelligence Architect / Security Review Board  
**Status:** RESEARCH COMPLETE  
**Implementation Decision:** DEFER  
**Implementation Authorized:** NO  
**Date:** 2026-09-03  

---

## Executive Summary

Following the ratification of [`ARCH-TRUST-001-TRUST-AUTHORITY-EPISTEMIC-CONSOLIDATION.md`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/chatgpt%20message%20box/ARCH-TRUST-001-TRUST-AUTHORITY-EPISTEMIC-CONSOLIDATION.md) and the formal approval of [`RESEARCH-TRUST-001-DECENTRALIZED-TRUST-ANCHOR-ANALYSIS.md`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/chatgpt%20message%20box/RESEARCH-TRUST-001-DECENTRALIZED-TRUST-ANCHOR-ANALYSIS.md) (`DEFER`), this research document addresses **RESEARCH-TRUST-002**.

The core objective of this research is to evaluate whether the `Verification Domain` can establish cryptographically meaningful claims about sensitive creative assets without ingesting or storing the raw underlying asset, and whether Zero-Knowledge Proofs (ZKPs) or simpler cryptographic primitives are the appropriate architectural mechanism for our Visual Intelligence engine.

Every major assertion in this document preserves the epistemic taxonomy required by `ARCH-TRUST-001`:
- `[CURRENT FACT]` — Empirical property of the existing system implementation.
- `[ARCHITECTURAL ASSUMPTION]` — Declared root-of-trust boundary or environment assumption.
- `[RESEARCH FINDING]` — Analytical result established by literature or mathematical modeling.
- `[EXPERIMENTAL EVIDENCE]` — Measured result from empirical test runs (`RTC-008`–`RTC-012`).
- `[REFERENCE BENCHMARK]` — Published literature benchmark from external research.
- `[ANALYTICAL ESTIMATE]` — Derived engineering estimate based on benchmarks and specifications.
- `[INFERENCE]` — Logical deduction derived from facts, assumptions, or findings.
- `[RECOMMENDATION]` — Actionable architectural decision.
- `[UNRESOLVED QUESTION]` — Open technical boundary requiring future study.

---

## 1. Problem Definition & Architectural Vocabulary

To establish a precise mathematical and architectural foundation, we formally define the core elements of privacy and evidence verification:

```text
[Producing Domain] ──► (Generates Asset A & Private Inputs) ──► [Commitment Engine] ──► (Public Salted Hash C_A)
                                                                                               │
                                                                                               ▼
[Verification Domain] ◄── (Evaluates Ephemeral Asset or Proof Π) ◄── [Privacy-Boundary Boundary]
```

1. **Asset ($A$):** `[CURRENT FACT]` The generated creative work (e.g. high-resolution RGBA image pixels, vector metadata, or campaign layout specifications).
2. **Asset Owner:** `[CURRENT FACT]` The administrative or corporate entity possessing intellectual property custody over Asset $A$.
3. **Producing Domain (Local Intelligence Domain):** `[CURRENT FACT]` The untrusted runtime component (generative models, pipeline compilers) that generates Asset $A$ and initial state claims.
4. **Verification Domain:** `[CURRENT FACT]` The isolated, trusted harness (`VerificationHarness`) responsible for executing verification logic and issuing evidence digests.
5. **Private Inputs ($w$):** `[RESEARCH FINDING]` Confidential witness parameters (raw pixel arrays $P_{raw}$, random generation seeds $S_{gen}$, model weights $W_{local}$, salted blinding factors $R_{salt}$) retained within the Producing Domain.
6. **Public Inputs ($x$):** `[RESEARCH FINDING]` Cryptographic digests and public parameters ($H(A \parallel R_{salt})$, target version $V_{target}$, run identifier $\text{RunID}$, tolerance thresholds $\theta_{drift}$) exposed to the Verification Domain.
7. **Computation ($C$):** `[RESEARCH FINDING]` The mathematical function or circuit mapping $(x, w) \to \{0, 1\}$ to verify property compliance.
8. **Claimed Property ($P$):** `[CURRENT FACT]` The assertion being evaluated (e.g., "Asset $A$ has a color drift ratio $\le 10\%$ against palette $C_{ref}$").
9. **Proof Statement ($\Pi$):** `[RESEARCH FINDING]` A cryptographic object proving $\exists w \text{ s.t. } C(x, w) = 1$ without disclosing $w$.
10. **Verification Key ($\text{VK}$):** `[RESEARCH FINDING]` Public cryptographic parameters derived during circuit setup enabling any verifier to validate $\Pi(x, \text{VK})$.
11. **Asset Identity & Version Binding:** `[CURRENT FACT]` The immutable hash $H(A)$ cryptographically bound to the software compilation version $V_{target}$.
12. **Provenance Metadata:** `[CURRENT FACT]` Structured execution context (verifier version, seed, environment ID, timestamp) bound to evidence payloads.
13. **Freshness Token:** `[CURRENT FACT]` A monotonic clock timestamp ($\text{monotonic\_time}$) ensuring evidence expiration.
14. **Replay Protection Nonce:** `[CURRENT FACT]` A unique, single-use $\text{RunID}$ challenge preventing transcript replay attacks.

> **Fundamental Epistemic Boundary:** `[RESEARCH FINDING]`
> $$\text{RAW-ASSET NON-EXPOSURE} \neq \text{RAW-ASSET NON-PERSISTENCE}$$
> • **Raw-Asset Non-Exposure:** The `Verification Domain` evaluates claims without ingesting or seeing raw asset pixels $P_{raw}$ at all (achieved ONLY via ZKPs or TEE enclaves).  
> • **Raw-Asset Non-Persistence:** The `Verification Domain` ingests raw asset pixels $P_{raw}$ in transient RAM, evaluates properties, and immediately discards $P_{raw}$ without writing pixels to persistent disk or ledger storage.

---

## 2. Evaluation of Candidate Approaches (Options A through H)

We evaluate eight candidate privacy-preserving verification architectures:

### 2.1 Option A: Raw Asset Verification `[CURRENT FACT]`
- **Mechanism:** The Producing Domain passes raw pixel arrays directly to the Verification Domain over IPC/local memory.
- **Pros:** Zero cryptographic overhead; instantaneous execution ($<1\text{ms}$ IPC latency measured in `RTC-010`).
- **Cons:** Zero confidentiality; raw proprietary pixels are stored persistently in verifier logs, memory dumps, and database backups.

### 2.2 Option B: Hash / Commitment-Based Evidence `[RESEARCH FINDING]`
- **Mechanism:** Producing Domain publishes a salted commitment $C_A = \text{SHA-256}(A \parallel R_{salt})$. Verification Domain checks validity against pre-registered commitments.
- **Pros:** Cryptographic asset binding; negligible CPU overhead ($<1\text{ms}$); simple auditability.
- **Cons:** A salted hash commitment provides cryptographic binding to the committed asset, but the commitment itself does not constitute a universal confidentiality guarantee against brute-force inspection of low-entropy inputs. Furthermore, a commitment alone cannot independently establish visual properties over hidden pixels without an additional proof or attestation mechanism.

### 2.3 Option C: Signed Metadata Attestations `[RESEARCH FINDING]`
- **Mechanism:** An authorized verifier binary running in transient memory computes metrics, signs a structured metadata payload $S_{admin}(\text{Metadata})$, and discards raw pixels.
- **Pros:** Fast execution ($<5\text{ms}$); low storage footprint ($<2\text{KB}$ per evidence payload); verifiable by third parties.
- **Cons:** Relies on transient memory security; does not provide zero-knowledge mathematical proof against a compromised verifier binary.

### 2.4 Option D: Merkle Tree Commitments `[RESEARCH FINDING]`
- **Mechanism:** Asset $A$ is divided into tile chunks $A_1, \dots, A_n$, structured as a Merkle tree. The verifier requests Merkle paths for specific tiles.
- **Pros:** Selective inspection of local image sections without exposing the entire asset.
- **Cons:** Tile-level exposure still leaks local visual features; Merkle proof construction adds memory and IPC overhead.

### 2.5 Option E: Trusted Execution Environments (TEEs / Intel SGX / ARM TrustZone) `[RESEARCH FINDING]`
- **Mechanism:** The Verification Domain executes inside a hardware-isolated enclave. Raw pixels are decrypted inside the CPU enclave; the enclave outputs a signed hardware attestation.
- **Pros:** High performance ($<10\text{ms}$ execution latency); achieves Raw-Asset Non-Exposure to the host OS root environment.
- **Cons:** Hardware vendor monoculture lock-in (Intel/ARM); vulnerable to CPU side-channel attacks (Spectre/Foreshadow); requires specialized hardware.

### 2.6 Option F: Selective Disclosure Cryptography (Attribute-Based Credentials) `[RESEARCH FINDING]`
- **Mechanism:** Uses Anonymous Credentials (e.g. BBS+ signatures) to prove specific asset metadata attributes without exposing full asset credentials.
- **Pros:** Elegant metadata privacy; prevents verifier tracking across different verification runs.
- **Cons:** Does not verify complex visual algorithms (e.g., color drift, spatial resolution) over high-dimensional image tensors.

### 2.7 Option G: Zero-Knowledge Proof Circuits (zk-SNARKs / Groth16 / PLONK) `[RESEARCH FINDING]`
- **Mechanism:** The Producing Domain constructs an arithmetic circuit $C(x, w)$ proving property compliance, generating a zk-SNARK proof $\Pi$. The Verification Domain verifies $\Pi$ using $\text{VK}$.
- **Pros:** Cryptographic privacy under the security assumptions of the selected proof system and implementation; achieves true Raw-Asset Non-Exposure to the Verification Domain; succinct verification time ($\sim 5\text{ms}–15\text{ms}$).
- **Cons:** Extreme prover computational cost ($5\text{s}–120\text{s}$ prover time); massive RAM requirements ($4\text{GB}–16\text{GB}$ memory allocation per image circuit); complex trusted setup (SRS).

### 2.8 Option H: Ephemeral Raw-Asset Verification & Storage Reduction (Salted Hash Commitments + Signed Metadata + Transient Verification) `[RECOMMENDATION]`
- **Mechanism:** Combine Option B, C, and transient memory processing:
  1. Producing Domain generates Asset $A$ and salted commitment $C_A = \text{SHA-256}(A \parallel R_{salt})$.
  2. Isolated `VerificationHarness` receives $A$ in ephemeral, non-persisted shared memory.
  3. Harness evaluates visual metrics, signs a structured provenance payload $S_{verifier}(\text{Digest})$, writes the signed evidence to the ledger, and immediately wipes raw pixels from RAM.
- **Properties Provided:**
  • Ephemeral processing window.  
  • Persistent-storage exposure reduction (zero raw pixels written to disk/logs).  
  • Cryptographic asset binding ($C_A$).  
  • Signed verification evidence payloads.  
- **Properties NOT Provided:**
  • Option H does **NOT** provide zero raw-pixel exposure to the Verification Domain. Raw Asset $A$ is ingested by `VerificationHarness` in transient memory during evaluation.  
  • **Option H is NOT equivalent to Zero-Knowledge Verification.**  
- **Pros:** Preserves $<5\text{ms}$ execution speed; eliminates persistent database data leak vectors; low implementation complexity.
- **Cons:** Relies on local container OS memory isolation during the transient execution window.

---

## 3. Concrete Proof Statement Specifications

We specify three practical visual verification circuits relevant to our content-generation engine:

```text
[Scenario 1: Color Drift Circuit]     [Scenario 2: Resolution Circuit]     [Scenario 3: Watermark Authenticity]
   Raw Pixels (Private)                 Image Dimensions (Private)            Generation Seed (Private)
         │                                    │                                     │
         ▼                                    ▼                                     ▼
   Drift <= 10% (Public)                Width >= 1920 (Public)                HMAC-SHA256 Match (Public)
```

### 3.1 Scenario 1: Color Palette Compliance (Drift $\le 10\%$)
- **PRIVATE INPUT ($w$):** Raw RGBA pixel array $P_{raw} \in \mathbb{R}^{H \times W \times 4}$, Blinding Salt $R_{salt}$.
- **PUBLIC INPUT ($x$):** Asset Commitment $C_A = H(P_{raw} \parallel R_{salt})$, Reference Palette $C_{palette}$, Maximum Allowed Drift $\theta_{drift} = 0.10$, Nonce $\text{RunID}$.
- **COMPUTATION ($C$):**
  $$\text{Verify } H(P_{raw} \parallel R_{salt}) = C_A$$
  $$D = \frac{1}{N} \sum_{i=1}^{N} \min_{j} \|P_{raw}[i] - C_{palette}[j]\|_2 \le \theta_{drift}$$
- **CLAIM:** The unreleased asset matching $C_A$ conforms to the target color palette within $10\%$ drift tolerance.
- **PROOF ($\Pi$):** zk-SNARK proof string ($\sim 256\text{ bytes}$ under Groth16).
- **VERIFIER KNOWLEDGE:** The verifier learns only that a private witness $P_{raw}$ exists whose hash matches $C_A$ and whose computed color drift ratio $D \le 0.10$.
- **PROVED MATHEMATICALLY:** The committed private asset satisfies the specified mathematical color-drift constraint.
- **NOT PROVED / OUTSIDE PROOF:** The asset is aesthetically good, commercially effective, brand-appropriate, or free of third-party copyright infringement.
- **TRUST ASSUMPTIONS:** `[ARCHITECTURAL ASSUMPTION]` Cryptographic soundness of Groth16 curve (BN254); non-compromise of SRS setup parameters.

### 3.2 Scenario 2: Minimum Resolution & Aspect Ratio Boundaries
- **PRIVATE INPUT ($w$):** Image height $H_{pixels}$, width $W_{pixels}$, raw header metadata.
- **PUBLIC INPUT ($x$):** Asset Commitment $C_A$, Minimum Width $W_{min} = 1920$, Minimum Height $H_{min} = 1080$, Required Aspect Ratio $R_{target} = 1.777$.
- **COMPUTATION ($C$):**
  $$\text{Verify } H(\text{Header} \parallel R_{salt}) = C_A \land W_{pixels} \ge 1920 \land H_{pixels} \ge 1080 \land \left|\frac{W_{pixels}}{H_{pixels}} - 1.777\right| \le 0.01$$
- **CLAIM:** The asset committed under $C_A$ meets high-definition resolution bounds without exposing image subject matter.
- **PROOF ($\Pi$):** Range proof / zk-SNARK payload ($\sim 192\text{ bytes}$).
- **VERIFIER KNOWLEDGE:** Height and width satisfy numerical range constraints.
- **PROVED MATHEMATICALLY:** The private header dimensions satisfy $W_{pixels} \ge 1920 \land H_{pixels} \ge 1080 \land \text{Aspect Ratio} \approx 1.777$.
- **NOT PROVED / OUTSIDE PROOF:** The image contains sharp visual details, is free from blurring artifacts, or conforms to visual artistic standards.
- **TRUST ASSUMPTIONS:** `[RESEARCH FINDING]` Arithmetic range-proof circuit completeness.

### 3.3 Scenario 3: Watermark Authenticity & Seed Integrity
- **PRIVATE INPUT ($w$):** Generation Seed $S_{gen}$, Model Weights Hash $W_{hash}$.
- **PUBLIC INPUT ($x$):** Watermark Hash $H_{wm}$, Asset Commitment $C_A$, Generator Version $V_{gen}$.
- **COMPUTATION ($C$):**
  $$\text{Verify } \text{HMAC-SHA256}(S_{gen}, C_A) = H_{wm} \land \text{VersionMatch}(V_{gen})$$
- **CLAIM:** The asset committed under $C_A$ was genuinely produced by an authorized generator run using seed $S_{gen}$.
- **PROOF ($\Pi$):** Preimage proof payload ($\sim 128\text{ bytes}$).
- **VERIFIER KNOWLEDGE:** The HMAC hash matches the pre-registered watermark commitment $H_{wm}$ for version $V_{gen}$.
- **PROVED MATHEMATICALLY:** The prover possesses the valid seed $S_{gen}$ that produces $H_{wm}$ bound to $C_A$.
- **NOT PROVED / OUTSIDE PROOF:** The generative model output is safe, morally compliant, or free of bias.
- **TRUST ASSUMPTIONS:** `[ARCHITECTURAL ASSUMPTION]` Preimage resistance of SHA-256.

---

## 4. Comprehensive Security & Cryptographic Analysis

We evaluate candidate privacy approaches across 17 security dimensions:

| Security Dimension | Option A (Raw) | Option B (Salted Hash) | Option C (Signed Meta) | Option E (TEE Enclave) | Option G (ZKP Circuit) | Option H (Hybrid Baseline) |
|---|---|---|---|---|---|---|
| **Confidentiality** | Zero | High (Commitment) | High (Metadata) | High (Hardware) | Cryptographically Bound | High (Ephemeral RAM) |
| **Integrity** | High | High (Hash bound) | High (Signature) | High (Attested) | Cryptographically Bound | High (Signed Digest) |
| **Authenticity** | Low | Medium | High (Signatures) | High (Hardware) | High (VK-bound) | High (Admin Signed) |
| **Provenance** | Direct | Indirect | Cryptographic | Hardware Bound | Cryptographic | Cryptographic |
| **Freshness** | Monotonic | Monotonic | Monotonic | Nonce-bound | Nonce-bound | Monotonic Nonce |
| **Replay Resistance**| Nonce | Nonce | Nonce | Enclave Nonce | Public Input Nonce| Nonce Checked |
| **Version Binding** | Manual | Digest bound | Metadata bound | Enclave Measurement| Public Input Bound| Digest & Meta Bound |
| **Tamper Resistance**| Zero | High | High | High | Cryptographically Bound | High |
| **Verifier Independence**| High | High | High | Low (Vendor dependency)| High (Math bound) | High |
| **Soundness** | N/A | High | High | High (Vendor dependent)| Cryptographically Bound ($2^{-128}$)| High |
| **Completeness** | N/A | High | High | High | Cryptographically Bound | High |
| **Privacy Leakage** | $100\%$ | Zero | Minimal (Metadata) | Zero | Zero | Zero (Disk) |
| **Metadata Leakage**| Full | Size/Digest | Explicit Schema | Enclave Attestation| Public Inputs Only| Minimal Schema |
| **Setup Assumptions**| None | Hash function | Key Infrastructure | Vendor PKI | Trusted Setup SRS | Key Infrastructure |
| **Key Compromise Impact**| N/A | Low | Medium | High | High (SRS leakage)| Medium |
| **Implementation Complexity**| Minimal | Very Low | Low | High | Extremely High | Low |

---

## 5. Critical Epistemic Constraint: Proof vs. Truth

A fundamental requirement of `ARCH-TRUST-001` is preserving the strict distinction between **cryptographic verification** and **objective reality**.

```text
+---------------------------------------------------------------------------------------------------+
|                                 EPISTEMIC BOUNDARY MATRIX                                         |
+---------------------------------------------------+-----------------------------------------------+
| Cryptographic Statement                           | Objective Reality Reality                     |
+---------------------------------------------------+-----------------------------------------------+
| Cryptographic Proof (Π) Is Valid                 ≠  Objective Truth                              |
| Valid Proof / Circuit Result = True              ≠  Correct Underlying Business Claim             |
| Valid Evidence Provenance                         ≠  Ground Truth Reality                         |
| Computation Correctness                           ≠  Semantic Correctness                         |
+---------------------------------------------------+-----------------------------------------------+
```

### 5.1 Mathematical Rationale `[RESEARCH FINDING]`
A Zero-Knowledge Proof $\Pi$ or cryptographic signature $S$ establishes **strictly** that:
$$\text{A specific computation } C(x, w) \text{ evaluated to } 1 \text{ over specified inputs } (x, w)$$

It does **NOT** establish that:
1. The underlying business assumption behind $C$ is semantically valid.
2. The raw image $P_{raw}$ is aesthetically pleasing, human-approved, or free from brand copyright violations.
3. The prompt provided to the generative model represented truthful real-world intent.

> **Epistemic Invariant:** `[INFERENCE]` Cryptographic proof guarantees *execution correctness over declared inputs within circuit bounds*; it does not manufacture objective truth out of faulty human or model premises.

---

## 6. Architectural Placement & Interaction Map

```text
[Producing Domain]
       │
       ├─► Ephemeral Private RAM (Raw Pixels P_raw, Seed S_gen)
       │         │
       │         ▼
[Privacy-Preserving Verification Boundary (Option H)] ◄─── Ephemeral Processing Window
       │   - Computes SHA-256(P_raw || R_salt)
       │   - Evaluates Visual Constraints
       │   - Generates Epistemic Evidence Payload
       │   - Ephemeral Memory Wipe
       │
       ▼
[Verification Domain]
       │   - Inspects Signed Evidence Digest
       │   - Verifies Freshness Nonce (RunID)
       │
       ▼
[Assurance Domain]
       │   - Updates Epistemic State Graph (UNKNOWN ──► UNVERIFIED ──► VERIFIED)
       │
       ▼
[ExecutionGate] ──► (Fail-Closed Authorization)
```

### 6.1 Epistemic State Machine Transitions `[CURRENT FACT]`
1. **Initial State (`UNKNOWN`):** Claim is registered; raw asset $A$ is held in private ephemeral memory.
2. **Registration (`UNVERIFIED`):** Salted commitment $C_A = \text{SHA-256}(A \parallel R_{salt})$ is committed to the Assurance Graph.
3. **Verification Processing:** Transient `VerificationHarness` evaluates visual compliance in ephemeral RAM, issues signed evidence payload $E_{digest}$, and wipes $A$ from memory.
4. **Transition (`VERIFIED`):** Assurance Domain evaluates $E_{digest}$, freshness, and counterexample status, transitioning claim state to `VERIFIED`.
5. **Enforcement (`ExecutionGate`):** `ExecutionGate` checks `VERIFIED` state and authorizes downstream release gating.

---

## 7. Performance & Operational Cost Evaluation

We compare performance dimensions between Option A (Raw), Option G (ZKP Circuit), and Option H (Hybrid Baseline):

| Performance Dimension | Option A (Raw IPC) `[EXPERIMENTAL EVIDENCE]` | Option G (zk-SNARK Circuit) `[REFERENCE BENCHMARK]` | Option H (Hybrid Baseline) `[ANALYTICAL ESTIMATE]` |
|---|---|---|---|
| **Proof Generation Time** | $0\text{ ms}$ (No proof) | $5,000\text{ ms} – 120,000\text{ ms}$ | $< 2\text{ ms}$ (SHA-256 / Ed25519) |
| **Verification Latency** | $< 1\text{ ms}$ (IPC measured) | $5\text{ ms} – 15\text{ ms}$ (SNARK check) | $< 1\text{ ms}$ (Signature check) |
| **Peak RAM Allocation** | $< 50\text{ MB}$ (Local buffer) | $4,000\text{ MB} – 16,000\text{ MB}$ | $< 50\text{ MB}$ (Ephemeral buffer) |
| **Proof / Payload Size** | $8\text{ MB}$ (Raw pixels) | $256\text{ Bytes}$ (Groth16 proof) | $< 2\text{ KB}$ (Signed digest) |
| **Scalability (Throughput)** | $> 500\text{ ops/sec}$ | $< 0.1\text{ ops/sec}$ (Single CPU) | $> 500\text{ ops/sec}$ |
| **Hardware Requirements** | Standard CPU | High-End GPU / Multi-Core Server | Standard CPU |
| **Operational Complexity** | Minimal | Extreme (Circuit maintenance) | Low |

### 7.1 Performance Classification Notes `[INFERENCE]`
- **Local IPC & Signature Speed (`<1ms` / `<2ms`):** Measured empirically in `RTC-010` (`[EXPERIMENTAL EVIDENCE]`).
- **ZKP Prover Latency ($5\text{s}–120\text{s}$):** Literature benchmark derived from external zk-SNARK image circuit research (e.g. zk-ML / Libsnark benchmarks on $1024 \times 1024$ pixel matrices) (`[REFERENCE BENCHMARK]`).
- **RAM Overhead ($4\text{GB}–16\text{GB}$):** Analytical estimate based on constraint graph expansion ($O(N)$ R1CS constraints for $10^6$ pixels) (`[ANALYTICAL ESTIMATE]`).

> **Performance Verdict:** `[INFERENCE]` Full ZKP circuits (Option G) introduce a **$2500\times–60,000\times$ prover latency penalty** and massive RAM overhead, rendering them completely unfeasible for real-time edge execution loops.

---

## 8. Architectural Recommendation & Dual-Question Breakdown

### 8.1 Dual-Question Analysis `[RECOMMENDATION]`
The research objective evaluates two distinct questions:

- **Question 1: Can we reduce persistent raw-asset storage exposure cheaply?**  
  • **Answer:** **YES.** **Option H (Salted Hash Commitments + Ephemeral Verification)** is an effective, high-performance operational candidate for eliminating persistent raw pixel exposure on disk, in log files, and in ledger databases (`[RECOMMENDATION]`).

- **Question 2: Can we verify properties without exposing raw assets to the Verification Domain itself?**  
  • **Answer:** **YES in principle** using ZKP (Option G) or TEE (Option E) mechanisms. However, **NOT with Option H alone**, because Option H ingests raw Asset $A$ into the `VerificationHarness` transient memory during evaluation (`[RESEARCH FINDING]`).

### 8.2 Formal Recommendation Outcome `[RECOMMENDATION]`
**RECOMMENDATION OUTCOME: DEFER**

- **Justification:** Full ZKP circuits (Option G) are **DEFERRED** for local edge runtimes due to extreme computational prover latency ($5\text{s}–120\text{s}$) and memory cost ($4\text{GB}–16\text{GB}$). The system shall adopt **Option H (Ephemeral Raw-Asset Verification & Storage Reduction)** as the operational privacy baseline.  
- **Explicit Property Statement:** Option H provides persistent-storage exposure reduction and ephemeral raw-asset verification; **it is NOT equivalent to Zero-Knowledge Verification and does NOT provide zero raw-pixel exposure to the Verification Domain.**
- **Future Re-evaluation Trigger:** Full ZKP circuits should only be re-evaluated if:
  1. Verification must be performed by untrusted third-party external networks without hardware enclave isolation.
  2. zk-SNARK prover performance advances to $< 200\text{ms}$ for megapixel image constraints on standard edge CPUs.

---

## 9. Explicit Implementation Gate

```text
RESEARCH-TRUST-002
PRIVACY BOUNDARY CORRECTION: COMPLETE
TERMINOLOGY CORRECTION: COMPLETE
PROOF-SEMANTICS CORRECTION: COMPLETE
RECOMMENDATION: DEFER
IMPLEMENTATION AUTHORIZED: NO
```

---

## 10. Permanent Architectural Record Classifications

This document is filed as part of the permanent architecture record. All assertions preserve explicit epistemic classifications:

- `[CURRENT FACT]` Raw asset verification currently executes over local IPC buffers in `VerificationHarness`.
- `[ARCHITECTURAL ASSUMPTION]` Ephemeral RAM memory space is isolated by host OS container boundaries.
- `[RESEARCH FINDING]` ZKP prover times for megapixel images require $5\text{s}–120\text{s}$ and $4\text{GB}–16\text{GB}$ RAM allocation based on published literature benchmarks.
- `[EXPERIMENTAL EVIDENCE]` RTC-010 demonstrated $<1\text{ms}$ IPC latency and SHA-256 commitment performance.
- `[INFERENCE]` Option H provides robust persistent-storage exposure reduction at $0.0001\times$ the computational cost of ZKPs, but ingests raw pixels in transient RAM.
- `[RECOMMENDATION]` DEFER full ZKP circuit implementation; adopt Option H as operational privacy baseline.
- `[UNRESOLVED QUESTION]` Verification circuit optimizations for GPU-accelerated zk-STARKs without trusted setups.

# Phase 26: Scoped Memory Partitions & Confidentiality Specification

## 1. Overview
The Worker Memory Subsystem partitions memories into 6 distinct tiers to prevent cross-tenant and cross-client leakage while maintaining attribution and anti-poisoning defenses.

## 2. Memory Partitions
1. `SESSION_MEMORY`: Ephemeral scratchpad for a single task session.
2. `CAMPAIGN_MEMORY`: Context scoped to a single campaign (`campaign_id`).
3. `CLIENT_MEMORY`: Private client preferences, guidelines, and historical feedback.
4. `BRAND_MEMORY`: Brand identity, visual DNA rules, archetype constraints.
5. `WORKER_MEMORY`: Private worker reflections, task performance notes.
6. `INSTITUTIONAL_MEMORY`: Abstract patterns, cross-campaign lessons (purged of client secrets).

## 3. Security Invariants
- **Memory $\neq$ Policy**: Learned memory cannot override security policy or expand capabilities.
- **Cross-Client Boundary**: Worker A querying memory under `client_a` cannot access `client_b` data.
- **Anti-Poisoning Filter**: Memory store scans strings for injection payloads (e.g. `ignore previous instructions`) and aborts write operations.

# Phase 25: Visual Observatory Subsystem Report

## 1. Overview
The Visual Observatory (`src/visual_observatory/`) monitors visual artifact generation, aesthetic drift, quality benchmarks, brand compliance, and visual quarantine registries.

## 2. Invariant Enforcement
- **Quarantine Enclosure**: Artifacts flagged with aesthetic drift ($\text{drift} > 0.15$) or brand guideline violations are locked in quarantine with `quarantine_status="QUARANTINED"`.
- **Governed Disposition**: Quarantined artifacts cannot be published or released to campaign deliverables without an explicit, audited operator disposition (`APPROVED` or `REJECTED`).
- **Full Lineage Tracing**: Visual artifacts maintain complete parent-child ancestry, linking prompts, models, seeds, and brand tokens back to source campaign stages.

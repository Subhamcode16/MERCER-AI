# Phase 28: Governed Knowledge Promotion & Rollback Runbook

## 1. Promotion Lifecycle
Knowledge moves through strict states:
`OBSERVED` $\rightarrow$ `PROVISIONAL` $\rightarrow$ `REVIEWED` $\rightarrow$ `VALIDATED` $\rightarrow$ `PROMOTED` $\rightarrow$ `ROLLED_BACK` / `RETIRED`.

## 2. Review Gate
Promotion requires explicit sign-off from an authorized human operator (`CREATIVE_DIRECTOR`, `BRAND_EXECUTIVE`, `STUDIO_LEAD`, `SUPER_ADMIN`).

## 3. Rollback Runbook
If promoted knowledge introduces aesthetic drift, regression, or customer dissatisfaction:
1. Operator invokes `/learning/promotions/{id}/rollback`.
2. The knowledge object's `is_active` flag is immediately set to `False`.
3. Historical campaign records remain intact (never destroyed).
4. A `knowledge_rolled_back` telemetry audit event is emitted.

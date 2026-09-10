# Phase 25: Reliability Center Subsystem Report

## 1. Overview
The Reliability Center (`src/reliability_center/`) tracks system-level Service Level Objectives (SLOs), error budgets, latency distributions, active incident logs, and automated rollback health.

## 2. Key Projections & Metrics
- **SLO View (`slo_view.py`)**: Monitors target availability (99.9%) against current rolling availability, latency p95 and p99 thresholds.
- **Error Budget View (`error_budget_view.py`)**: Computes remaining error budget percentage and burn rates.
- **Rollback & Canary View (`rollback_view.py`)**: Observes active canary rollouts, threshold anomalies, and rollback trigger readiness.

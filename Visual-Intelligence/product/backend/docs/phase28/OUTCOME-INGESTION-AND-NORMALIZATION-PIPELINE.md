# Phase 28: Outcome Ingestion & Normalization Pipeline

## 1. Multi-Channel Ingestion Architecture
Raw outcome feeds from Shopify, Meta Ads, Google Analytics, and Digital OOH sensors are ingested via `OutcomeIngestionPipeline` with cryptographic source signature verification.

## 2. Metric Normalization Engine
Raw telemetry is mapped to canonical normalized metrics without losing source platform semantics:
- **`IMPRESSIONS`:** Absolute reach volume.
- **`CTR`:** $\mathrm{Clicks} / \mathrm{Impressions}$.
- **`CONVERSION_RATE`:** $\mathrm{Conversions} / \mathrm{Clicks}$.
- **`AVG_DWELL_TIME_SEC`:** Duration in seconds.
- **`SENTIMENT_POSITIVE_RATIO`:** Natural language sentiment polarity.

All normalized metrics preserve their origin platform, normalization rule, and time window (`7_DAY_POST_LAUNCH`, `30_DAY_POST_LAUNCH`).

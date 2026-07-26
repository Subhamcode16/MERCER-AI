# Atelier OS — MVP Checklist

This document tracks the end-to-end progress of the Atelier OS backend build. It is the single source of truth for what has been built, what is in progress, and what remains for MVP launch.

## 🏗️ Phase 0: Foundation [COMPLETED]
- [x] Scaffolding: FastAPI structure, Motor async driver, Pydantic settings.
- [x] Database: MongoDB connection lifespan, index creation on startup.

## 🔒 Phase 1: Identity & Auth Layer [COMPLETED]
- [x] JWT Utility: Local verification of Supabase HS256 tokens (no network call).
- [x] Auth Dependencies: `get_current_user` enforcing DB-backed entitlements.
- [x] Email Gate: Reject unverified free-tier users.
- [x] Provision Endpoint: `POST /auth/provision` — idempotent user upsert and initial 20 credit grant with ledger integration.

## 👤 Phase 2: Profiles & Entitlements [COMPLETED]
- [x] Profile Endpoint: `GET /users/me` returning current tier, credits, and basic metadata.
- [x] Transaction Ledger: Return recent credit ledger activity (grants, usage) for the user dashboard.

## 🧠 Phase 3: Generation Layer [COMPLETED]
- [x] Provider Setup: Google GenAI (Gemini) API key configuration.
- [x] Generation Router: `POST /generate/{model}` (e.g., Nano Banana 2).
- [x] Billing Engine: Phase 1 (Reserve) -> Call API -> Phase 2 (Commit/Refund) pattern.
- [x] Rate Limiting: Strict limits using SlowAPI to prevent abuse.

## 💳 Phase 4: Payments & Webhooks [COMPLETED]
- [x] Payment Provider Setup (Stripe).
- [x] Checkout Endpoint: Generate subscription or top-up checkout links.
- [x] Webhook Handler: Verify signatures and process `checkout.session.completed`.
- [x] Subscription Upgrades: Upgrade user tier and grant monthly credits via the ledger.

## 🔄 Phase 5: Jobs & Asynchronous Polling [COMPLETED]
- [x] Job State Machine: Tracking queued -> running -> completed -> failed.
- [x] Polling Endpoint: `GET /jobs/{job_id}` for the client to retrieve completed images.
- [x] Callbacks (Optional): Provider webhooks for async models.

## 📊 Phase 6: Admin & Telemetry [COMPLETED]
- [x] Admin Gate: Route dependency requiring `user.role == 'admin'`.
- [x] Dashboard Metrics: Aggregated usage, cost, and user growth endpoints.
- [x] Internal Logging: Structured logging of generation latencies and failure rates.

## 🚀 Phase 7: Deployment & Hardening [PENDING]
- [ ] CORS & Security Headers.
- [ ] Production Environment Checks (Render/Vercel readiness).
- [ ] Load Testing (Database pooling limits).

---
*Next milestone:* Completing Phase 7 (Deployment & Hardening) and integrating the frontend polling system for generation requests.

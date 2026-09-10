# Atelier OS — Backend Product Understanding

> This document explains the backend architecture in plain terms, mapped directly to the user experience defined in `user-flow.md`. Every technical decision here exists to serve one principle:
>
> *"The user journey should never feel like using software."*

---

## What We Are Building

A **multi-model AI image generation SaaS backend** — credit-based, 4-tier, 2 AI providers (OpenAI + Google Gemini), with a batch queue system for cost optimisation.

**Stack:**
- **FastAPI** — Python web framework (backend)
- **MongoDB** — Primary database (credit ledger + job queue)
- **Supabase** — Auth (JWT tokens, user identity)
- **Cloudflare R2** — Object storage (generated images, signed expiring URLs)
- **Razorpay** — Primary payment processor (India: UPI, cards, netbanking, wallets)
- **Stripe** — Secondary payment processor (international cards)
- **Docker + Supervisor** — Deployment and process management
- **OpenAI** — GPT Image 2 model
- **Google Gemini API** — Nano Banana 2 (NB2) + Nano Banana Pro (NB Pro) models

---

## The 5 Interlocking Systems

### 1. Auth Layer — The Moment the User Arrives

**User flow**: User enters Atelier. No tutorial, no friction.

**Backend reality**: Supabase handles authentication and issues JWT tokens. The moment a user makes any request, the FastAPI backend validates their identity and immediately looks up server-side:
- Their **tier** (Free / Starter / Pro / Studio)
- Their **credit balance**

The client never tells us who the user is or what they're allowed to do. Supabase provides identity. MongoDB provides entitlements. These are resolved on the server on every single request — no exceptions.

---

### 2. The Credit Machine — When the User Starts Generating

**User flow**: User drags image → material intelligence activates → moodboards generate → assets appear progressively.

**Backend reality**: Every generation request passes through a strict 3-phase pipeline.

```
PHASE 1: RESERVE
  → Atomic credit hold using MongoDB's $gte + $inc
  → If balance < cost: reject cleanly. User sees a calm, clear message.
  → If sufficient: credits are held immediately and atomically.
  → Two concurrent requests from the same user CANNOT both pass this check.

PHASE 2: CALL
  → Provider API is called (OpenAI or Gemini)
  → Standard calls: seconds
  → Batch calls: minutes (Studio tier)

PHASE 3: COMMIT or RELEASE
  → Success? A "commit" ledger entry is written. Charge is confirmed.
  → Error? Credits are returned via a "release" entry. User is never charged for failures.
```

**The two-collection ledger design:**

| Collection | Purpose |
|---|---|
| `users.credit_balance` | Fast cache — what the UI displays |
| `credit_transactions` | Append-only truth — what actually happened, immutable, auditable forever |

If the two ever disagree, the ledger wins. This is what makes billing disputes possible to resolve and audits possible to run.

**One critical rule**: Prompt moderation runs **before** the reserve step. If a prompt is blocked, zero credits are spent and no API call is made. The user gets a clean, calm rejection with a clear next step.

---

### 3. The Routing Logic — Which Model Runs When

**User flow**: User accepts a creative direction → moodboards begin generating → visual concepts appear.

**Backend reality**: The routing function `resolve_call_params(tier, model, urgent)` makes every decision before a single API call is made.

| Tier | NB Pro Access | Mode | Resolution |
|---|---|---|---|
| Free | Locked | — | — |
| Starter | Preview only | Standard (real-time) | 1024px |
| Pro | Full access | Standard (real-time) | 2048px |
| Studio | Full access | Batch by default | 2048px |

**Credit costs per generation:**
- Nano Banana 2 → 2 credits
- GPT Image 2 (medium) → 2 credits
- NB Pro (1K preview) → 3 credits
- NB Pro (2K full) → 4 credits
- Credit anchor: 1 credit ≈ $0.017 raw API cost

For Studio users, the generation is not instant — it enters a queue. The user-flow says "loading never feels empty — the interface reveals Atelier's thinking." The batch status feeds the frontend so the user sees the process unfolding rather than staring at a spinner.

---

### 4. The Batch Pipeline — Making Long Waits Invisible

**User flow**: "Generation complete." A passive notification. The creative flow never leaves the campaign.

**Backend reality**: The most complex piece of the system.

```
User triggers generation (Studio, non-urgent)
        ↓
Job written to MongoDB generation_jobs (status: "queued")
        ↓
User continues working — workspace is never blocked
        ↓
batch_worker.py (Supervisor-managed process, rolling window every 15-30 min)
        ↓
Jobs grouped by provider → submitted as batch to OpenAI or Gemini
        → ~50% cost discount vs standard API calls
        ↓
Worker polls for completion → image stored in Cloudflare R2
        ↓
WebSocket / SSE notification → "Generation complete"
        ↓
User clicks result — it's already there, retrieved via signed expiring URL
```

**Job lifecycle states:**
```
submitted → queued → batched → sent_to_provider → polling → completed | failed → credited | refunded → delivered
```

**Why rolling window (not nightly batch):**
Providers offer up to 24h turnaround, but users won't accept a next-day delivery for image generation. Submitting every 15-30 min captures the ~50% discount while delivering results in minutes, not hours.

**Partial failure handling:**
If you batch 50 jobs and 3 fail, the other 47 still succeed. Credits are refunded per item, not per batch. The user flow says "every error explains what happened, why, how to recover" — the backend surfaces which specific job failed with a clean, non-technical message.

---

### 5. The Payment Layer — What Triggers Credits

**User flow**: The user never thinks about this. It just works.

**Backend reality**: Two payment processors, one unified credit ledger.

| Processor | Audience | Methods |
|---|---|---|
| Razorpay | Indian customers | UPI, cards, netbanking, wallets |
| Stripe | International | Cards (when invite access arrives) |

Both fire webhooks when a payment succeeds. The backend has three non-negotiable rules:

**Rule 1 — Only confirmed-charge events grant credits.**
Never grant on "payment initiated" or "checkout started." Only on the confirmed-charge event specifically.

**Rule 2 — Webhook idempotency.**
Both Razorpay and Stripe redeliver events (at-least-once delivery). Grant logic keys off the provider's event ID — a redelivered subscription.charged must not double-grant credits.

**Rule 3 — PaymentProvider abstraction.**
Both processors implement a common internal interface. The credit-granting code calls one method regardless of which provider fired the webhook — the ledger stays unified, the code never forks into parallel paths.

**Every credit grant carries a source tag:**
- source: "razorpay" or source: "stripe" → subscription renewal
- source: "purchase" → manual top-up

This tag is what lets you reconcile "credits granted" against "payments received" per provider when webhook timings don't line up.

---

## The Security Layer — What the User Never Sees

**User flow**: The user feels nothing. That's the point.

| Layer | What It Does |
|---|---|
| Supabase JWT | Every /generate route requires authentication — no anonymous generation possible |
| Server-side tier lookup | The server reads tier from the database on every request — client claims are ignored |
| slowapi rate limiter | Per-user, tier-based limits — one account cannot burn the org-level provider quota |
| Provider semaphore | Caps concurrent outbound calls to OpenAI/Gemini — protects against traffic spikes getting us throttled |
| Email verification gate | Free tier credits don't activate until email is verified — prevents multi-account farming |
| Prompt moderation | OpenAI moderation endpoint + Gemini safety settings run before any credit is reserved |
| Cloudflare R2 signed URLs | Generated images are never in a permanently public bucket — URLs expire |
| Webhook signature verification | Razorpay (X-Razorpay-Signature HMAC-SHA256) and Stripe (Stripe-Signature) verified on every webhook before the payload touches the credit ledger |
| Immutable ledger | credit_transactions entries are never updated or deleted — only new offsetting entries are inserted |

---

## The Tier Table — Business Logic at a Glance

| | Free | Starter | Pro | Studio |
|---|---|---|---|---|
| Monthly price | $0 | $12/mo | $35/mo | $85/mo |
| Credits | 20 (one-time, 14-day expiry) | 200/mo | 800/mo | 2,500/mo |
| Nano Banana 2 | 10 images | 100 images | 400 images | 1,250 images |
| GPT Image 2 | 10 images | 100 images | 400 images | 1,250 images |
| NB Pro | Locked | 50 images (preview) | 200 images | 625 images (batch default) |
| Raw API cost to us | ~$0.50 worst case | ~$3.40/mo | ~$13.60/mo | ~$42.50/mo |
| Margin | Acquisition cost | 2.65x | 2.0x | 1.53x |

Studio's 1.53x margin is only sustainable because NB Pro runs through the Batch API by default — saving ~50% on the most expensive model.

---

## What This Means for the Creative Experience

The backend's entire job is to ensure that **whatever the user does in the creative workspace — generate, explore, refine, review — happens with the right model, at the right cost, within their tier's limits, without them ever feeling any of the complexity underneath.**

When the user flow says:
- "The user never waits for setup" → Auth + tier resolution happens in milliseconds on the server
- "Everything begins automatically" → Credit reservation is atomic and instant
- "Loading never feels empty" → Batch job status is always surfaced, never hidden
- "Failures remain calm" → Every error path (insufficient credits, failed generation, blocked prompt) produces a human-readable outcome with a clear recovery path
- "Returning to the campaign feels instantaneous" → Session state + generation results are persisted in MongoDB and R2, restored on demand

The philosophy of the product and the architecture of the backend are the same thing, expressed in two different languages.

---

*This document is a living reference. Update it as architecture decisions evolve.*
*Cross-references: pricing-tier.md, credit-system.md, api-calling.md, api-connection.md, batch-processing.md, security-checklist.md, user-flow.md*

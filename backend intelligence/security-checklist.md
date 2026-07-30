# Security Checklist — Pre-Deployment

Covers API key handling, rate limiting, abuse prevention, and general SaaS hardening for the image-gen app. Organized so you can work through it as a literal checklist before going live.

## 1. API key management

- [ ] OpenAI and Gemini keys never appear in frontend code, mobile bundles, or client-visible network requests — every provider call is proxied through your FastAPI backend
- [ ] Keys stored in environment variables loaded via Supervisor's config, not hardcoded or committed — confirm `.env` is in `.gitignore`
- [ ] Separate keys per environment (dev/staging/prod) — a leaked dev key shouldn't touch production spend
- [ ] Use a secrets manager (AWS Secrets Manager, or Hetzner-equivalent + Vault) once you have more than one server pulling the same keys — env files don't scale past a single box
- [ ] Rotation plan: if a key is ever exposed (logged, committed, leaked), you should be able to revoke and replace it within minutes, not hours — keep the provider console access documented and tested, not theoretical

## 2. Auth on every generation endpoint

- [ ] JWT/session auth required on all `/generate` routes — no anonymous generation
- [ ] User's tier is looked up server-side from your database on every request — never trust a `tier` field sent from the client
- [ ] Credit balance check happens server-side at reservation time (see `credit-system.md`) — client-side balance display is UX only, not enforcement

## 3. Rate limiting

Two layers, both needed:

- **Per-user, tier-based**: cap requests/minute per user so one account can't burn through a provider's org-wide rate limit alone. Token-bucket or sliding-window, keyed by `user_id`. A lightweight in-process limiter (e.g. `slowapi`) is fine at your current scale; move to a Redis-backed limiter once you run more than one API instance, since in-process counters don't share state across processes.
- **Global, provider-level**: OpenAI and Gemini rate limits apply at your org level, not per end-user (see `api-connection.md`). Put a queue or semaphore in front of outbound calls so a traffic spike on your side doesn't get you throttled or banned by the provider — this is separate from the batch queue and applies to real-time (`urgent=True`) calls too.

```python
# sketch — semaphore limiting concurrent outbound calls per provider
openai_semaphore = asyncio.Semaphore(5)   # tune to your current IPM tier

async def call_openai(payload):
    async with openai_semaphore:
        return await client.images.generate(**payload)
```

- [ ] Rate limit responses return a clear `429` with retry-after, not a silent failure

## 4. Abuse and fraud prevention

- [ ] Signup requires email verification before any free-tier credits are granted — prevents disposable-account credit farming
- [ ] Velocity check: flag/block accounts creating many sessions from the same IP or device fingerprint in a short window
- [ ] Prompt/content moderation runs **before** credit reservation — reject disallowed content at validation, don't spend a user's credits (or your API cost) generating something you'll block on delivery. Use OpenAI's moderation endpoint and Gemini's built-in safety settings.
- [ ] Log and alert on anomalous burn rate (a single user consuming far more credits/hour than your tier limits should allow points to a bug or an exploit, not normal usage)

## 5. Data handling

- [ ] Don't log full prompts or generated images in application logs — logs should reference job IDs, not payload content, especially since prompts may contain user-submitted PII
- [ ] MongoDB: enable encryption at rest, restrict network access to app servers only (no public bind), use role-scoped DB users rather than one root credential
- [ ] TLS everywhere — API, webhooks, object storage URLs. No plaintext HTTP anywhere in the path
- [ ] Generated images stored in object storage (S3-compatible) with signed, expiring URLs — not permanently public buckets
- [ ] Define and enforce a retention policy for generated content and prompts; don't keep everything forever by default

## 6. Webhook security (billing + batch completion)

- [ ] Verify signatures on every incoming webhook before processing — never touch the credit ledger from a payload that hasn't passed signature check
  - **Razorpay**: verify `X-Razorpay-Signature` header via HMAC-SHA256 against your webhook secret (`razorpay.Utility.verify_webhook_signature`) — reject anything that fails, don't log-and-continue
  - **Stripe** (if/when the invite comes through): verify via `Stripe-Signature` header using `stripe.Webhook.construct_event`, same reject-on-failure rule
  - Any batch-completion webhook you wire up from OpenAI/Gemini gets the same treatment — signature or shared-secret check before the payload touches job status
- [ ] Webhook endpoints are not the same as your public API — separate route, separate rate limit, reject anything that doesn't pass signature check before touching the credit ledger
- [ ] Idempotency on webhook delivery: both Razorpay and Stripe can and will redeliver the same event (network retries, at-least-once delivery) — key your grant logic off the provider's event ID, not just "webhook arrived," so a redelivered `subscription.charged` doesn't double-grant credits

## 7. Payment handling

- [ ] Never store raw card data — use Razorpay's/Stripe's own tokenization exclusively, card details never touch your servers
- [ ] Razorpay as primary for Indian customers (UPI, cards, netbanking, wallets — Stripe India is invite-only and card-only, which excludes UPI users); Stripe as a secondary path for international cards if/when you get access
- [ ] Abstract both providers behind one internal interface (e.g. a `PaymentProvider` class each implements) so your credit-granting code calls one method regardless of which provider fired the webhook — keeps `credit-system.md`'s grant logic from forking into two parallel code paths
- [ ] Subscription state (tier, renewal date) driven by payment processor webhooks, not client-side confirmation — for either provider
- [ ] Reconcile credit grants against actual successful payment webhooks — don't grant credits on an optimistic "checkout started" or "payment initiated" event, wait for the confirmed-charge event specifically

## 8. Infra hardening (EC2/Hetzner + Docker + Supervisor)

- [ ] Firewall: only expose ports actually needed (443/80 to the world, DB ports restricted to internal network only)
- [ ] Docker images: use minimal base images, scan for known CVEs before deploy, don't run containers as root
- [ ] Supervisor-managed processes run with least-privilege system users, not root
- [ ] Keep OS and dependency patches current — set a recurring reminder, this is the check most likely to silently lapse on a solo-founder setup
- [ ] SSH: key-only auth, no password login, restrict to known IPs where possible

## 9. Monitoring and incident response

- [ ] Cost-spike alert: if daily provider spend (OpenAI + Gemini combined) exceeds your expected ceiling by some threshold (e.g. 2x rolling average), get paged, not surprised by the invoice
- [ ] Error-rate alert on generation failures — a spike often means a provider outage or a broken auth key, and you want to know before users do
- [ ] Documented runbook: what to do if a key leaks, if the ledger drifts from the cached balance (see reconciliation job in `credit-system.md`), if a provider goes down mid-batch
- [ ] Status page or at minimum a way to communicate outages to users — image generation failures are visible and users will ask

## 10. Compliance basics

- [ ] Terms of Service covering AI-generated content ownership, acceptable use, and moderation policy
- [ ] Privacy policy disclosing that prompts/images are sent to third-party providers (OpenAI, Google) for processing
- [ ] If serving EU users: GDPR basics — data deletion on request, documented data processing agreement coverage from OpenAI/Google's own DPAs
- [ ] DMCA/takedown process if user-generated content could infringe copyright
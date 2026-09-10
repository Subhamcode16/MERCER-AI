# Pricing Tiers

Credit-based pricing across three models: **Nano Banana 2** (Gemini 3.1 Flash Image), **Nano Banana Pro** (Gemini 3 Pro Image), **GPT Image 2** (OpenAI). One credit currency, spendable across any model. Four tiers: Free, Starter, Pro, Studio.

## Credit costs per generation

| Model | Resolution | Raw API cost (Batch) | Credits/gen |
|---|---|---|---|
| Nano Banana 2 | 1K | ~$0.034 | 2 |
| GPT Image 2 | Medium 1K | ~$0.027 | 2 |
| Nano Banana Pro | 2K | ~$0.067 | 4 |

Credit anchor: **1 credit ≈ $0.017 raw cost**

## Tier table

| | Free | Starter | Pro | Studio |
|---|---|---|---|---|
| Monthly price | $0 | $12/mo | $35/mo | $85/mo |
| Annual price | — | $9/mo ($108/yr) | $27/mo ($324/yr) | $65/mo ($780/yr) |
| Annual discount | — | 25% | 23% | 24% |
| Credits | 20, one-time | 200/mo | 800/mo | 2,500/mo |
| Renewal | none — 14-day expiry | monthly | monthly | monthly |
| Nano Banana 2 (2 cr) | 10 images | 100 images | 400 images | 1,250 images |
| GPT Image 2 (2 cr) | 10 images | 100 images | 400 images | 1,250 images |
| Nano Banana Pro (4 cr) | locked | 50 images | 200 images | 625 images |
| Raw API cost to us | ~$0.35-0.53 worst case | ~$3.40/mo | ~$13.60/mo | ~$42.50/mo |
| Margin (annual) | acquisition cost, not margin | 2.65x | 2.0x | 1.53x |

## Access rules by tier

- **Free**: one-time 20 credits, no renewal, expires 14 days after signup. Nano Banana 2 and GPT Image 2 only, real-time, standard resolution. Nano Banana Pro fully locked — no preview override, since even one uncapped Pro generation on a disposable free account is an easy abuse vector. Requires verified email before credits activate, to blunt multi-account farming.
- **Starter**: Nano Banana Pro capped at low-res preview only, no 4K, no Batch queueing (real-time only, keeps latency low but cost-controlled since volume is naturally low)
- **Pro**: All three models unlocked at full resolution. Nano Banana Pro real-time by default.
- **Studio**: All models unlocked. Nano Banana Pro routed through **Batch API by default** for anything not flagged urgent — this is what keeps the 1.53x margin sustainable at this price point. Real-time available as an explicit opt-in per request (still deducts the same credits, just skips the queue).

## Design rationale

- Free tier isn't margin-bearing — it's a bounded acquisition cost (~50-70 cents worst case per signup), kept cheap by locking Nano Banana Pro entirely and expiring unused credits after 14 days so it can't be farmed as an ongoing free-generation source.
- Margin decreases as tier increases — Starter subsidizes acquisition, Studio is priced close to cost and retained through volume + retainer relationships, not per-unit markup.
- Breakage assumption: Starter users historically don't exhaust pools; don't rely on this holding for Pro/Studio.
- Any future 4th model gets slotted into this same credit currency — price its credits at raw-batch-cost / $0.017, round to nearest whole credit.
- Revisit this table if Google or OpenAI change per-token rates — it's pinned to API pricing as of July 2026.

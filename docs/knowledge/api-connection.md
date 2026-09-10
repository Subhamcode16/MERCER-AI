# API Connection Setup

Two providers to connect: **OpenAI** (GPT Image 2) and **Google Gemini API** (Nano Banana Pro, Nano Banana 2).

## OpenAI — GPT Image 2

**Model ID**: `gpt-image-2`

1. Create an API key at platform.openai.com → API keys
2. New accounts start on rate-limit Tier 1. Image-per-minute (IPM) limits scale with cumulative spend — if Studio-tier batch jobs need high throughput, factor in a ramp period (~$100 spend to reach Tier 3, per OpenAI's tiering).
3. Install SDK:
   ```bash
   pip install openai --break-system-packages
   ```
4. Env vars:
   ```bash
   OPENAI_API_KEY=sk-...
   ```
5. Client init:
   ```python
   from openai import OpenAI
   client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
   ```

**Rate limit note**: limits apply at the org level, not per end-user. If your app serves concurrent users, all their requests share one quota pool — build a request queue in front of this, don't let user traffic hit OpenAI directly.

## Google Gemini API — Nano Banana Pro & Nano Banana 2

**Model IDs**:
- Nano Banana Pro → `gemini-3-pro-image-preview`
- Nano Banana 2 → `gemini-3.1-flash-image`

Two integration paths:
- **Gemini Developer API / AI Studio** — simpler, API-key auth, recommended starting point
- **Vertex AI** — needed only if you require GCP IAM, project-level governance, or are already on Vertex for other services

1. Get an API key at aistudio.google.com/apikey (Developer API path)
2. Install SDK:
   ```bash
   pip install google-genai --break-system-packages
   ```
3. Env vars:
   ```bash
   GEMINI_API_KEY=...
   ```
4. Client init:
   ```python
   from google import genai
   client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
   ```

## Environment file (all providers)

```bash
# .env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# internal routing config
NB_PRO_BATCH_DEFAULT=true      # Studio tier: route NB Pro through Batch unless urgent=true
NB_PRO_MAX_RESOLUTION_STARTER=1024   # cap Starter tier resolution
```

## Secrets handling

- Never commit `.env` — confirm it's in `.gitignore`
- On EC2/Hetzner: load via Supervisor's environment config or a secrets manager, not hardcoded in the FastAPI app
- Rotate keys if any are ever logged — both OpenAI and Gemini image responses can include prompt echoes in error payloads; make sure your logging layer redacts request bodies, not just keys

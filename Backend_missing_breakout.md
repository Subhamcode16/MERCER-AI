1. Backend Orchestration (ORRA Loop Integration)
Status: The individual LLM adapters (VisionAdapter, PromptEngine, and KnowledgeAdapter) are fully implemented and set up with Google Gemini API waterfall calls. However, they are currently bypassed/mocked inside the main orchestrator (OrraLoop class in app/services/orra_loop.py).
What's Left:
Connect observe(): Wire the OBSERVE phase to call self.vision.analyze_product(image_path) rather than returning hardcoded textile attributes.
Connect reason(): Wire the REASON phase to query the KnowledgeAdapter to fetch the markdown ontologies from the Obsidian vault and run PromptEngine.generate_recommendations() via Gemini.
Connect act(): Wire the ACT phase to compile actual generative prompts from the user selections, the Obsidian material physics, and the Honcho user memory using PromptEngine.generate_campaign_assets().

2. Live Rendering Engine Integration
Status: The ACT phase in the backend currently simulates image generation by returning mock filenames (["hero_image.png", "closeup.png"]) without producing actual image assets.
What's Left:
Integrate an external image rendering provider (such as Fal.ai, Flux, Midjourney API, or custom Stable Diffusion pipelines) to receive the compiled generation prompts and return high-fidelity rendered campaign assets.
Download and store the generated assets in the campaign folder so they display on the frontend "Generated Assets" screen.

3. Database Migration (Local JSON to MongoDB)
Status: The app has a configured MongoDB database setup (app/database.py) with optimized indexes for audit ledgers, workspaces, and users, but the campaigns themselves are still stored as local JSON files (data/campaign_*.json) inside the LocalStore module.
What's Left:
Swap LocalStore in local_store.py to store campaign documents in a MongoDB collection (e.g. db.campaigns). This will enable multi-user support, fast queries, and reliable data persistence.

4. Cloud Asset Storage Migration
Status: Fabric images and campaign folders are saved locally to data/assets/ via AssetStore. In cloud environments (such as Render or AWS ECS), local container storage is ephemeral and will be wiped on restarts.
What's Left:
Replace the local AssetStore with a cloud object storage client (e.g. AWS S3 or Supabase Storage) to upload images and return secure, signed CDN URLs for the frontend to render.

5. WebSockets/SSE Streaming for AI Thoughts
Status: The frontend relies on HTTP polling (setInterval every 2.5 seconds) to check campaign updates.
What's Left:
Implement WebSockets or Server-Sent Events (SSE) in the backend to stream the cognitive progress of the ORRA loop (e.g. observation logs, reasoning steps, recommendation explanations) in real time to the frontend Creative Dialogue drawer.

6. Authentication Middleware & Row-Level Security
Status: The frontend has an authentication shell (AuthContext), but the backend campaign router endpoints are completely public and lack request validation.
What's Left:
Add a JWT verification middleware in FastAPI to validate Supabase authentication tokens on every incoming request.
Update database calls to restrict campaign creation, modification, and access to the authenticated owner.

7. Credit & Billing System Enforcement
Status: The database has schemas for credit_transactions and unique idempotency keys to prevent double spending, but the logic is not yet enforced.
What's Left:
Check user credit balances before launching /generate jobs.
Implement Stripe webhooks to fund user accounts, and deduct credits upon successful asset generation.
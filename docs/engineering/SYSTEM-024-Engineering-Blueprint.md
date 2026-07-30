# SYSTEM-024 — Engineering Blueprint
**Layer:** Engineering Intelligence (Build)
**Agent:** `system-architect`
**Movement:** I — The Threshold

---

## 1. Repository Structure
- Monorepo approach using Turborepo (or standard npm workspaces).
- Separation of `apps/web` (Next.js) and `packages/ui` (Shared styles).

## 2. CI/CD Pipeline
- **Host:** Vercel (for Next.js Edge caching and Server Components).
- **Checks:** 
  - Strict TypeScript compilation (`tsc --noEmit`).
  - ESLint (with strict rules against `any` and unoptimized images).
  - Prettier enforcement.

## 3. Asset Delivery
- All `.glb` models, KTX2 textures, and large video assets must be served from a dedicated global CDN (e.g., AWS CloudFront or Vercel Blob) to bypass the 1MB Serverless Function limits and ensure fast global Time-To-First-Byte (TTFB).

## 4. Environment Variables
- Strict separation of `NEXT_PUBLIC_` variables for the client.
- CMS integration keys must never leak to the client bundle.

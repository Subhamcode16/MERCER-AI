# PRD-001: Campaign Creation & Orchestration

## 1. Overview
The core value of the Visual Intelligence Platform is moving from single-image generation to multi-asset **Campaigns**. A Campaign ensures that multiple outputs (Hero Image, Close-up, Lifestyle) maintain perfect visual consistency and inherit the same brand aesthetic (Reference DNA) and physical product attributes (Product DNA).

## 2. Goals
- Eliminate single-shot prompt engineering.
- Implement a 4-phase Campaign Lifecycle: Identity → Planning → Execution → Evaluation.
- Support parallel generation of independent assets via a Dependency Graph.
- Introduce **Asset DNA** so individual assets can override composition, lighting, and framing while inheriting the core Campaign DNA.

## 3. Architecture

### 3.1 Campaign Lifecycle Schema
Every Campaign transitions through four distinct phases:

1. **Identity Phase**: Establishes *what* we are shooting and for *whom*.
   - **Product DNA**: Physical constraints (material, weaving technique, features).
   - **Reference DNA**: Brand identity (preferred lighting styles, color grading from moodboards).
   
2. **Planning Phase**: Establishes *why* and *how*.
   - **Creative Objective**: e.g., "Luxury Editorial", "High-Volume Catalog".
   - **Dependency Graph**: Defines the sequence of asset generation.
     - `hero_image`: `[]` (Starts immediately)
     - `closeup_image`: `[]` (Starts immediately)
     - `lifestyle_image`: `[]` (Starts immediately)
     - `reel_storyboard`: `["hero_image"]` (Waits for hero image)
     
3. **Execution Phase**: The translation of constraints into renderer prompts.
   - **Campaign State**: The global solver output applying physics and visual craft rules.
   - **Asset States**: Each asset inherits the Campaign State but applies **Asset DNA** overrides.
     - *Example*: The Campaign State defines "hard directional light" based on the material (Silk Zari), but the `closeup_image` Asset DNA overrides the camera framing to "macro lens, shallow depth of field".

4. **Evaluation Phase**: Capturing structured feedback.
   - See **PRD-004: Evaluation Dashboard** for the schema on rich feedback (Severity, Reason, Desired Outcome).

## 4. API Specification (Internal)

### `POST /api/campaigns`
**Request Payload:**
```json
{
  "project_id": "proj_123",
  "product_id": "prod_001",
  "creative_objective": "luxury_bridal",
  "assets_requested": ["hero_image", "closeup_image", "lifestyle_image"]
}
```

**Response Payload:**
Returns the initialized `Campaign` object with `status: planning`.

### `POST /api/campaigns/{id}/execute`
Begins the parallel execution pipeline. The runtime traverses the Dependency Graph, resolving the solver for each asset and dispatching jobs to the Image Generator (or queuing them sequentially if API rate limits require it in dev).

## 5. Acceptance Criteria
- [ ] The `Campaign` object successfully stores Product DNA and Reference DNA in its Identity block.
- [ ] The Dependency Graph correctly identifies which assets can be generated in parallel vs sequentially.
- [ ] Asset DNA overrides successfully merge with the Campaign State (e.g., changing composition without losing the physical lighting constraints).
- [ ] The output JSON matches the 4-phase schema exactly.

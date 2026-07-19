# PRD-003: Asset Workspace

## 1. Overview
The Asset Workspace is the core execution interface for the MVP. Once a Campaign is planned, the user enters the workspace to generate, review, and approve the individual assets (e.g., Hero Image, Close-up, Lifestyle). This is where the Feedback Flywheel (Phase 3) captures data on rejections.

## 2. Goals
- Provide a clean, dark-mode, glassmorphism UI that feels premium and luxury-oriented.
- Allow users to execute the dependency graph (generate assets in parallel).
- Expose the "Engine Room" conditionally for power users who want to see the *Creative Decision Trace*.
- Capture rich, structured feedback when an asset is rejected.

## 3. Core Features

### 3.1 The Campaign Board
A visual kanban-style or grid layout showing all requested assets:
- **Hero Image** [Status: Generating...]
- **Product Close-up** [Status: Pending]
- **Lifestyle** [Status: Completed]

### 3.2 Asset Review Modal
When an asset finishes generating, the user clicks it to review.
**Primary Actions:**
1. **Approve**: Locks the asset, saves the prompt + image + Creative State as a "Verified Pattern".
2. **Reject & Adjust**: Opens the Feedback Form (The Flywheel).

### 3.3 The Engine Room (Collapsible Panel)
A toggleable side panel showing the underlying logic for the generated asset:
- **Asset DNA**: Inherited Campaign constraints + local overrides.
- **Physics Solver Output**: Computed lighting direction, reflectance, and camera settings.
- **Visual Craft Output**: Render intent and styling choices.
*Value Proposition*: Proves to the user that the system is reasoning, not just passing prompts to a black box.

## 4. The Feedback Flywheel (Rejection Flow)
When rejecting an asset, the user does not type a new prompt. They provide structured feedback:

**UI Flow:**
1. Select Category: [Lighting] [Composition] [Color] [Realism] [Fabric Accuracy]
2. Select Severity: [1 - Minor Tweak] to [5 - Completely Wrong]
3. Select Desired Outcome: (e.g., "More metallic separation", "Softer shadows")
4. **Action**: The system translates this feedback into a `suggested_solver_adjustment` and re-runs the asset generation.

## 5. API Specification (Internal)

### `POST /api/campaigns/{id}/assets/{asset_id}/feedback`
**Request Payload:**
```json
{
  "category": "lighting",
  "severity": 4,
  "reason": "Flat",
  "desired_outcome": "More metallic separation"
}
```

**Response Payload:**
Returns the updated Asset state (now `status: generating`) and logs the feedback to `feedback_log.json`.

### `POST /api/campaigns/{id}/assets/{asset_id}/approve`
**Response Payload:**
Locks the asset and saves the Verified Pattern for future learning.

## 6. Acceptance Criteria
- [ ] Users can trigger generation for all assets in the Campaign Plan.
- [ ] Users can view the Engine Room (Creative Decision Trace) for any generated asset.
- [ ] Users can submit structured feedback on rejection, which correctly updates the backend feedback log.
- [ ] Approving an asset locks it and contributes to the Campaign's overall completion status.

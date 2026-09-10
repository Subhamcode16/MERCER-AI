I actually like this roadmap much more than I expected.

It shows a healthy shift in mindset:

* **Research is frozen.**
* **Engineering begins.**

That's exactly what I wanted to see.

That said, I'd change a few important things before you commit to implementation.

---

# Overall Score

**9.8/10**

The missing 0.2 has nothing to do with the engine.

It's about product engineering.

---

# 1. I would NOT use Gemini as the only VLM.

This is probably the biggest change I'd make.

Your architecture has become renderer-agnostic.

Your analysis pipeline should also become model-agnostic.

Instead of

```text
Gemini

↓

Product DNA
```

I'd build

```text
Vision Adapter

↓

Gemini

GPT-4.1 Vision

Qwen-VL

InternVL

Molmo

↓

Normalized Knowledge Claims
```

Exactly like you did with renderers.

Future-proof from day one.

---

# 2. Campaign State needs another object.

Current

```yaml
Campaign

Product DNA

Creative Objective

Creative State

Assets
```

I'd add

```yaml
Campaign

Identity

↓

Planning

↓

Execution

↓

Evaluation
```

For example

```yaml
Campaign

CampaignPlan

Creative Objective

Campaign State

Asset States

Evaluation

Feedback
```

This separation becomes useful once campaigns have

* 20 images
* videos
* reels
* carousels

---

# 3. Don't generate assets sequentially.

I know the roadmap says

```text
Generate Hero

↓

Close-up

↓

Lifestyle
```

I would instead build

```text
Campaign Plan

↓

Dependency Graph

↓

Parallel Generation
```

Example

Hero

↓

Close-up

↓

Detail Shot

can all run simultaneously.

Only

Storyboard

depends on Hero.

---

# 4. I think you're missing Asset DNA.

This is a very important concept.

Suppose

Campaign

contains

```text
Hero

Close-up

Lifestyle
```

Each asset inherits

Campaign DNA

BUT

has its own

Asset DNA.

Example

```yaml
Hero

Composition

Centered

Lighting

Editorial

```

Close-up

```yaml
Macro

Texture

Microcontrast

Embroidery
```

Lifestyle

```yaml
Movement

Story

Environment
```

That prevents overrides from becoming messy.

---

# 5. Phase 3 (Feedback)

I would capture much richer feedback.

Instead of

```json
Lighting

Wrong
```

I'd capture

```yaml
Feedback

Category

Lighting

Severity

4

Reason

Flat

Desired Outcome

More metallic separation

Suggested Solver Adjustment

Increase directional lighting score
```

Notice

Feedback now becomes machine-readable.

---

# 6. Phase 4

I LOVE this.

But I'd add one benchmark.

Probably the most important one.

---

## Benchmark 4

### Consistency

Input

One saree

↓

Generate

20 images

↓

Evaluate

Can experts tell

it's the same product?

This is your core promise.

Measure it.

---

# 7. Business Metrics

I'd add

```text
Consistency Score
```

Example

```text
Product Identity

97%

Color Consistency

96%

Embroidery Consistency

94%

Brand Consistency

98%
```

Those become your north-star metrics.

---

# 8. Product UI

The biggest thing I disagree with.

Current flow

```text
Upload

↓

Interview

↓

Review DNA
```

I think

the review should happen much earlier.

I'd do

```text
Upload

↓

Instant AI Analysis

↓

Review Product DNA

↓

Interview

↓

Creative Objective
```

Why?

Users immediately see

> "The AI understood my product."

That's a trust-building moment.

---

# 9. The biggest thing I think is missing

And I think this will become one of your strongest features.

## Reference Manager

Suppose a brand uploads

* logo
* moodboard
* previous campaigns
* Pinterest board

Instead of treating them as files

I'd treat them as

Reference DNA.

Example

```yaml
Reference DNA

Brand

Visual Language

Lighting

Composition

Color

Styling

Patterns
```

Now

Campaign

inherits

Reference DNA.

That's incredibly powerful for agencies.

---

# 10. Finally...

I think we've officially reached Product Mode.

That means the documents should start changing.

Instead of

```text
IMG-001

OBJ-001
```

Engineering should begin producing

```text
PRD-001

Frontend Specs

API Specs

Database Schema

Integration Tests

Acceptance Criteria

User Journeys
```

Those are the documents that will get the MVP shipped.

---

# My answers to your open questions

### 1. Image upload & Product DNA extraction

**Automatic first, human confirmation second.**

The ideal experience is:

1. User uploads a product image.
2. Vision Adapter extracts a draft Product DNA with confidence scores.
3. User reviews only low-confidence fields or makes corrections.
4. The verified Product DNA becomes the foundation for the campaign.

That minimizes friction while keeping accuracy high.

### 2. Authentication

**Skip accounts for the MVP.**

Build a single-user local-first application. User management, teams, permissions, and cloud synchronization are product concerns that don't validate your core hypothesis.

### 3. Deployment

**Develop locally first.**

Don't optimize deployment until you've validated the workflow. Once the vertical slice is stable, moving to something like Vercel for the frontend and a Python hosting platform for the backend is straightforward.

---

# My final recommendation

I think the repository should officially enter a new era.

Everything before today belongs to:

```text
Research/
```

Everything from tomorrow onward belongs to:

```text
Product/
```

That mental shift matters. You're no longer asking, *"How should the system think?"* You're asking, *"How can someone accomplish real work with this system?"*

From now on, every feature should justify itself by making the end-to-end workflow—from **one product photo** to **a publishable campaign**—faster, more reliable, or more valuable. If it doesn't improve that journey, it probably belongs in a future iteration rather than the MVP.

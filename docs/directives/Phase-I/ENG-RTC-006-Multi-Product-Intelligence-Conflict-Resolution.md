# INTELLIGENCE → ENGINEERING INSTRUCTION
# ENG-RTC-006 — Multi-Product Intelligence & Conflict Resolution

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** SPECIFICATION — IMPLEMENTATION REQUEST  
**Priority:** CRITICAL  
**Depends On:** ENG-RTC-001 through ENG-RTC-005  
**Architectural Position:** Intelligence Resolution → Shot-Level Creative Solution

---

# 1. Purpose

The current system has matured from single-product prompt generation into a closed-loop visual intelligence system.

The next architectural problem is:

> **How should the Intelligence Layer resolve competing visual requirements when multiple products, materials, domains, and authenticity constraints coexist within the same shot?**

A campaign may contain:

```text
MODEL
+
APPAREL
+
FOOTWEAR
+
JEWELRY
+
HANDBAG
+
ENVIRONMENT
```

Each entity can introduce different requirements for:

- material representation
- lighting
- texture visibility
- specular response
- camera/framing
- composition
- authenticity
- forbidden artifacts

These requirements cannot simply be concatenated.

The Intelligence Layer must produce **one coherent shot-level solution**.

---

# 2. Core Principle

Multi-product intelligence must follow:

> **Resolve before compiling.**

The system must NOT do:

```text
Product A rules
+
Product B rules
+
Product C rules
=
combined prompt
```

Instead:

```text
PRODUCT INTELLIGENCE
        ↓
REQUIREMENT EXTRACTION
        ↓
CONFLICT DETECTION
        ↓
PRIORITY / OBJECTIVE RESOLUTION
        ↓
PHYSICAL COMPATIBILITY ANALYSIS
        ↓
SHOT-LEVEL SOLUTION
        ↓
PROMPT COMPILATION
```

The Prompt Compiler must receive an already-resolved creative solution.

It must not become the conflict-resolution engine.

---

# 3. Architectural Boundary

The responsibility of each layer must remain explicit.

## Intelligence Layer

Determines:

```text
what each product requires
```

## Decision / Resolution Layer

Determines:

```text
which requirements dominate
which requirements can coexist
which requirements can be satisfied indirectly
which requirements must be relaxed
```

## Constraint Solver

Determines:

```text
whether the proposed combination is physically/technically coherent
```

## Prompt Compiler

Translates the resolved solution into:

```text
SUBJECT
MATERIAL
LIGHTING
CAMERA
ENVIRONMENT
QUALITY
FORBIDDEN
```

## Evaluator

Determines whether the resulting artifact actually satisfies the resolved solution.

---

# 4. Product Requirement Model

Each product participating in a shot must expose structured requirements.

Conceptually:

```json
{
  "product_id": "saree_001",
  "domain": "apparel",
  "material": "silk",
  "requirements": {
    "texture_visibility": 0.90,
    "specular_visibility": 0.55,
    "microstructure_visibility": 0.95,
    "drape_visibility": 0.90
  }
}
```

Another product:

```json
{
  "product_id": "jewelry_001",
  "domain": "jewelry",
  "material": "gold",
  "requirements": {
    "texture_visibility": 0.45,
    "specular_visibility": 0.90,
    "highlight_definition": 0.90
  }
}
```

Another:

```json
{
  "product_id": "shoe_001",
  "domain": "footwear",
  "material": "leather",
  "requirements": {
    "texture_visibility": 0.80,
    "specular_visibility": 0.75,
    "surface_definition": 0.85
  }
}
```

The exact schema is engineering territory.

The semantic concept is mandatory:

> **Products contribute requirements, not final decisions.**

---

# 5. Requirement Types

Initially classify requirements into:

```text
MATERIAL
LIGHTING
CAMERA
COMPOSITION
ENVIRONMENT
AUTHENTICITY
FORBIDDEN
VISIBILITY
```

Do not assume every product contributes to every category.

---

# 6. Requirement Priority

Not all requirements have equal importance.

The system must distinguish:

```text
MANDATORY
HIGH
MEDIUM
LOW
```

However, priority alone must not determine the final solution.

A mandatory requirement may still be physically incompatible with another mandatory requirement.

Therefore:

```text
priority
+
campaign objective
+
shot objective
+
physical compatibility
+
product importance
```

must jointly inform resolution.

---

# 7. Campaign Objective

The resolver must know what the shot is trying to achieve.

Examples:

```text
CRAFTSMANSHIP
PRODUCT DETAIL
CONVERSION
LIFESTYLE
EDITORIAL
BRAND
```

The same products can therefore produce different solutions depending on the shot objective.

Example:

```text
CRAFTSMANSHIP
→ maximize textile and jewelry detail

LIFESTYLE
→ prioritize natural interaction and believable environment

CONVERSION
→ prioritize product readability and commercial clarity
```

This objective must be explicit.

---

# 8. Product Role

Each product must also receive a role within the shot.

Initially:

```text
PRIMARY
SECONDARY
SUPPORTING
BACKGROUND
```

Example:

```text
Saree       → PRIMARY
Jewelry     → SECONDARY
Sandals     → SUPPORTING
Handbag     → SUPPORTING
```

This does not mean secondary products can be visually incorrect.

It means their requirements may be negotiated differently when conflicts occur.

---

# 9. Conflict Detection

The resolver must explicitly identify conflicts.

Example:

```text
Requirement A:
soft diffused light

Requirement B:
strong directional specular highlight
```

Potential conflict:

```text
LIGHTING
```

Another:

```text
Requirement A:
full-body composition

Requirement B:
extreme facial/textile detail
```

Potential conflict:

```text
CAMERA / COMPOSITION
```

Another:

```text
Requirement A:
minimal environment

Requirement B:
environmental storytelling
```

Potential conflict:

```text
ENVIRONMENT
```

The system should never silently discard one requirement.

---

# 10. Conflict Types

Initially support:

## TYPE 1 — Direct Conflict

Two requirements cannot reasonably coexist under the same parameter.

Example:

```text
hard directional key
vs
fully flat diffused illumination
```

## TYPE 2 — Partial Conflict

Requirements can coexist with compromise.

Example:

```text
soft key
+
controlled specular accent
```

## TYPE 3 — Apparent Conflict

Requirements appear contradictory but can be satisfied through a more sophisticated setup.

Example:

```text
soft overall illumination
+
controlled jewelry highlight
```

This may be solved through:

```text
large soft key
+
small controlled specular accent
```

## TYPE 4 — Priority Conflict

Both requirements are feasible, but one must receive more visual emphasis.

---

# 11. Conflict Resolution Strategies

Initially support:

```text
ACCOMMODATE
COMPROMISE
PRIORITIZE
ISOLATE
DEFER
ESCALATE
```

### ACCOMMODATE

Both requirements can be satisfied directly.

### COMPROMISE

Adjust the implementation so both remain adequately represented.

### PRIORITIZE

One requirement receives stronger treatment because of campaign/shot objectives.

### ISOLATE

Use spatial, temporal, compositional, or optical separation.

Example:

```text
primary soft key
+
controlled jewelry kicker
```

### DEFER

A secondary requirement is intentionally reduced because the shot cannot adequately serve it.

This must be recorded.

### ESCALATE

The conflict cannot be safely resolved at the current layer.

---

# 12. No Silent Requirement Loss

This is a critical law.

If:

```text
Product A requirement
```

is not included in the final shot solution, the resolver must record:

```text
requirement_id
resolution
reason
```

Example:

```json
{
  "requirement_id": "SHOE-TEXTURE-001",
  "resolution": "DEFER",
  "reason": "Craftsmanship shot prioritizes saree weave and jewelry detail.",
  "impact": "Reduced footwear texture visibility."
}
```

The system must never silently drop product requirements.

---

# 13. Resolved Shot Solution

The output of the resolver should conceptually resemble:

```json
{
  "shot_id": "craftsmanship_01",

  "objective": "CRAFTSMANSHIP",

  "primary_product": "saree_001",

  "product_roles": {
    "saree_001": "PRIMARY",
    "jewelry_001": "SECONDARY",
    "shoe_001": "SUPPORTING"
  },

  "resolved_solution": {
    "lighting": {
      "key": "large directional soft source",
      "fill": "controlled low fill",
      "accent": "small controlled specular accent for jewelry"
    },

    "camera": {
      "framing": "medium-full",
      "priority": "saree and upper-body detail"
    },

    "material": {
      "saree": "high weave visibility",
      "jewelry": "controlled highlight definition",
      "leather": "moderate texture visibility"
    }
  },

  "resolutions": [
    {
      "requirement": "jewelry_specular",
      "strategy": "ISOLATE"
    },
    {
      "requirement": "shoe_texture",
      "strategy": "DEFER"
    }
  ]
}
```

The exact implementation may differ.

The semantic requirements must remain.

---

# 14. Lighting Conflict Resolution

Lighting requires special treatment because it is shared by multiple products.

Do not model lighting as:

```text
product → independent lighting
```

Instead:

```text
products
    ↓
shared lighting environment
    ↓
localized optical accommodations
```

The system should first establish:

```text
GLOBAL LIGHTING SOLUTION
```

and then determine:

```text
LOCAL ACCENTS
```

where required.

Example:

```text
GLOBAL:
large soft directional key

LOCAL:
controlled jewelry highlight

LOCAL:
subtle leather edge definition
```

This is preferred over contradictory global lighting instructions.

---

# 15. Material Conflict Resolution

Materials should not independently dictate lighting.

Instead, the system should ask:

```text
What visual property of this material must survive in the final image?
```

Examples:

```text
Silk
→ weave + drape + controlled sheen

Gold
→ highlight definition + metallic response

Leather
→ grain + controlled reflection

Cotton
→ weave + softness + fold behaviour
```

This prevents the system from translating:

```text
material
→ one rigid lighting command
```

---

# 16. Shared Physical Solution

The resolver should prefer solutions that satisfy multiple requirements simultaneously.

Example:

```text
large soft directional key
```

may satisfy:

```text
silk texture
+
skin realism
+
garment drape
```

while a:

```text
small controlled accent
```

can satisfy:

```text
gold highlight
```

This is superior to independently generating:

```text
silk lighting
+
skin lighting
+
gold lighting
```

---

# 17. Priority Resolution Model

Do not create a simplistic:

```text
PRIMARY ALWAYS WINS
```

rule.

Instead use:

```text
Requirement Priority Score
=
Product Role
+
Shot Objective
+
Visual Importance
+
Material Criticality
+
Campaign Requirement
+
Physical Feasibility
```

The exact mathematical implementation is engineering territory.

The important principle:

> **Resolution must be explainable.**

---

# 18. Explainability

For every non-trivial conflict, the system should be able to answer:

```text
What conflicted?
Why was it a conflict?
What strategy was selected?
Why was that strategy selected?
What requirement was reduced?
What was preserved?
```

Example:

```text
Conflict:
Jewelry required strong specular definition.
Saree required soft dimensional lighting.

Resolution:
ISOLATE.

Reason:
Maintain soft global illumination while introducing a localized controlled highlight.

Preserved:
Saree texture visibility.

Preserved:
Jewelry highlight definition.
```

---

# 19. Multi-Product Constraint Graph

Engineering should model the relationships as a graph rather than a flat list.

Conceptually:

```text
SAREE
  │
  ├── requires → weave visibility
  ├── benefits → soft directional light
  └── requires → drape readability

JEWELRY
  │
  ├── requires → highlight definition
  └── benefits → controlled specular accent

SHOE
  │
  ├── requires → surface definition
  └── benefits → directional edge light
```

Then:

```text
Lighting Node
     ↑
     │
shared constraints
     │
 ┌───┴────┐
 ↓        ↓
Saree   Jewelry
```

The exact graph implementation is up to engineering.

The conceptual requirement is:

> **Relationships between requirements must be represented explicitly.**

---

# 20. Resolution Must Precede Prompt Compilation

The Prompt Compiler must not receive:

```text
Saree lighting rule
+
Jewelry lighting rule
+
Leather lighting rule
```

It must receive:

```text
RESOLVED LIGHTING SOLUTION
```

Likewise:

```text
MATERIAL
```

should contain resolved material priorities rather than independent contradictory directives.

---

# 21. Conflict Resolution and Evaluation

The Evaluation Engine must eventually evaluate the artifact against the:

```text
RESOLVED SHOT SOLUTION
```

not against every raw product rule independently.

This is important.

If the resolver intentionally chose:

```text
DEFER shoe texture
```

then the evaluator should not later fail the image merely because the shoe texture is not maximized.

The evaluator must know:

```text
what was required
what was intentionally reduced
why it was reduced
```

---

# 22. Resolution Record

Every shot should retain:

```text
Raw Requirements
+
Detected Conflicts
+
Resolution Decisions
+
Deferred Requirements
+
Final Shot Solution
```

This becomes part of provenance.

---

# 23. Escalation Conditions

Escalate when:

```text
two mandatory requirements are physically incompatible
```

or:

```text
resolution would materially violate campaign intent
```

or:

```text
no known optical/creative strategy can satisfy the conflict
```

or:

```text
the resolver lacks sufficient domain knowledge
```

Escalation should produce:

```text
MULTI_PRODUCT_CONFLICT_REPORT
```

Do not silently choose.

---

# 24. Required Machine-Readable Objects

Introduce conceptual objects for:

```text
ProductRequirement
RequirementPriority
ProductRole
Conflict
ConflictResolution
ResolvedShotSolution
MultiProductConflictReport
```

Exact class/file naming remains engineering territory.

---

# 25. Required Test Cases

### TEST-MP-001 — No Conflict

Two products with compatible requirements.

Expected:

```text
ACCOMMODATE
```

### TEST-MP-002 — Partial Conflict

Soft garment lighting + controlled jewelry highlight.

Expected:

```text
ISOLATE or COMPROMISE
```

### TEST-MP-003 — Direct Conflict

Two mutually incompatible global lighting requirements.

Expected:

```text
CONFLICT DETECTED
```

and no silent resolution.

### TEST-MP-004 — Primary Product Priority

Primary product has a craftsmanship objective.

Expected:

```text
primary requirements receive greater weight
```

but secondary requirements remain represented or explicitly deferred.

### TEST-MP-005 — Deferred Requirement

Supporting product requirement intentionally reduced.

Expected:

```text
DEFER
+
reason
+
provenance
```

### TEST-MP-006 — Shared Lighting Solution

Multiple products should be satisfied by one global lighting solution plus localized accents.

Expected:

```text
no contradictory global lighting directives
```

### TEST-MP-007 — Explainability

Every non-trivial conflict returns:

```text
conflict
strategy
reason
preserved requirements
reduced requirements
```

### TEST-MP-008 — Prompt Compiler Boundary

Compiler receives resolved solution, not raw competing rules.

### TEST-MP-009 — Evaluator Boundary

Evaluator evaluates against resolved solution and known deferred requirements.

### TEST-MP-010 — Mandatory Conflict

Two mandatory requirements cannot coexist.

Expected:

```text
MULTI_PRODUCT_CONFLICT_REPORT
```

### TEST-MP-011 — Knowledge Gap

Conflict cannot be resolved because domain knowledge is insufficient.

Expected:

```text
knowledge-layer escalation
```

### TEST-MP-012 — Provenance

Every resolution traces back to the contributing requirements.

---

# 26. Non-Goals

Do not implement in ENG-RTC-006:

- new product-domain knowledge
- new saree rules
- new jewelry ontology
- new footwear ontology
- new lighting ontology
- new image-generation models
- adaptive evaluator redesign
- semantic locality
- autonomous knowledge-base modification

The task is:

> **Resolve existing intelligence.**

Not:

> **Create new domain intelligence.**

---

# 27. Freeze Conditions

ENG-RTC-006 may be frozen only when:

```text
Product requirements are represented
        AND
Product roles are represented
        AND
Shot objective is explicit
        AND
Conflicts are explicitly detected
        AND
Conflict strategies are deterministic/auditable
        AND
Requirements cannot silently disappear
        AND
Shared lighting can be resolved
        AND
Deferred requirements retain provenance
        AND
Prompt compilation receives resolved solutions
        AND
Evaluation respects resolved/deferred requirements
        AND
All tests pass
```

---

# 28. Final Architectural Law

The system must now obey:

> **Products provide requirements.**
>
> **The Intelligence Layer resolves requirements.**
>
> **The Constraint Solver validates feasibility.**
>
> **The Prompt Compiler expresses the resolved solution.**
>
> **The Generator renders it.**
>
> **The Evaluator judges the rendered artifact against the resolved solution.**

Never allow the Prompt Compiler to become the place where product conflicts are accidentally resolved.

---

# 29. Required Engineering Response

Return:

`ENG-RTC-006-IMPLEMENTATION`

Include:

1. Files created/changed
2. Product requirement representation
3. Product role representation
4. Shot objective integration
5. Conflict detection
6. Conflict classification
7. Resolution strategies
8. Priority mechanism
9. Shared lighting resolution
10. Deferred requirement handling
11. Resolution provenance
12. Resolved Shot Solution representation
13. Prompt Compiler integration
14. Evaluator integration
15. Escalation handling
16. All TEST-MP-001 through TEST-MP-012 results
17. Example multi-product resolution
18. Example unresolved conflict
19. Known limitations
20. Architectural risks

Do not proceed to another architectural layer until this implementation has been reviewed and frozen.

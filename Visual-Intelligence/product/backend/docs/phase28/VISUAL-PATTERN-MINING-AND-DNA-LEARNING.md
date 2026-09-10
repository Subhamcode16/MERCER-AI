# VISUAL-PATTERN-MINING-AND-DNA-LEARNING.md
## Phase 28 Architecture Specification: Visual Pattern Mining & DNA Learning

---

### 1. Executive Overview

Visual and aesthetic elements of marketing campaigns (color palettes, visual densities, composition topologies, kinetic pacings, and typography weights) correlate with downstream user attention, click-through behavior, and brand memorability. However, under the **ILYREN Epistemic Invariants**:
$$\mathbf{Correlation \neq Causal\ Proof} \quad \mathbf{Visual\ Feature \neq Universal\ Truth}$$

The `VisualPatternMiner` extracts high-dimensional aesthetic correlations, establishes rigorous visual DNA profiles, and maps how specific stylistic configurations perform across heterogeneous audiences without hallucinating deterministic design rules.

---

### 2. Visual DNA Architecture

Visual configurations are modeled across five orthogonal dimensions:

```
+-------------------------------------------------------------------------+
|                         Visual DNA Configuration                        |
+-------------------------------------------------------------------------+
| 1. Color Palette: Warm / Cool / Neutral / High-Contrast / Monochromatic  |
| 2. Composition: Rule-of-Thirds / Centered / Asymmetric / Dense Grid    |
| 3. Kinetic Flow: Static / Smooth Pan / Fast Cut / Micro-Paced / Glitch  |
| 4. Typography: Heavy Sans / Serif Minimal / Brutalist Display / Script   |
| 5. Subject Geometry: Macro Close-up / Environmental / Flat-Lay / Avatar |
+-------------------------------------------------------------------------+
```

```python
class VisualDNA:
    dna_id: str
    tenant_id: str
    channel: str
    palette_distribution: Dict[str, float]
    composition_entropy: float
    pacing_bpm: Optional[float]
    typography_density: float
    feature_hash: str  # SHA-256 hash of invariant visual tokens
```

---

### 3. Confounder-Aware Pattern Mining

When a visual configuration correlates with positive campaign lift, `VisualPatternMiner` executes multi-variable isolation:

1. **Seasonality Control:** Was the visual launched during Black Friday or Holiday sales spikes?
2. **Spend Normalization:** Was the visual backed by a 10x media spend budget?
3. **Channel Affinity:** Does the pattern succeed exclusively on TikTok or cross-channel to Pinterest and Meta?
4. **Brand Tone Alignment:** Does the visual violate brand guidelines despite short-term attention spikes?

```python
def mine_visual_patterns(visual_samples: List[VisualArtifact]) -> List[VisualPattern]:
    for sample in visual_samples:
        raw_correlation = compute_lift(sample.visual_dna, sample.outcomes)
        confounder_score = evaluate_confounders(sample.context, sample.media_spend)
        
        # Invariant: Never promote unadjusted visual lift
        calibrated_lift = raw_correlation * (1.0 - confounder_score)
        
        yield VisualPattern(
            pattern_id=f"VP-{uuid4().hex[:8]}",
            visual_dna=sample.visual_dna,
            raw_lift=raw_correlation,
            calibrated_lift=calibrated_lift,
            epistemic_grade=EpistemicGrade.CORRELATIONAL_OBSERVATIONAL,
            is_actionable=calibrated_lift > MIN_ACTIONABLE_LIFT
        )
```

---

### 4. Integration with Creative Skills

Visual patterns mined by Phase 28 feed into Phase 25 Creative Intelligence engines and Phase 26 Asset Generation pipelines:
- **Skill Suggestions:** Offer visual DNA priors to prompt synthesizers and design agents.
- **Counter-Pattern Warnings:** Alert designers when a proposed layout strongly matches historically high-fatigue visual profiles.
- **Strict Human Oversight:** No visual template is automatically overwritten without designer sign-off.

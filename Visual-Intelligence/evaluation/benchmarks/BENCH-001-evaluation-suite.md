---
BENCH-ID: BENCH-001
Title: Evaluation & Benchmark Suite Architecture
Version: 1.0.0
Status: Draft
Owner: Track C (Intelligence Improvement)
Last Updated: 2026-07-01
---

# BENCH-001: Evaluation & Benchmark Suite Architecture

## Purpose

As we transition into the Product Phase, we must definitively prove that the **Creative Intelligence Infrastructure** produces higher-quality campaigns than traditional Prompt Engineering. 

To achieve this, we are establishing a rigorous, automated **Benchmark Suite**. Every subsequent code commit, model integration, or prompt tweak must be evaluated against this gold-standard dataset.

---

## 1. Directory Architecture

The benchmark suite is organized by specific creative verticals and edge cases. For the MVP, we are exclusively populating the `textile/` vertical.

```text
Visual-Intelligence/
└── benchmarks/
    ├── textile/                   # Domain-specific material testing
    │   ├── banarasi/
    │   ├── kanjeevaram/
    │   └── organza/
    ├── campaigns/                 # Output aesthetic testing
    │   ├── luxury_wedding/
    │   ├── festive_evening/
    │   └── summer_casual/
    └── consistency/               # Edge-case stability testing
        ├── multi_scene/
        ├── wardrobe/
        └── lighting/
```

---

## 2. Test Case Structure

Within a specific test case (e.g., `benchmarks/textile/banarasi/test_001/`), we store the raw input along with the exact expected outputs for the various pipeline stages.

```text
benchmarks/textile/banarasi/test_001/
├── input.jpg                  # The raw image of the Banarasi Saree
├── expected_claims.json       # Gold-standard output for the VIF
├── expected_dna.json          # Gold-standard state for the Runtime
└── expected_patterns.json     # Gold-standard context injection
```

### A. expected_claims.json
This tests the extraction side of the platform (Track B). If we upgrade Processing Station 3's texture model, it must accurately recreate this JSON.
```json
{
  "Subject": "Weave",
  "Predicate": "Technique",
  "Value": "Banarasi",
  "Evidence": ["Heavy gold zari border", "Floral brocade motifs"]
}
```

### B. expected_dna.json
This tests the `ARC-002` Creative Context state. It ensures the Decision Engine is correctly structuring the data for the Prompt Compiler.
```json
{
  "Product_DNA": {
    "GarmentType": "Saree",
    "Material": "Silk",
    "Weave": "Banarasi"
  }
}
```

### C. expected_patterns.json
This tests the retrieval layer (`RES-008`). If a user prompts for a "Luxury Wedding", the Retriever *must* pull these statistical rules to inject into the compiler.
```json
{
  "Lighting": "Golden Hour",
  "Jewelry": "Antique Gold",
  "ColorPalette": "Warm"
}
```

---

## 3. CI/CD Integration

This benchmark suite is not a manual QA checklist. It is designed to be executed automatically.

Before any update to the Prompt Compiler or VIF Models is merged into `main`, the test runner will:
1. Ingest `input.jpg`.
2. Generate the claims, DNA, and patterns.
3. Compare the generated files against the `expected_*.json` gold standards.
4. Block the deployment if `Product Fidelity` or `Identity Consistency` drops below the thresholds defined in `PRD-001`.

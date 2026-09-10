# PRD-002: Product Analysis (Vision Adapter)

## 1. Overview
The Vision Adapter replaces the hardcoded "Gemini-only" analysis pipeline with a model-agnostic interface. It takes raw visual inputs (product images, reference moodboards) and standardizes the output into structured **Knowledge Claims** regardless of whether the underlying VLM is Gemini, GPT-4.1 Vision, or Qwen-VL. 

## 2. Goals
- Ensure the extraction of Product DNA and Reference DNA is robust to model changes.
- Provide "Creative Confidence" scores for each extracted claim.
- Support both **Product Extraction** (finding material, weave, features) and **Reference Extraction** (finding brand identity, lighting, color palettes).

## 3. Architecture

### 3.1 Vision Adapter Interface
```python
class VisionAdapter:
    def extract_product_dna(self, image_path: str, provider: str = "gemini") -> ProductDNA:
        """Extracts physical constraints from a garment image."""
        pass
        
    def extract_reference_dna(self, image_paths: list[str], provider: str = "gemini") -> ReferenceDNA:
        """Extracts stylistic intent from moodboards or past campaigns."""
        pass
```

### 3.2 Confidence Scoring
Every extracted field must include a confidence score (0.0 to 1.0).

```json
{
  "material": {
    "value": "Silk",
    "confidence": 0.99
  },
  "weaving_technique": {
    "value": "Banarasi",
    "confidence": 0.95
  },
  "primary_features": {
    "value": ["Gold Zari Brocade", "Floral Motifs"],
    "confidence": 0.97
  }
}
```
*UI Implementation:* Fields with `< 0.85` confidence are highlighted in yellow during the "Review Product DNA" step, prompting the user for manual verification.

### 3.3 The Reference Manager
Agencies often upload past campaigns. The adapter must extract:
- **Lighting Preference**: e.g., "high key, soft shadows"
- **Color Grading**: e.g., "warm, desaturated greens"
- **Composition**: e.g., "negative space, center weighted"

## 4. API Specification (Internal)

### `POST /api/analyze/product`
**Request Payload:**
```json
{
  "image_url": "s3://.../saree_01.jpg",
  "provider": "gemini"
}
```

**Response Payload:**
Returns the structured `ProductDNA` with confidence scores.

### `POST /api/analyze/reference`
**Request Payload:**
```json
{
  "image_urls": ["s3://.../ref_1.jpg", "s3://.../ref_2.jpg"],
  "provider": "gemini"
}
```

**Response Payload:**
Returns the structured `ReferenceDNA`.

## 5. Acceptance Criteria
- [ ] The system can parse a VLM response and normalize it into the exact same JSON schema regardless of the provider used.
- [ ] The `confidence` field is successfully surfaced to the frontend for the "Review DNA" UI.
- [ ] The adapter successfully distinguishes between physical extraction (Product DNA) and stylistic extraction (Reference DNA).

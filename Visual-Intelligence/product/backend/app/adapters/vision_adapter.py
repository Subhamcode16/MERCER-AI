import os
import json
import base64
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.models.campaign import ProductDNA, ReferenceDNA, ConfidenceField

# Model Waterfall: try in order, fall back on quota/availability errors
VISION_MODELS = ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"]

PRODUCT_EXTRACTION_PROMPT = """
You are an expert textile and fashion analyst with deep knowledge of South Asian weaving traditions.

Analyze this garment or textile image with precision. Return ONLY a valid JSON object with no additional text:

{
  "material": { "value": "<fabric type>", "confidence": <0.0-1.0> },
  "weaving_technique": { "value": "<technique name>", "confidence": <0.0-1.0> },
  "primary_features": { "value": ["<feature1>", "<feature2>", ...], "confidence": <0.0-1.0> },
  "cultural_context": { "value": "<cultural/regional origin>", "confidence": <0.0-1.0> },
  "raw_claims": [
    { "Subject": "<subject>", "Predicate": "<predicate>", "Value": "<value>", "Confidence": <0.0-1.0> }
  ],
  "proposed_direction_title": "<short evocative campaign title>",
  "proposed_direction_body": "<2-3 sentence cinematic creative rationale for this garment>"
}

Be precise. If unsure, lower the confidence score rather than guessing.
"""

class VisionAdapter:
    """
    Model-agnostic Vision Adapter.
    Routes image analysis to Gemini Vision and normalizes output into structured Knowledge Claims.
    Uses the Model Waterfall strategy for resilience across quota limits and regional availability.
    """

    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self._client = None

    def _get_client(self):
        """Lazy-loads the Gemini client using the API key from the environment."""
        if self._client is None:
            try:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable is not set.")
                genai.configure(api_key=api_key)
                self._client = genai
            except ImportError:
                raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        return self._client

    def _call_with_waterfall(self, prompt: str, image_bytes: bytes, mime_type: str) -> str:
        """
        Attempts to call each model in VISION_MODELS in order.
        Falls back to the next model on 429 (quota), 503 (unavailable), or 404 (not found).
        """
        genai = self._get_client()
        image_part = {
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(image_bytes).decode("utf-8")
            }
        }

        last_error = None
        for model_name in VISION_MODELS:
            try:
                print(f"[VisionAdapter] Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([prompt, image_part])
                return response.text
            except Exception as e:
                error_str = str(e).lower()
                if any(code in error_str for code in ["429", "503", "404", "quota", "not found", "unavailable"]):
                    print(f"[VisionAdapter] {model_name} failed ({e}), trying next model...")
                    last_error = e
                    continue
                # Re-raise unexpected errors immediately
                raise e

        raise RuntimeError(f"All models in waterfall failed. Last error: {last_error}")

    def analyze_product(self, image_path: str) -> tuple[ProductDNA, Optional[dict]]:
        """
        Analyzes a product image and extracts physical constraints + creative direction.
        Returns (ProductDNA, creative_direction_dict) where creative_direction may be None on parse failure.
        """
        print(f"[VisionAdapter] Analyzing {image_path} via {self.provider}...")

        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            # Detect MIME type from extension
            ext = os.path.splitext(image_path)[-1].lower()
            mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
            mime_type = mime_map.get(ext, "image/jpeg")

            raw_text = self._call_with_waterfall(PRODUCT_EXTRACTION_PROMPT, image_bytes, mime_type)

            # Strip markdown code fences if present
            clean_text = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(clean_text)

            dna = ProductDNA(
                material=ConfidenceField(**data["material"]),
                weaving_technique=ConfidenceField(**data["weaving_technique"]),
                primary_features=ConfidenceField(**data["primary_features"]),
                cultural_context=ConfidenceField(**data.get("cultural_context", {"value": "Unknown", "confidence": 0.5})),
                raw_claims=data.get("raw_claims", [])
            )

            creative_direction = {
                "title": data.get("proposed_direction_title"),
                "body": data.get("proposed_direction_body")
            }

            return dna, creative_direction

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"[VisionAdapter] Analysis failed: {e}. Returning fallback mock.")
            return self._mock_product_dna(), None

    def analyze_reference(self, image_paths: List[str]) -> ReferenceDNA:
        """
        Analyzes moodboard or reference images to extract brand aesthetic constraints.
        (Currently returns a structured mock — live multi-image analysis in Phase 3)
        """
        print(f"[VisionAdapter] Analyzing {len(image_paths)} references via {self.provider}...")
        return ReferenceDNA(
            lighting_preference=ConfidenceField(value="High key, soft shadows", confidence=0.88),
            color_grading=ConfidenceField(value="Warm, desaturated tones", confidence=0.85),
            composition_style=ConfidenceField(value="Negative space, center weighted", confidence=0.90)
        )

    def _mock_product_dna(self) -> ProductDNA:
        """Fallback mock for when the API is unreachable."""
        return ProductDNA(
            material=ConfidenceField(value="Silk", confidence=0.98),
            weaving_technique=ConfidenceField(value="Banarasi", confidence=0.95),
            primary_features=ConfidenceField(value=["Gold Zari Brocade", "Floral Motifs"], confidence=0.92),
            cultural_context=ConfidenceField(value="Varanasi, Uttar Pradesh", confidence=0.90),
            raw_claims=[
                {"Subject": "Garment", "Predicate": "Type", "Value": "Saree", "Confidence": 0.99},
                {"Subject": "Weave", "Predicate": "Technique", "Value": "Banarasi", "Confidence": 0.95}
            ]
        )


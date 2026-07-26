import os
import json
from app.models.campaign import Campaign, AssetState
from app.adapters.knowledge_adapter import KnowledgeAdapter
from app.adapters.honcho_adapter import HonchoAdapter

GENERATION_PROMPT_TEMPLATE = """
You are the Mercer AI Constraints & Image Formation Engine (RES-009).
Your goal is to design a high-end cinematic moodboard brief and precise image generation prompts for a Fashion Campaign.

Here is the context:

=== 1. HONCHO USER MEMORY (Brand Guidelines & Past Corrections) ===
{honcho_context}

=== 2. MATERIAL PHYSICS (Obsidian Knowledge Base) ===
{obsidian_knowledge}

=== 3. PRODUCT DNA (Extracted from Uploaded Image) ===
Material: {material}
Technique: {technique}
Features: {features}

=== 4. CAMPAIGN DIRECTION (Vibe/Aesthetic) ===
Title: {campaign_title}
Objective: {campaign_body}
Assets Requested: {assets_requested}

=== 5. USER SELECTED ART DIRECTION ===
Background: {selected_background}
Pose/Motion: {selected_pose}
Lighting: {selected_lighting}

=== INSTRUCTIONS ===
Synthesize the above constraints. Do NOT simply concatenate strings. Apply physics constraints (e.g. Silk requires specific lighting).
Output a valid JSON object with the following structure:

{{
  "moodboard_brief": "<A rich, 3-paragraph cinematic description of the overall shoot's lighting, set design, and emotional tone.>",
  "prompts": {{
     // For each asset in 'Assets Requested', provide a precise prompt optimized for an Image Generator (e.g. DALL-E or Midjourney)
     "hero_image": "<prompt text>",
     "product_closeup": "<prompt text>"
  }}
}}
"""

class PromptEngine:
    def __init__(self):
        self.knowledge_adapter = KnowledgeAdapter()
        self.honcho_adapter = HonchoAdapter()
        self._client = None

    def _get_client(self):
        if self._client is None:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set.")
            genai.configure(api_key=api_key)
            self._client = genai
        return self._client

    def generate_recommendations(self, campaign: Campaign) -> dict:
        """
        Calls Gemini to get background, pose, and lighting recommendations based on ProductDNA and ontologies.
        """
        dna = campaign.identity.product_dna
        if not dna:
            return {}
            
        # Retrieve context (ontology and vault files)
        obsidian_knowledge = self.knowledge_adapter.retrieve_context(dna)
        
        prompt = f"""
You are the Mercer AI Art Direction Recommendation Engine.
Based on the following garment details and the domain knowledge base:

=== PRODUCT DNA ===
Material: {dna.material.value}
Technique: {dna.weaving_technique.value}

=== DOMAIN KNOWLEDGE & ONTOLOGY ===
{obsidian_knowledge}

Recommend the absolute best Background, Pose, and Lighting configuration.
Select from these available options:
- Backgrounds: Heritage Fort / Palace Corridor, Lush Garden, Nighttime Palace, Cinematic Studio, Persian Carpet Backdrop.
- Poses/Motions: Dynamic Fabric Spin, Contemplative Veil Drape, Editorial Close-Up Gaze, The Saree Column, Wind-Blown Toss.
- Lighting: Golden Hour (2700K-3200K), Ethereal Backlight / Edge Wrap, Soft Window Light, High-Key Window Doorway, Moonlight / Night Ambient, Studio Warm Key.

Output a valid JSON object matching this structure exactly:
{{
  "background": {{
    "value": "<selected background option>",
    "reason": "<one sentence explanation referencing the garment's ontology/history>"
  }},
  "pose": {{
    "value": "<selected pose option>",
    "reason": "<one sentence explanation of why this pose complements this fabric physics>"
  }},
  "lighting": {{
    "value": "<selected lighting option>",
    "reason": "<one sentence explanation of how this lighting brings out the textile weave/zari>"
  }}
}}
"""
        genai = self._get_client()
        # Fallback waterfall for Gemini models in cloud/local context (user global rule)
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        response = None
        for model_name in models_to_try:
            try:
                print(f"[PromptEngine] Attempting recommendations with model {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                break
            except Exception as e:
                print(f"[PromptEngine] Model {model_name} failed: {e}")
                continue

        if not response:
            raise RuntimeError("All model choices failed for recommendations.")
        
        try:
            clean_text = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"[PromptEngine] Failed to generate recommendations: {e}")
            # Fallbacks based on material
            is_heavy = "kanjeevaram" in str(dna.material.value).lower() or "banarasi" in str(dna.material.value).lower()
            return {
                "background": {
                    "value": "Heritage Fort / Palace Corridor" if is_heavy else "Cinematic Studio",
                    "reason": "Provides a culturally and architecturally authentic backdrop suitable for this weave."
                },
                "pose": {
                    "value": "The Saree Column" if is_heavy else "Wind-Blown Toss",
                    "reason": "Accentuates the natural weight and drape structure of this textile."
                },
                "lighting": {
                    "value": "Golden Hour (2700K-3200K)" if is_heavy else "Soft Window Light",
                    "reason": "Highlights the rich luster and details of the fabric weave."
                }
            }

    def generate_campaign_assets(self, campaign: Campaign) -> dict:
        """
        Executes the RAG pipeline. Returns a dictionary with the moodboard brief and asset prompts.
        """
        print(f"[PromptEngine] Starting generation for campaign {campaign.id}")
        
        # 1. Fetch RAG Context
        honcho_context = self.honcho_adapter.get_context()
        obsidian_knowledge = self.knowledge_adapter.retrieve_context(campaign.identity.product_dna)
        
        # 2. Extract Campaign Data
        dna = campaign.identity.product_dna
        planning = campaign.planning
        
        features = ", ".join(dna.primary_features.value) if isinstance(dna.primary_features.value, list) else dna.primary_features.value
        assets_requested = ", ".join(planning.campaign_plan.assets_requested)

        # 3. Build Prompt
        prompt = GENERATION_PROMPT_TEMPLATE.format(
            honcho_context=honcho_context,
            obsidian_knowledge=obsidian_knowledge,
            material=dna.material.value,
            technique=dna.weaving_technique.value,
            features=features,
            campaign_title=planning.proposed_direction_title,
            campaign_body=planning.proposed_direction_body,
            assets_requested=assets_requested,
            selected_background=planning.selected_background or "Not specified",
            selected_pose=planning.selected_pose or "Not specified",
            selected_lighting=planning.selected_lighting or "Not specified"
        )

        # 4. Call LLM
        genai = self._get_client()
        # Fallback waterfall for Gemini models in cloud/local context (user global rule)
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        response = None
        for model_name in models_to_try:
            try:
                print(f"[PromptEngine] Attempting prompt generation with model {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                break
            except Exception as e:
                print(f"[PromptEngine] Model {model_name} failed: {e}")
                continue

        if not response:
            raise RuntimeError("All model choices failed for generation.")
        
        # 5. Parse JSON output
        try:
            clean_text = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            result = json.loads(clean_text)
            return result
        except Exception as e:
            print(f"[PromptEngine] Failed to parse JSON: {e}")
            print(f"Raw Output: {response.text}")
            # Fallback
            return {
                "moodboard_brief": "Fallback cinematic brief. A high-end editorial shoot.",
                "prompts": {asset: f"A high fashion {asset} shot" for asset in planning.campaign_plan.assets_requested}
            }

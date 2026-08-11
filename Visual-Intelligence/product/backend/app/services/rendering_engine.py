import logging
from typing import Optional

from app.adapters.providers.provider_nanobanana import NanoBananaProvider
from app.adapters.providers.provider_bytedance import ByteDanceProvider
from app.adapters.providers.provider_openai import OpenAIProvider
from app.adapters.providers.provider_imagineart import ImagineArtProvider
from app.adapters.providers.provider_recraft import RecraftProvider

logger = logging.getLogger(__name__)

class RenderingEngine:
    """
    Unified Inference Adapter (Model Router).
    Routes image generation requests to specific providers based on model_id.
    Implements fallback logic if the primary provider fails.
    """
    def __init__(self):
        self.providers = {
            "nano": NanoBananaProvider(),
            "bytedance": ByteDanceProvider(),
            "openai": OpenAIProvider(),
            "imagineart": ImagineArtProvider(),
            "recraft": RecraftProvider()
        }
        
        # Model routing table
        self.model_map = {
            "Seedream V5 pro": ("bytedance", 4),
            "Nano Banana Lite": ("nano", 2),
            "GPT Image 2": ("openai", 2),
            "ImagineArt 2.0": ("imagineart", 2),
            "Recraft V4.1 Pro": ("recraft", 4),
            "Nano Banana 2": ("nano", 2),
            "Seedream v5.0 Lite": ("bytedance", 2),
            "Nano Banana Pro": ("nano", 4)
        }

    def get_model_cost(self, model_id: str) -> int:
        """Returns the credit cost of the model."""
        if model_id not in self.model_map:
            raise ValueError(f"Unsupported model: {model_id}")
        return self.model_map[model_id][1]

    def _get_fallback_model(self, model_id: str) -> str:
        """Determine fallback based on tier (Pro vs Lite/Normal)."""
        cost = self.get_model_cost(model_id)
        if cost >= 4:
            return "Nano Banana Pro"
        return "Nano Banana 2"

    async def generate_image(self, prompt: str, model_id: str) -> bytes:
        """
        Generates an image. Attempts the primary model, falls back if it fails.
        """
        if model_id not in self.model_map:
            raise ValueError(f"Unsupported model: {model_id}")

        provider_key, _ = self.model_map[model_id]
        provider = self.providers[provider_key]

        try:
            logger.info(f"[RenderingEngine] Attempting generation with {model_id}")
            result = await provider.generate_image(prompt, model_id)
            return result
        except Exception as e:
            logger.warning(f"[RenderingEngine] Primary model {model_id} failed: {e}. Attempting fallback.")
            
            fallback_model = self._get_fallback_model(model_id)
            
            if fallback_model == model_id:
                # The fallback is the primary, we cannot fall back further
                raise RuntimeError(f"Generation failed on fallback model {model_id}: {e}")
                
            fallback_key, _ = self.model_map[fallback_model]
            fallback_provider = self.providers[fallback_key]
            
            logger.info(f"[RenderingEngine] Executing fallback with {fallback_model}")
            return await fallback_provider.generate_image(prompt, fallback_model)

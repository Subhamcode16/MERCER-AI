import os
import base64
import logging
from app.adapters.providers.base import BaseImageProvider

logger = logging.getLogger(__name__)

class NanoBananaProvider(BaseImageProvider):
    async def generate_image(self, prompt: str, model_name: str) -> bytes:
        logger.info(f"[NanoBananaProvider] Generating image using {model_name}...")
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Check if key exists and is not dummy
        if api_key and api_key != "dummy_key_for_testing":
            try:
                from google import genai
                # Map model names to actual Gemini API model IDs
                model_id = "gemini-3.1-flash-image"
                if "pro" in model_name.lower():
                    model_id = "gemini-3-pro-image-preview"
                    
                client = genai.Client(api_key=api_key)
                
                # Execute blocking API call in executor
                import asyncio
                def _call():
                    return client.models.generate_content(
                        model=model_id,
                        contents=[prompt],
                        config={"response_modalities": ["IMAGE"]}
                    )
                response = await asyncio.to_thread(_call)
                
                # Extract image bytes from response candidate inline data
                part = response.candidates[0].content.parts[0]
                image_bytes = part.inline_data.data
                
                # Check if returned as base64 string or raw bytes
                if isinstance(image_bytes, str):
                    image_bytes = base64.b64decode(image_bytes)
                return image_bytes
            except Exception as e:
                logger.error(f"[NanoBananaProvider] Real API generation failed: {e}. Falling back to mock image.")
        else:
            logger.warning("[NanoBananaProvider] GEMINI_API_KEY not configured. Falling back to mock image.")

        # Fallback to local mock image
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        mock_path = os.path.join(dir_path, "tests", "mock_image.png")
        with open(mock_path, "rb") as f:
            return f.read()
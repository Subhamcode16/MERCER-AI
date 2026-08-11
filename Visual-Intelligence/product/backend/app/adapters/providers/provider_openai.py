import os
import base64
import logging
import httpx
import asyncio
from app.adapters.providers.base import BaseImageProvider

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseImageProvider):
    async def generate_image(self, prompt: str, model_name: str) -> bytes:
        logger.info(f"[OpenAIProvider] Generating image using {model_name}...")
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key != "dummy_key_for_testing":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                def _call():
                    return client.images.generate(
                        model="dall-e-3" if model_name == "gpt_image_2" or "gpt" in model_name.lower() else model_name,
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard"
                    )
                response = await asyncio.to_thread(_call)
                
                # Extract image URL
                image_url = response.data[0].url
                
                # Download image bytes
                async with httpx.AsyncClient() as httpx_client:
                    img_response = await httpx_client.get(image_url)
                    if img_response.status_code == 200:
                        return img_response.content
                    else:
                        raise RuntimeError(f"Failed to download image from OpenAI: status {img_response.status_code}")
            except Exception as e:
                logger.error(f"[OpenAIProvider] Real API generation failed: {e}. Falling back to mock image.")
        else:
            logger.warning("[OpenAIProvider] OPENAI_API_KEY not configured. Falling back to mock image.")

        # Fallback to local mock image
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        mock_path = os.path.join(dir_path, "tests", "mock_image.png")
        with open(mock_path, "rb") as f:
            return f.read()
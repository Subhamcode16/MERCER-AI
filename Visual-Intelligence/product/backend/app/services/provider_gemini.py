"""
Mercer AI — Google GenAI Provider

Integrates with the `google-genai` SDK for Nano Banana 2 image generation.
Wraps calls in robust exception handling to protect the billing engine.
"""
import os
import logging
import base64
from fastapi import HTTPException, status
from google import genai
from google.genai.errors import APIError

logger = logging.getLogger(__name__)


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in environment variables")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image generation provider is not configured properly."
        )
    return genai.Client(api_key=api_key)


async def generate_nano_banana_2(prompt: str) -> str:
    """
    Calls the gemini-3.1-flash-image (Nano Banana 2) model to generate an image.
    Returns the base64 encoded image string.
    
    Raises HTTPException on provider failure (which the router catches to refund credits).
    """
    client = _get_client()
    
    logger.info("Calling Nano Banana 2 with prompt: %s...", prompt[:50])
    
    try:
        # We run the synchronous SDK method in a threadpool to not block the async event loop
        # For a truly async integration we would use the async client if available, but for MVP
        # standard thread offloading is acceptable, or if the SDK supports async:
        # client.aio.models.generate_images(...)
        
        # Check if async is supported, else fallback to sync in executor
        if hasattr(client, "aio"):
            response = await client.aio.models.generate_images(
                model='gemini-3.1-flash-image',
                prompt=prompt,
                config=dict(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    # aspectRatio="3:4" # if we add aspect ratio support
                )
            )
        else:
            response = client.models.generate_images(
                model='gemini-3.1-flash-image',
                prompt=prompt,
                config=dict(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                )
            )
            
        if not response.generated_images:
            raise ValueError("Provider returned an empty response with no images.")
            
        # The new SDK returns raw bytes in image.image.image_bytes
        image_bytes = response.generated_images[0].image.image_bytes
        
        # Convert to base64 for the frontend payload
        b64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        
        logger.info("Successfully generated Nano Banana 2 image")
        return b64_encoded
        
    except APIError as e:
        logger.error("Google GenAI API Error: %s", str(e))
        # 429 indicates Quota Exceeded (Resource Exhausted)
        if "429" in str(e) or e.code == 429:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Our creative engine is currently at capacity. Please try again in a few moments."
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to generate image due to an upstream provider error."
        )
    except Exception as e:
        logger.exception("Unexpected error during image generation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the image."
        )

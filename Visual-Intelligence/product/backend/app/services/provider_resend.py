import httpx
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)

async def subscribe_to_resend_marketing(email: str):
    """
    Subscribes the user's email address to the Resend marketing audience list.
    """
    settings = get_settings()
    if not settings.resend_api_key or not settings.resend_audience_id:
        logger.warning("Resend credentials not set. Skipping subscription for %s", email)
        return False

    url = f"https://api.resend.com/audiences/{settings.resend_audience_id}/contacts"
    headers = {
        "Authorization": f"Bearer {settings.resend_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "unsubscribed": False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=5.0)
            if response.status_code in [200, 201]:
                logger.info("Successfully subscribed %s to Resend audience", email)
                return True
            else:
                logger.error(
                    "Resend subscription failed for %s: %d - %s",
                    email,
                    response.status_code,
                    response.text
                )
                return False
    except Exception as e:
        logger.error("Error subscribing %s to Resend: %s", email, str(e))
        return False

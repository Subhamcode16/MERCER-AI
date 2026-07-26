import logging
from datetime import datetime, timezone
import stripe
from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel

from app.config import get_settings
from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.database import get_db
from app.models.user import Tier, TIER_CREDIT_ALLOTMENT

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments", tags=["payments"])

settings = get_settings()
if settings.stripe_secret_key:
    stripe.api_key = settings.stripe_secret_key

class CheckoutRequest(BaseModel):
    tier: str

# In a real app, map these to actual Stripe Price IDs created in your Stripe Dashboard.
# Here we use dummy IDs that would be replaced with actual env vars or hardcoded IDs.
STRIPE_PRICE_MAP = {
    Tier.starter.value: "price_starter_dummy",
    Tier.pro.value: "price_pro_dummy",
    Tier.studio.value: "price_studio_dummy"
}

@router.post("/create-checkout-session")
async def create_checkout_session(
    req: CheckoutRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=501, detail="Stripe is not configured.")

    price_id = STRIPE_PRICE_MAP.get(req.tier)
    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid tier requested.")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{settings.frontend_url}/settings/subscription?success=true",
            cancel_url=f"{settings.frontend_url}/settings/subscription?canceled=true",
            client_reference_id=user.user_id,
            customer_email=user.email,
        )
        return {"url": session.url}
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        raise HTTPException(status_code=500, detail="Could not create checkout session.")


@router.post("/webhook", summary="Stripe Webhook Handler")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header or not settings.stripe_webhook_secret:
        raise HTTPException(status_code=400, detail="Webhook misconfigured.")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    db = get_db()
    now = datetime.now(timezone.utc)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get("client_reference_id")
        
        if not user_id:
            logger.warning("Checkout session missing client_reference_id")
            return {"status": "ok"}
            
        # Optional: Retrieve the subscription or line items to know which tier was purchased.
        # For simplicity, if we knew they bought Pro:
        # Note: robust implementations will map the session's subscription's price ID back to a tier.
        
        # Here we mock retrieving the tier for demonstration.
        # In production: retrieve subscription -> get price ID -> map to tier
        purchased_tier = Tier.pro  # MOCK
        credits_to_grant = TIER_CREDIT_ALLOTMENT[purchased_tier]
        
        # 1. Update user document
        await db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "tier": purchased_tier.value,
                "credit_balance": credits_to_grant,  # Option: reset completely instead of rollover
                "updated_at": now
            }}
        )
        
        # 2. Add transaction to ledger
        tx_doc = {
            "user_id": user_id,
            "type": "grant",
            "amount": credits_to_grant,
            "source": "subscription_renewal",
            "created_at": now,
        }
        event_id = event.get("id") if event else None
        if event_id:
            tx_doc["provider_event_id"] = event_id

        await db.credit_transactions.insert_one(tx_doc)
        
        logger.info(f"Granted {credits_to_grant} credits to {user_id} for {purchased_tier.value}")

    return {"status": "success"}

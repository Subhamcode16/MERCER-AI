"""
Mercer AI — Supabase JWT Decoder

Pure utility — no FastAPI dependency injection here.
Used by auth/dependencies.py to verify Supabase tokens locally
without making a network call to Supabase on every request.

All jwt.exceptions.InvalidTokenError subclasses bubble up to the
caller (auth/dependencies.py), which converts them into HTTP 401.
"""
import jwt
from jwt import PyJWKClient

from app.config import get_settings

settings = get_settings()

jwks_url = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"
jwk_client = PyJWKClient(
    jwks_url
)

def decode_supabase_jwt(token: str) -> dict:
    """
    Decode and verify a Supabase-issued JWT locally.

    Validates:
    - Signature   — using JWKS for ES256/RS256, fallback to HS256 secret
    - Expiry      — rejects tokens past their exp claim
    - Algorithm   — ES256, RS256, or HS256

    Returns:
        dict of decoded claims (sub, email, email_confirmed, exp, iss, ...)

    Raises:
        jwt.exceptions.ExpiredSignatureError   — token has expired
        jwt.exceptions.InvalidSignatureError   — token was tampered with
        jwt.exceptions.DecodeError             — malformed token
        jwt.exceptions.InvalidTokenError       — any other JWT problem
    """
    try:
        # Try to get signing key from JWKS (for ES256/RS256)
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256", "HS256"],
            options={"verify_aud": False},
        )
    except Exception as e:
        import traceback
        print("JWK Fetch failed:", type(e).__name__, str(e))
        try:
            unverified_header = jwt.get_unverified_header(token)
            print("Token unverified header:", unverified_header)
        except Exception as header_e:
            print("Could not get unverified header:", str(header_e))

        # Fallback for HS256 tokens that don't have a kid in JWKS
        try:
            return jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        except Exception as fallback_e:
            print("Fallback jwt.decode failed:", type(fallback_e).__name__, str(fallback_e))
            raise

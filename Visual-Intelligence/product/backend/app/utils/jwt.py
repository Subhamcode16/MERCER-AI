"""
Mercer AI — Supabase JWT Decoder

Pure utility — no FastAPI dependency injection here.
Used by auth/dependencies.py to verify Supabase tokens locally
without making a network call to Supabase on every request.

Algorithm strategy:
  1. Fetch signing key from Supabase JWKS endpoint (ES256/RS256).
     Pass the PyJWK object directly to jwt.decode() so PyJWT auto-derives
     the algorithm from key.algorithm_name — no risk of alg mismatch.
  2. If the JWKS endpoint is unreachable (network error), fall back to
     local HS256 verification using the SUPABASE_JWT_SECRET from .env.

All jwt.exceptions.InvalidTokenError subclasses bubble up to the
caller (auth/dependencies.py), which converts them into HTTP 401.
"""
import base64
import logging

import jwt
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientConnectionError

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

jwks_url = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"

# cache_keys=True: LRU-cache the PyJWK objects so we don't re-fetch on every
# request. cache_jwk_set=True (default): cache the raw JWKS JSON for 5 minutes.
jwk_client = PyJWKClient(jwks_url, cache_keys=True)


def _get_hs256_secret() -> bytes:
    """
    Supabase JWT secrets are base64-encoded in the Supabase dashboard
    and in the .env file. PyJWT needs the raw bytes, not the base64 string.
    We try base64 decode first; if it fails, use the raw string as bytes.
    """
    raw = settings.supabase_jwt_secret
    try:
        return base64.b64decode(raw + "==")  # pad to avoid padding errors
    except Exception:
        return raw.encode("utf-8")


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
    # ── Path 1: JWKS verification (ES256 / RS256) ─────────────────────────────
    try:
        # get_signing_key_from_jwt fetches the JWKS endpoint and returns a
        # PyJWK object whose .algorithm_name matches the 'alg' header.
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        # CRITICAL: pass the PyJWK object — NOT signing_key.key (raw bytes).
        # When a PyJWK is passed, PyJWT reads key.algorithm_name automatically,
        # so the algorithms list is derived correctly and no mismatch can occur.
        return jwt.decode(
            token,
            signing_key,                  # PyJWK object — alg auto-derived
            algorithms=[signing_key.algorithm_name],
            options={"verify_aud": False},
        )

    except PyJWKClientConnectionError as conn_err:
        # JWKS endpoint unreachable (network issue) — try HS256 fallback.
        logger.warning(
            "JWKS endpoint unreachable, falling back to HS256: %s", conn_err
        )

    except jwt.exceptions.InvalidTokenError:
        # Token is genuinely invalid (expired, bad signature, wrong alg).
        # Do NOT fall through to HS256 — re-raise immediately so the caller
        # returns 401 instead of trying an inappropriate algorithm.
        raise

    # ── Path 2: HS256 fallback (JWKS network failure only) ───────────────────
    secret_bytes = _get_hs256_secret()
    return jwt.decode(
        token,
        secret_bytes,
        algorithms=["HS256"],
        options={"verify_aud": False},
    )

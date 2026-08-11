"""
Mercer AI — Security Utilities

Provides rate limiting (SlowAPI) instances, JWT verification, and other global security components.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Dict, Any

from app.config import get_settings

settings = get_settings()

# Global rate limiter using Redis for distributed rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis_url if settings.environment != "development" else "memory://"
)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify the Supabase JWT.
    Returns the decoded token payload (containing 'sub' which is the user_id).
    """
    token = credentials.credentials
    try:
        # Supabase uses HS256 with the JWT secret
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

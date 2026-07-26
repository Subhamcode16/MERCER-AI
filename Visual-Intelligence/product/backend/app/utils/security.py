"""
Mercer AI — Security Utilities

Provides rate limiting (SlowAPI) instances and other global security components.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Global rate limiter using the client's remote address
limiter = Limiter(key_func=get_remote_address)

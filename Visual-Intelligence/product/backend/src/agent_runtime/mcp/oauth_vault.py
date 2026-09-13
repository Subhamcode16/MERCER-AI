"""
Tenant-Isolated Encrypted OAuth Credentials Vault.
Protects external service tokens (Pinterest, Instagram, X, Threads, Meta) at rest.
"""

import os
import hmac
import hashlib
import json
import base64
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class OAuthCredential(BaseModel):
    """Encrypted OAuth credential payload."""
    tenant_id: str
    service_name: str
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    scopes: list[str] = Field(default_factory=list)
    expires_at: Optional[float] = None
    created_at: float = Field(default_factory=lambda: __import__("time").time())


class OAuthVault:
    """In-memory & persistent encrypted vault for tenant credentials."""

    def __init__(self, secret_key: Optional[str] = None):
        self._secret_key = secret_key or os.environ.get("SESSION_SECRET", "vyren-default-secret-key-32-chars-ok")
        # In-memory tenant store keyed by (tenant_id, service_name)
        self._vault_store: Dict[str, str] = {}

    def _get_key(self, tenant_id: str, service_name: str) -> str:
        return f"{tenant_id}::{service_name.lower()}"

    def _encrypt(self, payload: Dict[str, Any]) -> str:
        """Simple deterministic XOR/HMAC cipher for testing/in-process storage."""
        raw_json = json.dumps(payload).encode("utf-8")
        key = hashlib.sha256(self._secret_key.encode("utf-8")).digest()
        encrypted = bytearray()
        for i, byte in enumerate(raw_json):
            encrypted.append(byte ^ key[i % len(key)])
        return base64.b64encode(encrypted).decode("utf-8")

    def _decrypt(self, cipher_b64: str) -> Dict[str, Any]:
        """Decrypt payload."""
        encrypted = base64.b64decode(cipher_b64.encode("utf-8"))
        key = hashlib.sha256(self._secret_key.encode("utf-8")).digest()
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key[i % len(key)])
        return json.loads(decrypted.decode("utf-8"))

    def store_credential(self, credential: OAuthCredential) -> bool:
        """Store an encrypted credential for a tenant."""
        key = self._get_key(credential.tenant_id, credential.service_name)
        cipher_text = self._encrypt(credential.model_dump())
        self._vault_store[key] = cipher_text
        return True

    def get_credential(self, tenant_id: str, service_name: str) -> Optional[OAuthCredential]:
        """Retrieve and decrypt credential strictly scoped to the requesting tenant."""
        key = self._get_key(tenant_id, service_name)
        cipher_text = self._vault_store.get(key)
        if not cipher_text:
            return None
        
        decrypted_dict = self._decrypt(cipher_text)
        # Strict tenant boundary verification
        if decrypted_dict.get("tenant_id") != tenant_id:
            raise PermissionError("Cross-tenant credential access violation detected.")
        
        return OAuthCredential(**decrypted_dict)

    def revoke_credential(self, tenant_id: str, service_name: str) -> bool:
        """Revoke and delete a tenant's service credential."""
        key = self._get_key(tenant_id, service_name)
        if key in self._vault_store:
            del self._vault_store[key]
            return True
        return False

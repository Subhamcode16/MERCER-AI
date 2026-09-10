"""
Phase 23 Secret Operations Audit Logger.
"""
import logging
import uuid
import time
from typing import List, Dict, Any
from src.secret_operations.secret_models import SecretAuditRecord, CredentialDomain

logger = logging.getLogger(__name__)

class SecretAuditLogger:
    """Logs all secret access, rotation, and revocation events."""

    def __init__(self):
        self._audit_records: List[SecretAuditRecord] = []

    def record_access(self, secret_name: str, domain: CredentialDomain, action: str, actor: str, success: bool = True, details: Dict[str, Any] = None) -> SecretAuditRecord:
        rec = SecretAuditRecord(
            audit_id=str(uuid.uuid4()),
            secret_name=secret_name,
            domain=domain,
            action=action,
            actor=actor,
            timestamp=time.time(),
            success=success,
            details=details or {}
        )
        self._audit_records.append(rec)
        logger.info(f"Secret Audit: {action} on {secret_name} [{domain.value}] by {actor} (Success: {success})")
        return rec

    def list_records(self) -> List[SecretAuditRecord]:
        return list(self._audit_records)

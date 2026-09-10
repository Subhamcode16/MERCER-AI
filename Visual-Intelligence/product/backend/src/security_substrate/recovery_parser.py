"""
IF-RECOVER-001 Capability Payload Parser and Recovery Manager implementation.
Enforces 10-field schema validation, freshness, replay defense, and out-of-band state reset.
"""

import time
import threading
import uuid
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .epistemic_state import EpistemicState
from .assurance_loop import AssuranceLoopController, ConsumedNonceCache
from .exceptions import (
    FailClosedException,
    MalformedEvidenceException,
    ReplayAttackException,
    StaleTimestampException,
    InvalidStateTransitionException,
)
from .crypto_utils import sign_evidence_payload, verify_evidence_signature

DEFAULT_SYSTEM_ID = "SYSTEM_VISUAL_INTELLIGENCE_001"
DEFAULT_PROTOCOL_VERSION = "1.0"
DEFAULT_OPERATION_ID = "RESET_LEDGER_CHAIN"
DEFAULT_AUTHORIZATION_SCOPE = "SCOPE_ADMIN_RECOVERY"
MAX_RECOVERY_FRESHNESS_SECONDS = 900.0  # 15 minutes


@dataclass
class RecoveryPayload:
    """
    Mandatory 10-Field Capability Payload Schema for out-of-band recovery.
    """
    system_id: str
    recovery_request_id: str
    unique_nonce: str
    operation_id: str
    authorization_scope: str
    trust_anchor_id: str
    protocol_version: str
    creation_time: float
    expiration_time: float
    current_recovery_epoch: int


@dataclass
class RecoveryAuthorizationResult:
    """
    Authorization result returned by CapabilityPayloadParser.
    """
    status: str  # "SUCCESS" or "FAILED"
    system_id: str
    recovery_epoch: int
    authorization_scope: str
    reason: str


class RecoveryEpochStore:
    """
    Thread-safe storage for the system recovery epoch counter.
    """
    def __init__(self, initial_epoch: int = 1):
        self._lock = threading.RLock()
        self._epoch: int = initial_epoch

    def get_epoch(self) -> int:
        with self._lock:
            return self._epoch

    def increment_epoch(self) -> int:
        with self._lock:
            self._epoch += 1
            return self._epoch

    def set_epoch(self, epoch: int) -> None:
        with self._lock:
            self._epoch = epoch


class CapabilityPayloadParser:
    """
    IF-RECOVER-001 Capability Payload Parser.
    Parses, validates schema, verifies freshness & replay defense, and authenticates signatures.
    """
    def __init__(
        self,
        system_id: str = DEFAULT_SYSTEM_ID,
        nonce_cache: Optional[ConsumedNonceCache] = None,
        epoch_store: Optional[RecoveryEpochStore] = None,
    ):
        self.system_id = system_id
        self.nonce_cache = nonce_cache or ConsumedNonceCache()
        self.epoch_store = epoch_store or RecoveryEpochStore()

    def _canonical_payload_string(self, p: RecoveryPayload) -> str:
        return f"{p.system_id}:{p.recovery_request_id}:{p.unique_nonce}:{p.operation_id}:{p.authorization_scope}:{p.trust_anchor_id}:{p.protocol_version}:{p.creation_time}:{p.expiration_time}:{p.current_recovery_epoch}"

    def parse_and_validate(
        self,
        raw_payload: Dict[str, Any],
        signature: str,
        domain_signing_key: bytes
    ) -> RecoveryAuthorizationResult:
        """
        IF-RECOVER-001 Interface Method: Structural, semantic, and cryptographic payload validation.
        """
        if not raw_payload or not isinstance(raw_payload, dict):
            raise MalformedEvidenceException("Recovery payload must be a non-empty dictionary")

        if not signature or not isinstance(signature, str):
            raise FailClosedException("Invalid or missing cryptographic signature")

        if not domain_signing_key or not isinstance(domain_signing_key, bytes):
            raise FailClosedException("Invalid domain signing key provided")

        # 1. Structural 10-Field Schema Precondition Verification
        required_fields = [
            "system_id", "recovery_request_id", "unique_nonce", "operation_id",
            "authorization_scope", "trust_anchor_id", "protocol_version",
            "creation_time", "expiration_time", "current_recovery_epoch"
        ]
        for field in required_fields:
            if field not in raw_payload or raw_payload[field] is None:
                raise MalformedEvidenceException(f"Missing mandatory field in recovery payload: {field}")
            val = raw_payload[field]
            if isinstance(val, bool):
                raise MalformedEvidenceException(f"Boolean value not permitted for field: {field}")
            if isinstance(val, str) and not val.strip():
                raise MalformedEvidenceException(f"Empty or whitespace-only string in recovery payload: {field}")

        try:
            payload = RecoveryPayload(
                system_id=str(raw_payload["system_id"]),
                recovery_request_id=str(raw_payload["recovery_request_id"]),
                unique_nonce=str(raw_payload["unique_nonce"]),
                operation_id=str(raw_payload["operation_id"]),
                authorization_scope=str(raw_payload["authorization_scope"]),
                trust_anchor_id=str(raw_payload["trust_anchor_id"]),
                protocol_version=str(raw_payload["protocol_version"]),
                creation_time=float(raw_payload["creation_time"]),
                expiration_time=float(raw_payload["expiration_time"]),
                current_recovery_epoch=int(raw_payload["current_recovery_epoch"]),
            )
        except (ValueError, TypeError) as e:
            raise MalformedEvidenceException(f"Invalid field data type in recovery payload: {str(e)}") from e

        # 2. Scope & Identity Binding Verification
        if payload.system_id != self.system_id:
            raise MalformedEvidenceException(f"Mismatched system_id: {payload.system_id} (expected {self.system_id})")

        if payload.operation_id != DEFAULT_OPERATION_ID:
            raise MalformedEvidenceException(f"Unauthorized operation_id: {payload.operation_id}")

        if payload.authorization_scope != DEFAULT_AUTHORIZATION_SCOPE:
            raise MalformedEvidenceException(f"Unauthorized authorization_scope: {payload.authorization_scope}")

        if payload.protocol_version != DEFAULT_PROTOCOL_VERSION:
            raise MalformedEvidenceException(f"Unsupported protocol_version: {payload.protocol_version}")

        # 3. Epoch & Replay Verification
        current_epoch = self.epoch_store.get_epoch()
        if payload.current_recovery_epoch < current_epoch:
            raise ReplayAttackException(
                f"Outdated recovery epoch: {payload.current_recovery_epoch} (active epoch is {current_epoch})"
            )

        if not self.nonce_cache.check_and_add(payload.unique_nonce):
            raise ReplayAttackException(f"Replayed recovery nonce detected: {payload.unique_nonce}")

        # 4. Freshness Verification
        now = time.time()
        if payload.expiration_time < payload.creation_time:
            raise StaleTimestampException("Expiration time cannot be earlier than creation time")

        if payload.creation_time > now + 5.0:  # 5s max future skew
            raise StaleTimestampException(f"Future-dated creation timestamp: creation={payload.creation_time}, now={now}")

        if now > payload.expiration_time:
            raise StaleTimestampException(f"Expired recovery payload: expiration={payload.expiration_time}, now={now}")

        if (payload.expiration_time - payload.creation_time) > MAX_RECOVERY_FRESHNESS_SECONDS + 0.1:
            raise StaleTimestampException("Expiration window exceeds max 15-minute limit")

        # 5. Cryptographic Signature Authentication
        payload_str = self._canonical_payload_string(payload)
        import hmac, hashlib
        expected_sig = hmac.new(domain_signing_key, payload_str.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_sig, signature):
            raise FailClosedException("Recovery signature verification failed")

        return RecoveryAuthorizationResult(
            status="SUCCESS",
            system_id=payload.system_id,
            recovery_epoch=payload.current_recovery_epoch,
            authorization_scope=payload.authorization_scope,
            reason="Recovery capability payload successfully validated."
        )


class RecoveryManager:
    """
    IF-RECOVER-001 Recovery Manager.
    Orchestrates payload parsing and out-of-band administrative state reset.
    """
    def __init__(
        self,
        parser: Optional[CapabilityPayloadParser] = None,
        epoch_store: Optional[RecoveryEpochStore] = None,
    ):
        self.epoch_store = epoch_store or RecoveryEpochStore()
        self.parser = parser or CapabilityPayloadParser(epoch_store=self.epoch_store)

    def execute_emergency_recovery(
        self,
        raw_payload: Dict[str, Any],
        signature: str,
        domain_signing_key: bytes,
        assurance_controller: AssuranceLoopController
    ) -> RecoveryAuthorizationResult:
        """
        Executes emergency recovery reset.
        State transition: RECOVERY_REQUIRED -> UNKNOWN (NEVER directly to VERIFIED).
        """
        if not assurance_controller or not isinstance(assurance_controller, AssuranceLoopController):
            raise FailClosedException("RecoveryManager requires a valid AssuranceLoopController instance.")

        try:
            # 1. Parse and validate recovery payload
            auth_result = self.parser.parse_and_validate(raw_payload, signature, domain_signing_key)

            # 2. Execute state reset strictly to UNKNOWN
            assurance_controller.execute_recovery_reset(recovery_auth_valid=True)

            # 3. Increment system recovery epoch post-reset
            self.epoch_store.increment_epoch()

            return auth_result

        except Exception:
            assurance_controller.store.force_blocked()
            raise

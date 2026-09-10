"""
Phase 26 Governed Worker Handoffs.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import hashlib
import json
import uuid

from src.creative_workforce.worker_identity.models import WorkerIdentity
from src.creative_workforce.worker_lifecycle.lifecycle_engine import WorkerLifecycleManager
from src.creative_workforce.capability_binding.manifest import CapabilityResolver


class HandoffStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"


class HandoffError(Exception):
    pass


@dataclass
class WorkerHandoff:
    handoff_id: str
    room_id: str
    tenant_id: str
    client_id: str
    sender_worker_id: str
    recipient_worker_id: str
    purpose: str
    input_artifacts: List[Dict[str, Any]] = field(default_factory=list)
    artifact_hashes: Dict[str, str] = field(default_factory=dict)
    claims: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    constraints: List[str] = field(default_factory=list)
    requested_action: str = ""
    authorization_status: str = "NOT_REQUIRED"
    status: HandoffStatus = HandoffStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HandoffService:
    """Manages cryptographic, evidence-backed worker-to-worker handoffs."""

    def __init__(self, capability_resolver: CapabilityResolver):
        self.capability_resolver = capability_resolver
        self._handoffs: Dict[str, WorkerHandoff] = {}

    def create_handoff(
        self,
        room_id: str,
        tenant_id: str,
        client_id: str,
        sender_worker_id: str,
        recipient_worker_id: str,
        purpose: str,
        input_artifacts: Optional[List[Dict[str, Any]]] = None,
        claims: Optional[List[str]] = None,
        evidence: Optional[Dict[str, Any]] = None,
        confidence: float = 1.0,
        constraints: Optional[List[str]] = None,
        requested_action: str = "",
    ) -> WorkerHandoff:
        artifacts = input_artifacts or []
        artifact_hashes = {}
        for idx, art in enumerate(artifacts):
            art_id = art.get("artifact_id") or art.get("concept_id") or f"art_{idx}"
            raw = json.dumps(art, sort_keys=True).encode("utf-8")
            artifact_hashes[art_id] = hashlib.sha256(raw).hexdigest()

        handoff_id = f"hoff_{uuid.uuid4().hex[:12]}"
        handoff = WorkerHandoff(
            handoff_id=handoff_id,
            room_id=room_id,
            tenant_id=tenant_id,
            client_id=client_id,
            sender_worker_id=sender_worker_id,
            recipient_worker_id=recipient_worker_id,
            purpose=purpose,
            input_artifacts=artifacts,
            artifact_hashes=artifact_hashes,
            claims=claims or [],
            evidence=evidence or {},
            confidence=confidence,
            constraints=constraints or [],
            requested_action=requested_action,
        )
        self._handoffs[handoff_id] = handoff
        return handoff

    def accept_handoff(self, handoff_id: str, recipient: WorkerIdentity) -> WorkerHandoff:
        handoff = self._handoffs.get(handoff_id)
        if not handoff:
            raise HandoffError(f"Handoff '{handoff_id}' not found")
        if handoff.recipient_worker_id != recipient.worker_id:
            raise HandoffError(f"Worker '{recipient.worker_id}' is not the declared recipient of handoff '{handoff_id}'")
        
        # 1. Assert recipient is executable
        WorkerLifecycleManager.assert_executable(recipient)

        # 2. Assert recipient has capability for requested action if action specified
        if handoff.requested_action:
            self.capability_resolver.assert_capability(recipient.worker_id, handoff.requested_action)

        handoff.status = HandoffStatus.ACCEPTED
        return handoff

    def get_handoff(self, handoff_id: str) -> Optional[WorkerHandoff]:
        return self._handoffs.get(handoff_id)

"""
Phase 23 Persistence Storage Models, Checkpoints, and Ledger Definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import hashlib
import json

class StorageEngineType(str, Enum):
    MEMORY = "MEMORY"
    SQLITE = "SQLITE"
    ATOMIC_FILE = "ATOMIC_FILE"

@dataclass
class StorageRecord:
    key: str
    tenant_id: str
    client_id: str
    data: Dict[str, Any]
    version: int = 1
    checksum: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def compute_checksum(self) -> str:
        payload = json.dumps({
            "key": self.key,
            "tenant_id": self.tenant_id,
            "client_id": self.client_id,
            "data": self.data,
            "version": self.version
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

@dataclass
class WorkflowCheckpoint:
    checkpoint_id: str
    workflow_id: str
    tenant_id: str
    client_id: str
    step_index: int
    step_name: str
    state_payload: Dict[str, Any]
    parent_checkpoint_hash: Optional[str] = None
    checkpoint_hash: str = ""
    timestamp: float = field(default_factory=time.time)
    authorization_token_id: Optional[str] = None

    def compute_hash(self) -> str:
        payload = json.dumps({
            "checkpoint_id": self.checkpoint_id,
            "workflow_id": self.workflow_id,
            "tenant_id": self.tenant_id,
            "client_id": self.client_id,
            "step_index": self.step_index,
            "step_name": self.step_name,
            "state_payload": self.state_payload,
            "parent_checkpoint_hash": self.parent_checkpoint_hash,
            "authorization_token_id": self.authorization_token_id
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

@dataclass
class LedgerEntry:
    entry_id: str
    tenant_id: str
    client_id: str
    event_type: str
    event_data: Dict[str, Any]
    prev_entry_hash: str
    entry_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def compute_hash(self) -> str:
        payload = json.dumps({
            "entry_id": self.entry_id,
            "tenant_id": self.tenant_id,
            "client_id": self.client_id,
            "event_type": self.event_type,
            "event_data": self.event_data,
            "prev_entry_hash": self.prev_entry_hash,
            "timestamp": self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

@dataclass
class BackupMetadata:
    backup_id: str
    created_at: float
    schema_version: str
    record_count: int
    checkpoint_count: int
    ledger_entry_count: int
    content_sha256: str
    tenant_ids: List[str]
    contains_secrets: bool = False

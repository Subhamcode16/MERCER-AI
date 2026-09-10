# Phase 26: Campaign Rooms & Multi-Agent Collaboration Specification

## 1. Overview
A Campaign Room is a structured, collaborative workspace within ILYREN where human creative leads and persistent AI coworkers exchange context, deliberate, share artifacts, and record decisions.

## 2. Invariant Principles
- **Room $\neq$ Authorization Boundary**: Membership in a Campaign Room does not grant execution privileges or cross-tenant visibility.
- **Shared Context $\neq$ Shared Authority**: Workers in the same room maintain their own individual capability manifests and security boundaries.

## 3. Campaign Room Model
```python
@dataclass
class CampaignRoom:
    room_id: str
    tenant_id: str
    client_id: str
    campaign_id: str
    name: str
    status: RoomStatus  # ACTIVE, PAUSED, CLOSED
    participants: Dict[str, str]  # participant_id -> role_or_type ("HUMAN", "WORKER")
    shared_context: Dict[str, Any]
    shared_artifacts: List[Dict[str, Any]]
    activity_log: List[Dict[str, Any]]
    decisions: List[Dict[str, Any]]
    created_at: str
```

## 4. Collaboration Protocol
- Messages carry explicit sender type (`HUMAN` vs `WORKER`), content, claims, and confidence scores.
- Artifacts attached to rooms are cryptographically committed with SHA-256 hashes.
- Decisions are recorded with explicit human approver signatures.

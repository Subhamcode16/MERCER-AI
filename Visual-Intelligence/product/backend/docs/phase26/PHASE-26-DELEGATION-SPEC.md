# Phase 26: Governed Worker Delegation Specification

## 1. Overview
Delegation allows digital coworkers to distribute tasks across specialized roles while strictly preventing privilege transfer and uncontrolled delegation cascades.

## 2. Invariant Principles
- **Collaboration $\neq$ Privilege Transfer**: A worker may delegate work, analysis, or drafting; it may **never** transfer its own capabilities, execution tokens, or authorization status.
- **Strict Depth Limits**: Configurable delegation depth limit (default: Max Depth 3) prevents runaways.
- **Loop Prevention**: Circular delegations (e.g. Worker A $\rightarrow$ Worker B $\rightarrow$ Worker A) are detected and aborted with `DelegationError`.

## 3. Delegation Task Model
```python
@dataclass
class DelegationTask:
    delegation_id: str
    tenant_id: str
    client_id: str
    initiator_id: str
    delegation_chain: List[str]  # e.g., ["human_lead", "planner_01", "cd_01"]
    current_worker_id: str
    task_payload: Dict[str, Any]
    max_depth: int = 3
    status: str = "IN_PROGRESS"
    created_at: str
```

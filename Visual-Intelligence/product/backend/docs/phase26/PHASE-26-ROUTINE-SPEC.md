# Phase 26: Workforce Routines & Trigger Execution Specification

## 1. Overview
Workforce Routines allow organizations to schedule recurring tasks (e.g. daily trend sweeps, weekly aesthetic drift checks) and respond to events in an automated yet bounded manner.

## 2. Invariant Principles
- **Routine $\neq$ Authorization**: Routines can initiate work items, but they **cannot** authorize actions or bypass human approvals for high-risk executions.
- **Advisory / Dry-Run Mode**: Routines produce structured proposals requiring verification before mutation.
- **Replay Protection**: Replay attacks and duplicate runs are blocked using execution nonce caching.
- **Self-Modification Forbidden**: A routine definition cannot grant itself additional capabilities or modify security policy.

## 3. Routine Definition Model
```python
@dataclass
class WorkforceRoutine:
    routine_id: str
    tenant_id: str
    client_id: str
    name: str
    worker_id: str
    skill_id: str
    trigger_type: RoutineTriggerType  # SCHEDULED, EVENT, MANUAL
    cron_expression: Optional[str] = None
    max_runtime_sec: int = 300
    max_delegation_depth: int = 2
    required_approvals: List[str] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    failure_policy: str = "LOG_AND_ABORT"
    status: RoutineStatus = RoutineStatus.ACTIVE
    created_at: str
```

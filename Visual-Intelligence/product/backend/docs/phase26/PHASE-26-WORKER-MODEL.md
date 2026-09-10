# Phase 26: Worker Identity & Organizational Role Model

## 1. Overview
The Worker Identity Model provides stable, persistent digital coworker identities separate from ephemeral session, execution, or underlying LLM identities.

## 2. Worker Identity Structure
```python
@dataclass
class WorkerIdentity:
    worker_id: str
    tenant_id: str
    organization_id: str
    name: str
    role_id: str
    description: str
    status: WorkerStatus  # DRAFT, ACTIVE, PAUSED, RESTRICTED, SUSPENDED, RETIRED
    version: str = "1.0.0"
    owner: str = "SYSTEM"
    memory_policy_id: str = "STANDARD_SCOPED"
    capability_profile_id: str = "DEFAULT"
    skill_profile_id: str = "DEFAULT"
    model_policy_id: str = "DEFAULT"
    created_at: str
    updated_at: str
    metadata: Dict[str, Any]
```

## 3. The 13 Canonical Creative Roles
1. `STRATEGY_DIRECTOR`: High-level market strategy & positioning.
2. `BRAND_INTELLIGENCE`: Brand identity guidelines & tone analysis.
3. `CREATIVE_DIRECTOR`: Visual narrative & art direction concept synthesis.
4. `ART_DIRECTION`: Visual composition & palette formulation.
5. `VISUAL_DNA_SPECIALIST`: Visual DNA token extraction & aesthetic consistency.
6. `CAMPAIGN_PLANNER`: Milestone scheduling & asset dependency tracking.
7. `COPY_STRATEGIST`: Editorial copy, storytelling & narrative framing.
8. `CONTENT_PRODUCER`: Multi-channel packaging & asset formatting.
9. `TREND_RESEARCHER`: Cultural trend tracking & fashion cycle analysis.
10. `QUALITY_REVIEWER`: Aesthetic critique & compliance auditing.
11. `PERFORMANCE_ANALYST`: Campaign telemetry & resonance modeling.
12. `CLIENT_COORDINATOR`: Brief synthesis & feedback intake.
13. `STUDIO_OPERATOR`: Routine scheduling & operational triage.

## 4. Lifecycle State Machine
- `DRAFT` $\rightarrow$ `ACTIVE`
- `ACTIVE` $\rightleftharpoons$ `PAUSED` / `RESTRICTED` / `SUSPENDED`
- `SUSPENDED` $\rightarrow$ `RESTRICTED` $\rightarrow$ `ACTIVE` (Direct jump from `SUSPENDED` to `ACTIVE` is prohibited)
- Terminal state: `RETIRED` (Attribution preserved, execution blocked permanently)

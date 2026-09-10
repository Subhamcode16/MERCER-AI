# Phase 26: Skill Registry, Runtime & Versioning Specification

## 1. Overview
Skills represent discrete, reusable, testable, and attributable capabilities that persistent digital coworkers execute within strict policy constraints.

## 2. Invariant Principles
- **Skill $\neq$ Authority**: A skill describes what a worker knows how to do. It does not grant execution or mutation permissions.
- **Immutable by Version**: Skills are registered under semantic versions (`skill_id@version`, e.g., `creative_direction@1.0.0`). Once registered, a version is immutable.

## 3. Skill Definition Model
```python
@dataclass
class SkillDefinition:
    skill_id: str
    version: str  # SemVer e.g., "1.0.0"
    purpose: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    required_context: List[str]
    required_capabilities: List[str]
    evidence_requirements: List[str]
    risk_class: SkillRiskClass  # LOW, MEDIUM, HIGH, CRITICAL
    validation_suite: str = "DEFAULT"
    owner: str = "SYSTEM"
    status: SkillStatus = SkillStatus.ACTIVE
    created_at: str
```

## 4. Evaluation and Promotion
Prior to production promotion, a skill definition is audited by `SkillEvaluator`:
1. SemVer format check (`major.minor.patch`).
2. Detailed purpose declaration.
3. Prohibited wildcard capability check (`*` forbidden).
4. Schema validation for input and output contracts.

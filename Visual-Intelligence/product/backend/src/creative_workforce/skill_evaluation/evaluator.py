"""
Phase 26 Skill Evaluation Harness.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any
from src.creative_workforce.skill_registry.models import SkillDefinition, SkillStatus


@dataclass
class SkillEvaluationReport:
    skill_id: str
    version: str
    passed: bool
    score: float
    checks: Dict[str, bool] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)


class SkillEvaluator:
    """Evaluates skills against quality, schema compliance, and boundary safety."""

    @staticmethod
    def evaluate_skill(skill: SkillDefinition) -> SkillEvaluationReport:
        checks = {}
        findings = []

        # 1. Check version format
        version_parts = skill.version.split(".")
        checks["semver_format"] = len(version_parts) == 3 and all(p.isdigit() for p in version_parts)
        if not checks["semver_format"]:
            findings.append("Version does not follow standard SemVer format (e.g. 1.0.0)")

        # 2. Check purpose definition
        checks["purpose_defined"] = len(skill.purpose.strip()) > 10
        if not checks["purpose_defined"]:
            findings.append("Skill purpose description is missing or too brief")

        # 3. Check capability declarations (no wildcards)
        has_wildcard = any("*" in cap for cap in skill.required_capabilities)
        checks["no_wildcard_capabilities"] = not has_wildcard
        if has_wildcard:
            findings.append("Skill requests wildcard capabilities")

        # 4. Check schema validity
        checks["schemas_present"] = isinstance(skill.inputs, dict) and isinstance(skill.outputs, dict)

        passed = all(checks.values())
        score = 1.0 if passed else (sum(1 for v in checks.values() if v) / len(checks))

        return SkillEvaluationReport(
            skill_id=skill.skill_id,
            version=skill.version,
            passed=passed,
            score=score,
            checks=checks,
            findings=findings,
        )

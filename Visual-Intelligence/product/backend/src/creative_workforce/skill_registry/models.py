"""
Phase 26 Versioned Immutable Skill Models.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class SkillRiskClass(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SkillStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


@dataclass
class SkillDefinition:
    skill_id: str
    version: str  # SemVer e.g., "1.0.0"
    purpose: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    required_context: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    evidence_requirements: List[str] = field(default_factory=list)
    risk_class: SkillRiskClass = SkillRiskClass.LOW
    validation_suite: str = "DEFAULT"
    owner: str = "SYSTEM"
    status: SkillStatus = SkillStatus.ACTIVE
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def full_key(self) -> str:
        return f"{self.skill_id}@{self.version}"

"""
Phase 26 Skill Registry.
"""
from typing import Dict, List, Optional
from src.creative_workforce.skill_registry.models import SkillDefinition, SkillStatus


class SkillRegistryError(Exception):
    pass


class SkillRegistry:
    """Registry managing immutable versioned skills."""

    def __init__(self):
        # Keyed by "skill_id@version"
        self._skills: Dict[str, SkillDefinition] = {}

    def register_skill(self, skill: SkillDefinition) -> SkillDefinition:
        key = skill.full_key
        if key in self._skills:
            raise SkillRegistryError(f"Skill version '{key}' is already registered and immutable")
        self._skills[key] = skill
        return skill

    def get_skill(self, skill_id: str, version: Optional[str] = None) -> Optional[SkillDefinition]:
        if version:
            return self._skills.get(f"{skill_id}@{version}")
        
        # If no version requested, find latest active version
        matching = [s for s in self._skills.values() if s.skill_id == skill_id]
        if not matching:
            return None
        # Sort by version string descending
        matching.sort(key=lambda s: s.version, reverse=True)
        return matching[0]

    def list_skills(self, status: Optional[SkillStatus] = None) -> List[SkillDefinition]:
        if status:
            return [s for s in self._skills.values() if s.status == status]
        return list(self._skills.values())

"""
Phase 14-21 Staff Dossier Data Models
--------------------------------------
Dataclasses representing exhaustive staff dossiers including roles, capabilities,
skills, knowledge domains, universal system instructions, tool bindings, and model routing.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from src.creative_workforce.organization_models import Department, Role, AuthorityClass

@dataclass(frozen=True)
class SkillDefinition:
    """Detailed definition of a staff skill."""
    skill_id: str
    name: str
    category: str
    proficiency_level: str  # Expert, Master, Lead
    description: str

@dataclass(frozen=True)
class ToolBinding:
    """Tool schema bound to a staff identity."""
    tool_id: str
    tool_name: str
    description: str
    input_schema_keys: List[str]

@dataclass(frozen=True)
class StaffDossier:
    """Complete, exhaustive dossier for a workforce staff identity."""
    staff_id: str
    name: str
    handle: str
    role: Role
    department: Department
    authority_class: AuthorityClass
    title: str
    bio: str
    primary_skills: List[SkillDefinition]
    capabilities: List[str]
    knowledge_domains: List[str]
    system_instruction: str
    bound_tools: List[ToolBinding]
    target_model: str
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the dossier into a JSON-compatible dictionary for API responses."""
        return {
            "staff_id": self.staff_id,
            "name": self.name,
            "handle": self.handle,
            "role": self.role.value,
            "department": self.department.value,
            "authority_class": self.authority_class.value,
            "title": self.title,
            "bio": self.bio,
            "primary_skills": [
                {
                    "skill_id": s.skill_id,
                    "name": s.name,
                    "category": s.category,
                    "proficiency_level": s.proficiency_level,
                    "description": s.description,
                }
                for s in self.primary_skills
            ],
            "capabilities": self.capabilities,
            "knowledge_domains": self.knowledge_domains,
            "system_instruction": self.system_instruction,
            "bound_tools": [
                {
                    "tool_id": t.tool_id,
                    "tool_name": t.tool_name,
                    "description": t.description,
                    "input_schema_keys": t.input_schema_keys,
                }
                for t in self.bound_tools
            ],
            "target_model": self.target_model,
            "version": self.version,
        }

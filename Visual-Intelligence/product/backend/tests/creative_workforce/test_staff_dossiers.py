"""
Phase 14-21 Test Staff Dossiers
--------------------------------
Tests canonical 13 staff dossiers, schema validity, serialization, and department completeness.
"""

import pytest
from src.creative_workforce.organization_models import Department, Role, AuthorityClass
from src.creative_workforce.dossiers import (
    StaffDossier,
    SkillDefinition,
    ToolBinding,
    STAFF_DOSSIERS,
    get_dossier,
    list_dossiers,
    list_dossiers_by_department,
)
from src.creative_workforce import StaffRegistry

def test_canonical_13_dossiers_present():
    dossiers = list_dossiers()
    assert len(dossiers) == 13
    assert len(STAFF_DOSSIERS) == 13

def test_all_departments_represented():
    departments = {d.department for d in list_dossiers()}
    assert Department.STRATEGY in departments
    assert Department.CREATIVE in departments
    assert Department.INTELLIGENCE in departments
    assert Department.CONTENT in departments
    assert Department.QUALITY in departments

def test_dossier_fields_and_serialization():
    cd = get_dossier("creative_director_01")
    assert cd is not None
    assert cd.name == "Maximilian Sterling"
    assert cd.role == Role.CREATIVE_DIRECTOR
    assert cd.department == Department.CREATIVE
    assert cd.authority_class == AuthorityClass.PROPOSE
    assert len(cd.primary_skills) >= 3
    assert len(cd.bound_tools) >= 2
    assert cd.target_model == "gemini-2.5-flash"
    assert "Executive Creative Director" in cd.system_instruction

    data = cd.to_dict()
    assert data["staff_id"] == "creative_director_01"
    assert data["department"] == "STRATEGY" or data["department"] == "CREATIVE"
    assert isinstance(data["primary_skills"], list)
    assert isinstance(data["bound_tools"], list)
    assert len(data["bound_tools"]) >= 2
    assert "tool_id" in data["bound_tools"][0]

def test_staff_registry_dossier_integration():
    registry = StaffRegistry()
    dossier = registry.get_dossier("brand_strategist_01")
    assert dossier is not None
    assert dossier.name == "Elena Rostova"
    assert len(dossier.knowledge_domains) >= 3

    all_dossiers = registry.list_dossiers()
    assert len(all_dossiers) == 13

    quality_dossiers = registry.list_dossiers_by_department(Department.QUALITY)
    assert len(quality_dossiers) == 2

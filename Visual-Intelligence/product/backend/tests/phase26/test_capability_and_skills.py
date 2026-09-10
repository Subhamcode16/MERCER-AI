"""
Phase 26 Unit Tests: Capability Manifests & Immutable Versioned Skills.
"""
import pytest
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus
from src.creative_workforce.capability_binding.manifest import (
    CapabilityManifest,
    CapabilityResolver,
    CapabilityError,
)
from src.creative_workforce.skill_registry.models import (
    SkillDefinition,
    SkillRiskClass,
    SkillStatus,
)
from src.creative_workforce.skill_registry.registry import (
    SkillRegistry,
    SkillRegistryError,
)
from src.creative_workforce.skill_runtime.runtime import SkillRuntime, SkillExecutionResult
from src.creative_workforce.skill_evaluation.evaluator import SkillEvaluator


def test_capability_resolver_and_forbidden_override():
    resolver = CapabilityResolver()
    manifest = CapabilityManifest(
        worker_id="cd_01",
        allowed_capabilities={"campaign.read", "creative_direction.create", "render.request"},
        forbidden_capabilities={"production.deploy", "policy.modify"},
    )
    resolver.register_manifest(manifest)

    assert resolver.has_capability("cd_01", "creative_direction.create") is True
    assert resolver.has_capability("cd_01", "production.deploy") is False
    assert resolver.has_capability("cd_01", "unregistered_cap") is False

    # Wildcard rejection
    with pytest.raises(CapabilityError):
        resolver.register_manifest(
            CapabilityManifest(
                worker_id="rogue_01",
                allowed_capabilities={"*"},
            )
        )


def test_skill_registry_immutability():
    registry = SkillRegistry()

    skill_v1 = SkillDefinition(
        skill_id="creative_direction",
        version="1.0.0",
        purpose="Generate strategic creative direction for campaigns",
        required_capabilities=["creative_direction.create", "campaign.read"],
        risk_class=SkillRiskClass.MEDIUM,
    )
    registry.register_skill(skill_v1)

    assert registry.get_skill("creative_direction", version="1.0.0") is not None
    assert registry.get_skill("creative_direction").version == "1.0.0"

    # Cannot re-register same version
    with pytest.raises(SkillRegistryError):
        registry.register_skill(skill_v1)

    # Registering v2 is allowed
    skill_v2 = SkillDefinition(
        skill_id="creative_direction",
        version="2.0.0",
        purpose="Advanced multi-modal creative direction",
        required_capabilities=["creative_direction.create", "campaign.read", "visual_dna.read"],
        risk_class=SkillRiskClass.MEDIUM,
    )
    registry.register_skill(skill_v2)
    assert registry.get_skill("creative_direction").version == "2.0.0"


def test_skill_runtime_execution_and_evaluator():
    resolver = CapabilityResolver()
    resolver.register_manifest(
        CapabilityManifest(
            worker_id="cd_01",
            allowed_capabilities={"creative_direction.create", "campaign.read"},
        )
    )

    worker = WorkerIdentity(
        worker_id="cd_01",
        tenant_id="tenant_alpha",
        organization_id="org_1",
        name="Elena",
        role_id="CREATIVE_DIRECTOR",
        description="CD",
        status=WorkerStatus.ACTIVE,
    )

    skill = SkillDefinition(
        skill_id="creative_direction",
        version="1.0.0",
        purpose="Generate strategic creative direction for campaigns",
        required_capabilities=["creative_direction.create", "campaign.read"],
    )

    runtime = SkillRuntime(capability_resolver=resolver)
    res = runtime.execute_skill(
        worker=worker,
        skill=skill,
        inputs={"brand_name": "Haute Couture 2026"},
    )
    assert res.status == "SUCCESS"
    assert res.worker_id == "cd_01"

    # Evaluator check
    report = SkillEvaluator.evaluate_skill(skill)
    assert report.passed is True
    assert report.score == 1.0

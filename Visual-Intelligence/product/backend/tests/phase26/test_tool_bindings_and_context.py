"""
Phase 26 Unit Tests: Tool Capability Bindings & Typed Context Resolution.
"""
import pytest
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus
from src.creative_workforce.capability_binding.manifest import (
    CapabilityManifest,
    CapabilityResolver,
)
from src.creative_workforce.tool_bindings.connectors import (
    ToolDefinition,
    ToolBindingManager,
    ToolAccessError,
)
from src.creative_workforce.context_resolution.resolver import (
    ContextResolver,
    ContextCategory,
    EpistemicType,
)


def test_tool_binding_and_capability_guard():
    resolver = CapabilityResolver()
    resolver.register_manifest(
        CapabilityManifest(
            worker_id="cd_01",
            allowed_capabilities={"canva.read"},
        )
    )

    manager = ToolBindingManager(capability_resolver=resolver)
    manager.register_tool(
        ToolDefinition(
            tool_id="canva_reader",
            name="Canva Asset Reader",
            description="Reads canva moodboards",
            required_capability="canva.read",
        )
    )
    manager.register_tool(
        ToolDefinition(
            tool_id="canva_creator",
            name="Canva Design Creator",
            description="Creates canva designs",
            required_capability="canva.create_design",
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

    # Allowed invocation
    res = manager.invoke_tool("canva_reader", worker, params={"board_id": "b_123"})
    assert res["status"] == "SUCCESS"

    # Forbidden invocation (lacks canva.create_design)
    with pytest.raises(ToolAccessError):
        manager.invoke_tool("canva_creator", worker, params={"template_id": "t_456"})


def test_typed_context_resolution():
    raw_inputs = {
        "brand_guidelines": "Minimalist monochrome, strict serif typography",
        "visual_dna_tokens": ["editorial", "monochrome", "35mm_film"],
        "trend_hypothesis": "Rise in retro-futurist tailoring for Q4",
    }

    items = ContextResolver.assemble_campaign_context(
        tenant_id="tenant_alpha",
        client_id="client_haute",
        campaign_id="C-2026-AUTUMN",
        raw_inputs=raw_inputs,
    )

    assert len(items) == 3
    brand_item = next(i for i in items if i.category == ContextCategory.BRAND)
    assert brand_item.epistemic_type == EpistemicType.FACT

    trend_item = next(i for i in items if i.category == ContextCategory.DOMAIN)
    assert trend_item.epistemic_type == EpistemicType.HYPOTHESIS
    assert trend_item.confidence == 0.75

"""
Phase 26 Canonical Worker Roles & Default Capability Profiles.
"""
from typing import Dict, List
from src.creative_workforce.worker_identity.models import WorkerRole, RoleIdentity

CANONICAL_ROLES: Dict[str, RoleIdentity] = {
    WorkerRole.STRATEGY_DIRECTOR.value: RoleIdentity(
        role_id=WorkerRole.STRATEGY_DIRECTOR.value,
        role_name="Strategy Director",
        description="High-level campaign strategy, market positioning, audience segmentation",
        default_capabilities=[
            "strategy.propose",
            "campaign.read",
            "brand.read",
            "market.analyze",
            "handoff.create",
        ],
    ),
    WorkerRole.BRAND_INTELLIGENCE.value: RoleIdentity(
        role_id=WorkerRole.BRAND_INTELLIGENCE.value,
        role_name="Brand Intelligence Specialist",
        description="Brand identity guidelines, archetype synthesis, tone analysis",
        default_capabilities=[
            "brand.read",
            "brand.audit",
            "visual_dna.read",
            "guideline.verify",
            "handoff.create",
        ],
    ),
    WorkerRole.CREATIVE_DIRECTOR.value: RoleIdentity(
        role_id=WorkerRole.CREATIVE_DIRECTOR.value,
        role_name="Creative Director",
        description="Creative concept development, overarching visual narrative, art direction guidance",
        default_capabilities=[
            "campaign.read",
            "brand.read",
            "visual_dna.read",
            "creative_direction.create",
            "render.request",
            "review.request",
            "handoff.create",
        ],
    ),
    WorkerRole.ART_DIRECTION.value: RoleIdentity(
        role_id=WorkerRole.ART_DIRECTION.value,
        role_name="Art Director",
        description="Visual composition, color palette formulation, styling direction",
        default_capabilities=[
            "visual_dna.read",
            "visual_direction.create",
            "palette.formulate",
            "render.request",
            "handoff.create",
        ],
    ),
    WorkerRole.VISUAL_DNA_SPECIALIST.value: RoleIdentity(
        role_id=WorkerRole.VISUAL_DNA_SPECIALIST.value,
        role_name="Visual DNA Specialist",
        description="Visual DNA extraction, token mapping, aesthetic consistency verification",
        default_capabilities=[
            "visual_dna.read",
            "visual_dna.extract",
            "token.map",
            "consistency.evaluate",
            "handoff.create",
        ],
    ),
    WorkerRole.CAMPAIGN_PLANNER.value: RoleIdentity(
        role_id=WorkerRole.CAMPAIGN_PLANNER.value,
        role_name="Campaign Planner",
        description="Milestone scheduling, asset dependency mapping, deliverable tracking",
        default_capabilities=[
            "campaign.read",
            "campaign.plan",
            "timeline.project",
            "dependency.evaluate",
            "handoff.create",
        ],
    ),
    WorkerRole.COPY_STRATEGIST.value: RoleIdentity(
        role_id=WorkerRole.COPY_STRATEGIST.value,
        role_name="Copy Strategist",
        description="Editorial copy, campaign taglines, storytelling, narrative framing",
        default_capabilities=[
            "copy.draft",
            "tagline.create",
            "narrative.frame",
            "brand.read",
            "handoff.create",
        ],
    ),
    WorkerRole.CONTENT_PRODUCER.value: RoleIdentity(
        role_id=WorkerRole.CONTENT_PRODUCER.value,
        role_name="Content Producer",
        description="Multi-channel asset assembly, deliverable packaging, format adaptation",
        default_capabilities=[
            "asset.package",
            "format.adapt",
            "deliverable.compile",
            "handoff.create",
        ],
    ),
    WorkerRole.TREND_RESEARCHER.value: RoleIdentity(
        role_id=WorkerRole.TREND_RESEARCHER.value,
        role_name="Trend Researcher",
        description="Cultural trend tracking, micro-trend synthesis, fashion cycle analysis",
        default_capabilities=[
            "trend.analyze",
            "trend.read",
            "market.survey",
            "handoff.create",
        ],
    ),
    WorkerRole.QUALITY_REVIEWER.value: RoleIdentity(
        role_id=WorkerRole.QUALITY_REVIEWER.value,
        role_name="Quality Reviewer",
        description="Aesthetic critique, brand compliance auditing, artifact quality scoring",
        default_capabilities=[
            "quality.evaluate",
            "brand.audit",
            "compliance.verify",
            "review.submit",
            "handoff.create",
        ],
    ),
    WorkerRole.PERFORMANCE_ANALYST.value: RoleIdentity(
        role_id=WorkerRole.PERFORMANCE_ANALYST.value,
        role_name="Performance Analyst",
        description="Campaign telemetry analysis, engagement metrics, audience resonance modeling",
        default_capabilities=[
            "telemetry.read",
            "performance.model",
            "resonance.evaluate",
            "handoff.create",
        ],
    ),
    WorkerRole.CLIENT_COORDINATOR.value: RoleIdentity(
        role_id=WorkerRole.CLIENT_COORDINATOR.value,
        role_name="Client Coordinator",
        description="Client brief synthesis, feedback intake, review staging",
        default_capabilities=[
            "brief.intake",
            "feedback.synthesize",
            "review.stage",
            "handoff.create",
        ],
    ),
    WorkerRole.STUDIO_OPERATOR.value: RoleIdentity(
        role_id=WorkerRole.STUDIO_OPERATOR.value,
        role_name="Studio Operator",
        description="Workforce routine scheduling, pipeline monitoring, operational triage",
        default_capabilities=[
            "routine.trigger",
            "pipeline.inspect",
            "triage.execute",
            "handoff.create",
        ],
    ),
}


def get_role_definition(role_name_or_id: str) -> RoleIdentity:
    """Retrieve canonical role definition or raise KeyError."""
    if role_name_or_id in CANONICAL_ROLES:
        return CANONICAL_ROLES[role_name_or_id]
    raise KeyError(f"Unknown role ID: {role_name_or_id}")

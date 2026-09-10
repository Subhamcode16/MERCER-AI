"""
Phase 14 Creative Workforce Orchestrator
----------------------------------------
Main orchestrator entry point for ILYREN Creative Workforce & Organizational Intelligence Boundary.
Integrates CreativeWorkforceDirector, DelegationEngine, ContextManager, CollaborationProtocol,
SelfCritiqueEngine, IndependentReviewer, RevisionLoopController, TrendIntelligenceEngine,
VisualDNAManager, CreativeDirectionSynthesizer, InstitutionalMemoryStore, GovernedImprovementEngine,
WorkforceEventStream, and WorkforceLedger.
Interfaces seamlessly with Phase 8–13 control substrate without mutating security policy or authority boundaries.
"""

from typing import Dict, Any, List, Optional
import uuid

from src.creative_workforce.organization_models import (
    Role,
    Department,
    StaffIdentity,
    ContextBinding,
    WorkforceAssignment,
    CritiqueResult,
    ReviewResult,
)
from src.creative_workforce.staff_registry import StaffRegistry
from src.creative_workforce.client_context import ClientContextManager
from src.creative_workforce.delegation import WorkforceDelegationEngine
from src.creative_workforce.creative_director import CreativeWorkforceDirector, WorkforcePlan
from src.creative_workforce.collaboration import CreativeCollaborationProtocol, CreativeArtifact
from src.creative_workforce.critique import SelfCritiqueEngine
from src.creative_workforce.independent_review import IndependentReviewer
from src.creative_workforce.revision import RevisionLoopController
from src.creative_workforce.trend_observation import TrendIntelligenceEngine, TrendObservation
from src.creative_workforce.visual_dna import VisualDNAManager, VisualDNAProfile
from src.creative_workforce.creative_direction import CreativeDirectionSynthesizer, CreativeDirectionBrief
from src.creative_workforce.workforce_memory import InstitutionalMemoryStore
from src.creative_workforce.improvement import GovernedImprovementEngine
from src.creative_workforce.workforce_events import WorkforceEventStream
from src.creative_workforce.workforce_ledger import WorkforceLedger

class CreativeWorkforceOrchestrator:
    """Central entry point orchestrating the ILYREN Creative Workforce."""

    def __init__(self):
        self.staff_registry = StaffRegistry()
        self.context_manager = ClientContextManager()
        self.delegation_engine = WorkforceDelegationEngine(self.staff_registry, self.context_manager)
        self.director = CreativeWorkforceDirector(self.delegation_engine)
        self.collaboration = CreativeCollaborationProtocol()
        self.critique_engine = SelfCritiqueEngine()
        self.reviewer = IndependentReviewer()
        self.revision_controller = RevisionLoopController(self.collaboration, self.critique_engine)
        self.trend_engine = TrendIntelligenceEngine()
        self.visual_dna_manager = VisualDNAManager()
        self.creative_synthesizer = CreativeDirectionSynthesizer()
        self.memory_store = InstitutionalMemoryStore()
        self.improvement_engine = GovernedImprovementEngine()
        self.event_stream = WorkforceEventStream()
        self.ledger = WorkforceLedger()

    def execute_campaign_proposal_workflow(
        self,
        client_id: str,
        brand_id: str,
        campaign_title: str,
        objective: str,
        primary_colors: Optional[List[str]] = None,
        typography_styles: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Executes a complete end-to-end organizational creative campaign proposal workflow."""
        # 1. Formulate Workforce Plan via CreativeWorkforceDirector
        plan = self.director.formulate_workforce_plan(
            client_id=client_id,
            brand_id=brand_id,
            campaign_title=campaign_title,
            objective=objective,
        )

        self.event_stream.emit_event("WORKFORCE_PLAN_CREATED", client_id, plan.plan_id, "director", {"objective": objective})
        self.ledger.record_entry("WORKFORCE_PLAN_CREATED", client_id, "director", {"plan_id": plan.plan_id})

        # 2. Extract Visual DNA & Ingest Trend Intelligence
        colors = primary_colors or ["#000000", "#FFFFFF", "#FF0000"]
        fonts = typography_styles or ["Helvetica Neue", "Inter"]
        vdna = self.visual_dna_manager.extract_visual_dna(brand_id, colors, fonts)

        obs = self.trend_engine.collect_observation("https://trends.fashion.wiki/september", "streetwear", "Monochrome kinetic typography trend")

        # 3. Synthesize Creative Direction Brief
        brief = self.creative_synthesizer.synthesize_direction(campaign_title, vdna, [obs])

        # 4. Production: Create Initial Draft Campaign Artifact
        first_asgn = plan.assignments[3]  # Visual Designer
        binding = first_asgn.context_binding

        art_payload = {
            "title": f"{campaign_title} Visual Assets",
            "text": f"NOCAP September Social Campaign Draft v1 - {brief.creative_pillars[0]}",
            "brief_id": brief.brief_id,
        }

        artifact = self.collaboration.create_artifact(
            title=f"{campaign_title} Draft",
            content_type="SOCIAL_CAMPAIGN_POST",
            payload=art_payload,
            context_binding=binding,
        )

        self.event_stream.emit_event("ARTIFACT_CREATED", client_id, campaign_title, binding.staff_id, {"artifact_id": artifact.artifact_id})

        # 5. Self-Critique
        critique = self.critique_engine.evaluate_artifact(artifact)
        self.event_stream.emit_event("CRITIQUE_COMPLETED", client_id, campaign_title, "critic", {"revision_required": critique.revision_required})

        # 6. Revision if needed (within bounded limit)
        final_artifact = artifact
        if critique.revision_required:
            revised_payload = dict(art_payload)
            revised_payload["text"] += " (Revised - Refined visual contrast)"
            final_artifact = self.revision_controller.revise_artifact(artifact, revised_payload)

        # 7. Independent Review (Double-Blind)
        review = self.reviewer.review_artifact(final_artifact)
        self.event_stream.emit_event("REVIEW_COMPLETED", client_id, campaign_title, self.reviewer.reviewer_id, {"recommendation": review.recommendation})

        # 8. Record in Institutional Memory
        mem_rec = self.memory_store.record_event(
            record_id=f"mem-{uuid.uuid4().hex[:8]}",
            event_type="CAMPAIGN_PROPOSAL_COMPLETED",
            context_binding=binding,
            summary=f"Campaign proposal {campaign_title} generated and reviewed.",
            details={"review_recommendation": review.recommendation, "artifact_id": final_artifact.artifact_id},
        )

        return {
            "plan_id": plan.plan_id,
            "brief": brief,
            "artifact": final_artifact,
            "critique": critique,
            "review": review,
            "memory_record": mem_rec,
            "ledger_verified": self.ledger.verify_ledger_integrity(),
        }

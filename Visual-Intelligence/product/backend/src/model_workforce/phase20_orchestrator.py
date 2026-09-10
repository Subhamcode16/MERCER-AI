"""
Phase 20 - Model Workforce Orchestrator Facade.

Central orchestrator coordinating Model Gateway, Visual Model Gateway, MCP Gateway,
Visual Knowledge Benchmark, and Workforce Bridge for Phase 20 operations.
"""

from typing import Dict, Any, Optional
from src.model_gateway.gateway import ModelGateway
from src.visual_model_gateway.gateway import VisualModelGateway
from src.mcp_gateway.gateway import MCPGateway
from src.visual_knowledge.benchmark_runner import VisualKnowledgeBenchmarkRunner
from .workforce_bridge import ModelBackedWorkforceBridge


class Phase20Orchestrator:
    """Primary facade for Phase 20 Model Integration and Visual Intelligence Benchmark."""

    def __init__(self):
        self.model_gateway = ModelGateway()
        self.visual_gateway = VisualModelGateway()
        self.mcp_gateway = MCPGateway()
        self.workforce_bridge = ModelBackedWorkforceBridge(
            self.model_gateway, self.visual_gateway, self.mcp_gateway
        )
        self.benchmark_runner = VisualKnowledgeBenchmarkRunner(self.visual_gateway)

    def run_benchmark_suite(self) -> Dict[str, Any]:
        """Execute the 250-case Visual Knowledge Benchmark Suite."""
        return self.benchmark_runner.run_benchmark()

    def run_nocap_production_cycle(self, campaign_brief: Dict[str, Any], client_id: str = "client_nocap") -> Dict[str, Any]:
        """Execute full model-backed NOCAP campaign production cycle."""
        
        # 1. TREND_ANALYST: Trend observation via MCP + LLM
        trend_res = self.workforce_bridge.trend_analyst_observe(
            query=campaign_brief.get("theme", "Luxury Cyberpunk"),
            client_id=client_id
        )

        # 2. STRATEGIST: Strategy synthesis via LLM
        strat_res = self.workforce_bridge.strategist_synthesize(campaign_brief, client_id)

        # 3. DESIGNER: Visual generation via Visual Model Gateway
        img_res = self.workforce_bridge.designer_generate(
            creative_direction={"prompt": "NOCAP Silk trench hero visual", "aspect_ratio": "9:16"},
            visual_dna={"palette": ["#000000", "#FF0055"]},
            client_id=client_id
        )

        # 4. CONTENT_SPECIALIST: Copy generation via LLM
        copy_res = self.workforce_bridge.content_specialist_write(
            brand_context={"brand_name": "NOCAP Apparel"},
            client_id=client_id
        )

        # 5. CRITIC: Self-critique via Vision Analysis
        critic_res = self.workforce_bridge.critic_evaluate(img_res.image_url_or_bytes, client_id)

        # 6. REVIEWER: Independent governance evaluation
        reviewer_res = self.workforce_bridge.reviewer_evaluate(
            candidate_artifact={"artifact_id": img_res.artifact_id, "copy": copy_res["copy"]},
            client_id=client_id
        )

        return {
            "client_id": client_id,
            "trend_observation": trend_res,
            "strategy": strat_res,
            "generated_visual_artifact": img_res.model_dump(),
            "generated_copy": copy_res,
            "self_critique": critic_res,
            "governance_review": reviewer_res,
            "status": "APPROVED_FOR_HUMAN_AUTHORIZATION"
        }

    def verify_all_ledgers(self) -> bool:
        """Verify integrity across Model, Visual, and MCP audit ledgers."""
        m_ok = self.model_gateway.ledger.verify_integrity()
        v_ok = self.visual_gateway.ledger.verify_integrity()
        mcp_ok = self.mcp_gateway.ledger.verify_integrity()
        return m_ok and v_ok and mcp_ok

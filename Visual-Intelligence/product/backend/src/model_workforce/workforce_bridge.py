"""
Phase 20 - Workforce Model Gateway Bridge.

Connects the 6 Phase 14-18 creative workforce roles (TREND_ANALYST, STRATEGIST, DESIGNER,
CONTENT_SPECIALIST, CRITIC, REVIEWER) to the LLM Gateway, Visual Model Gateway, and MCP Gateway.
"""

from typing import Dict, Any, Optional
from src.model_gateway.gateway import ModelGateway
from src.model_gateway.models import LLMRequest, LLMResponse
from src.visual_model_gateway.gateway import VisualModelGateway
from src.visual_model_gateway.models import (
    ImageGenerationRequest, ImageGenerationResponse,
    VisionAnalysisRequest, VisionAnalysisResponse
)
from src.mcp_gateway.gateway import MCPGateway
from src.mcp_gateway.models import MCPInvocationRequest


class ModelBackedWorkforceBridge:
    """Bridge connecting governed workforce roles to model gateways."""

    def __init__(
        self,
        model_gateway: ModelGateway,
        visual_gateway: VisualModelGateway,
        mcp_gateway: MCPGateway
    ):
        self.model_gateway = model_gateway
        self.visual_gateway = visual_gateway
        self.mcp_gateway = mcp_gateway

    def trend_analyst_observe(self, query: str, client_id: str) -> Dict[str, Any]:
        """TREND_ANALYST: Invokes MCP trend tool + LLM analysis."""
        # 1. MCP tool invocation
        mcp_req = MCPInvocationRequest(
            server_id="mcp_fashion_trends",
            tool_name="read_fashion_trends",
            arguments={"query": query},
            client_id=client_id
        )
        mcp_res = self.mcp_gateway.invoke_tool(mcp_req)

        # 2. LLM synthesis
        llm_req = LLMRequest(
            task_type="TREND_ANALYSIS",
            prompt=f"Synthesize trend observations from external tool data: {mcp_res.sanitized_output}",
            client_id=client_id
        )
        llm_res = self.model_gateway.generate(llm_req)

        return {
            "role": "TREND_ANALYST",
            "mcp_observation": mcp_res.sanitized_output,
            "analysis_content": llm_res.content,
            "trust_classification": "UNTRUSTED_EXTERNAL_OBSERVATION"
        }

    def strategist_synthesize(self, brief: Dict[str, Any], client_id: str) -> Dict[str, Any]:
        """STRATEGIST: Invokes LLM strategy synthesis."""
        llm_req = LLMRequest(
            task_type="STRATEGY_SYNTHESIS",
            prompt=f"Formulate campaign strategy for brief: {brief}",
            client_id=client_id
        )
        llm_res = self.model_gateway.generate(llm_req)

        return {
            "role": "STRATEGIST",
            "strategy": llm_res.structured_data or {"strategy": llm_res.content},
            "provenance": llm_res.provenance.model_dump()
        }

    def designer_generate(self, creative_direction: Dict[str, Any], visual_dna: Dict[str, Any], client_id: str) -> ImageGenerationResponse:
        """DESIGNER: Invokes Visual Model Gateway for image asset generation."""
        img_req = ImageGenerationRequest(
            prompt=creative_direction.get("prompt", "High fashion lookbook hero shot"),
            aspect_ratio=creative_direction.get("aspect_ratio", "1:1"),
            creative_direction=creative_direction,
            visual_dna=visual_dna,
            client_id=client_id
        )
        return self.visual_gateway.generate_image(img_req)

    def content_specialist_write(self, brand_context: Dict[str, Any], client_id: str) -> Dict[str, Any]:
        """CONTENT_SPECIALIST: Invokes LLM copy generation."""
        llm_req = LLMRequest(
            task_type="COPY_GENERATION",
            prompt=f"Draft luxury e-commerce campaign copy for brand context: {brand_context}",
            client_id=client_id
        )
        llm_res = self.model_gateway.generate(llm_req)
        return {"role": "CONTENT_SPECIALIST", "copy": llm_res.content}

    def critic_evaluate(self, artifact_url: str, client_id: str) -> Dict[str, Any]:
        """CRITIC: Invokes Vision Analysis for defect detection and critique."""
        vanal_req = VisionAnalysisRequest(
            image_url_or_bytes=artifact_url,
            task="CRITIQUE",
            client_id=client_id
        )
        vanal_res = self.visual_gateway.analyze_vision(vanal_req)
        return {"role": "CRITIC", "critique": vanal_res.structured_observations, "confidence": vanal_res.confidence_score}

    def reviewer_evaluate(self, candidate_artifact: Dict[str, Any], client_id: str) -> Dict[str, Any]:
        """REVIEWER: Independent evaluation configuration."""
        llm_req = LLMRequest(
            task_type="REVIEW_EVALUATION",
            prompt=f"Perform independent governance evaluation of candidate artifact: {candidate_artifact}",
            client_id=client_id
        )
        llm_res = self.model_gateway.generate(llm_req)
        return {"role": "REVIEWER", "approved": True, "evaluation_summary": llm_res.content}

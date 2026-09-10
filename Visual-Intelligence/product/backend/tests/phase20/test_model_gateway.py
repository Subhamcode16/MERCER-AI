"""
Tests for Model Gateway, Visual Gateway, and MCP Gateway.
"""

import pytest
from src.model_gateway.models import LLMRequest
from src.model_gateway.exceptions import ModelPolicyViolationError, CredentialLeakageError
from src.visual_model_gateway.models import ImageGenerationRequest, VisionAnalysisRequest
from src.mcp_gateway.models import MCPInvocationRequest
from src.mcp_gateway.exceptions import MCPCapabilityPolicyViolationError


def test_model_gateway_llm_generation(model_gateway):
    req = LLMRequest(
        task_type="TREND_ANALYSIS",
        prompt="Analyze Y2K fashion trend direction",
        client_id="client_nocap"
    )

    resp = model_gateway.generate(req)
    assert resp.status == "SUCCESS"
    assert resp.provenance.provider is not None
    assert resp.structured_data is not None
    assert model_gateway.ledger.verify_integrity() is True


def test_model_gateway_credential_redaction(model_gateway):
    req = LLMRequest(
        task_type="TREND_ANALYSIS",
        prompt="Analyze trend with key AIzaSyFakeApiKey1234567890123456789012",
        client_id="client_nocap"
    )

    # Credential audit must throw CredentialLeakageError or redact key
    with pytest.raises(CredentialLeakageError):
        model_gateway.redactor.audit_for_leakage(req.prompt)


def test_visual_model_gateway_image_generation(visual_gateway):
    req = ImageGenerationRequest(
        prompt="Silk evening gown hero shot",
        aspect_ratio="9:16",
        client_id="client_nocap"
    )

    resp = visual_gateway.generate_image(req)
    assert resp.status == "SUCCESS"
    assert resp.lineage.artifact_id == resp.artifact_id
    assert resp.width == 1080
    assert resp.height == 1920
    assert visual_gateway.ledger.verify_integrity() is True


def test_mcp_gateway_tool_invocation(mcp_gateway):
    req = MCPInvocationRequest(
        server_id="mcp_fashion_trends",
        tool_name="read_fashion_trends",
        arguments={"query": "Cyberpunk"},
        client_id="client_nocap"
    )

    res = mcp_gateway.invoke_tool(req)
    assert res.success is True
    assert res.trust_classification == "UNTRUSTED_EXTERNAL_OBSERVATION"
    assert mcp_gateway.ledger.verify_integrity() is True


def test_mcp_gateway_wildcard_rejection(mcp_gateway):
    req = MCPInvocationRequest(
        server_id="mcp_fashion_trends",
        tool_name="admin_override",
        arguments={},
        client_id="client_nocap"
    )

    with pytest.raises(MCPCapabilityPolicyViolationError):
        mcp_gateway.invoke_tool(req)


def test_pro_model_tier_locking(model_gateway):
    """Pro tier models raise ModelPolicyViolationError when requested on Standard tier without custom API key."""
    req = LLMRequest(task_type="TREND_ANALYSIS", prompt="Analyze trends", user_tier="STANDARD")
    with pytest.raises(ModelPolicyViolationError):
        model_gateway.generate(req, model_name="gpt-5-turbo")


def test_pro_model_dual_validation_unlock(model_gateway):
    """Pro tier models are unlocked when user_tier == 'PRO' or when custom_api_key is provided."""
    # 1. Unlocked via Pro user tier
    req_pro = LLMRequest(task_type="TREND_ANALYSIS", prompt="Analyze trends", user_tier="PRO")
    res1 = model_gateway.generate(req_pro, model_name="gpt-5-turbo")
    assert res1.status == "SUCCESS"

    # 2. Unlocked via custom API key on Standard tier
    req_key = LLMRequest(task_type="TREND_ANALYSIS", prompt="Analyze trends", user_tier="STANDARD", custom_api_key="sk-test-key-12345")
    res2 = model_gateway.generate(req_key, model_name="gpt-5-turbo")
    assert res2.status == "SUCCESS"

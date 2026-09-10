"""
Pytest configuration and shared fixtures for Phase 20 test suite.
"""

import pytest
from src.model_gateway.gateway import ModelGateway
from src.visual_model_gateway.gateway import VisualModelGateway
from src.mcp_gateway.gateway import MCPGateway
from src.model_workforce.phase20_orchestrator import Phase20Orchestrator


@pytest.fixture
def model_gateway():
    return ModelGateway()


@pytest.fixture
def visual_gateway():
    return VisualModelGateway()


@pytest.fixture
def mcp_gateway():
    return MCPGateway()


@pytest.fixture
def orchestrator():
    return Phase20Orchestrator()

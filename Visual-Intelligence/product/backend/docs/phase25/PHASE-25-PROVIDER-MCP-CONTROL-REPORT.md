# Phase 25: Provider & MCP Control Subsystem Report

## 1. Overview
The Provider & MCP Control Subsystem (`src/provider_control/`) manages external model providers, visual rendering engines, MCP server tool invocations, credential scoping, and circuit breakers.

## 2. Invariant & Security Safeguards
1. **Masked Credential Invariant**: External API keys are NEVER returned in plaintext. They are rendered as `sk-ant-***-XYZ` or `[CONFIGURED_IN_ENV]`.
2. **MCP Tool Capability Scoping**: Wildcard tool permissions (`*`) are prohibited. All MCP tool bindings must specify explicit tool names (e.g., `['render_image', 'query_style_tokens']`).
3. **Circuit Breakers**: Tripped circuit breakers (`OPEN` state) can only be reset by operators possessing the `RESET_CIRCUIT_BREAKER` capability via authenticated control plane action.

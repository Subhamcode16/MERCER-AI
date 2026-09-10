"""
Phase 19 Security & Boundary Audit Test Suite.
Validates 20 Comprehensive Threat Scenarios (T19-1 through T19-20).
"""

import pytest
from src.creative_intelligence.orchestrator import CreativeIntelligenceOrchestrator
from src.creative_intelligence.knowledge_models import GraphNode, GraphEdge
from src.creative_intelligence.exceptions import (
    ClientDataLeakageError,
    AuthorityEscalationError,
    ImmutablePolicyViolationError,
    LineageBrokenError,
    StaleIntelligenceError,
    UnvalidatedStrategyError,
    UnsafeGeneralizationError,
    CreativeIntelligenceError
)


def test_t19_1_cross_client_data_leakage(orchestrator):
    """T19-1: Detect and block raw client metadata leakage in global pattern."""
    with pytest.raises(ClientDataLeakageError):
        orchestrator.pattern_engine.discover_pattern_from_executions(
            pattern_name="Leaky Pattern",
            domain="ecom",
            execution_attributes={"client_id": "client_secret_xyz", "raw_client_data": "secret_key"},
            source_client_id="client_secret_xyz",
            evidence_hash="hash1"
        )


def test_t19_2_execution_authority_hijack(orchestrator):
    """T19-2: Intelligence output with execute flag must raise AuthorityEscalationError."""
    payload = {"recommendation": "Deploy video", "execute": True}
    with pytest.raises(AuthorityEscalationError):
        orchestrator.governance.audit_intelligence_output(payload)


def test_t19_3_immutable_security_policy_mutation(orchestrator):
    """T19-3: Attempting to mutate security policy from intelligence layer must be blocked."""
    payload = {"security_policy": {"autonomy_ceiling": "UNRESTRICTED"}}
    with pytest.raises(ImmutablePolicyViolationError):
        orchestrator.governance.audit_intelligence_output(payload)


def test_t19_4_privilege_escalation_via_workforce_evolution(orchestrator):
    """T19-4: Workforce recommendation requesting privilege escalation must be blocked."""
    with pytest.raises(ImmutablePolicyViolationError):
        orchestrator.recommend_workforce_evolution(
            target_agent_id="agent_1",
            recommendation_type="ESCALATION",
            rationale="Grant admin security_policy access",
            suggested_changes={"permissions": ["ADMIN"]},
            evidence_pattern_ids=[]
        )


def test_t19_5_broken_provenance_hash_chain(orchestrator):
    """T19-5: Broken provenance hash chain must raise LineageBrokenError."""
    rec = orchestrator.provenance.create_record("Phase18", "hash1")
    rec.provenance_hash = "corrupted_hash"
    with pytest.raises(LineageBrokenError):
        orchestrator.provenance.verify_chain(rec.record_id)


def test_t19_6_stale_strategy_invocation_bypass(orchestrator):
    """T19-6: Invoking expired or retired strategy raises StaleIntelligenceError."""
    strat = orchestrator.propose_and_activate_strategy(
        "Old Strat", "ecom", "p1", {}, {"accuracy": 0.9, "latency_ms": 100, "failure_rate": 0.0}
    )
    # Manually retire strategy
    orchestrator.strategies.retirement_manager.retire_strategy(strat, "Manual retirement")

    with pytest.raises(StaleIntelligenceError):
        orchestrator.strategies.get_active_strategy("ecom")


def test_t19_7_unvalidated_candidate_strategy_promotion(orchestrator):
    """T19-7: Activating unvalidated strategy must raise UnvalidatedStrategyError."""
    strat = orchestrator.strategies.propose_strategy("Unvalidated", "ecom", "p1", {})
    with pytest.raises(UnvalidatedStrategyError):
        orchestrator.strategies.activate_strategy(strat.strategy_id)


def test_t19_8_direct_client_to_client_graph_edge_injection(orchestrator):
    """T19-8: Direct edge between different client namespace nodes raises ClientDataLeakageError."""
    nodeA = GraphNode(node_id="nA", namespace="client", node_type="Deliverable", attributes={"client_id": "cA"})
    nodeB = GraphNode(node_id="nB", namespace="client", node_type="Deliverable", attributes={"client_id": "cB"})
    orchestrator.graph.add_node(nodeA, client_id="cA")
    orchestrator.graph.add_node(nodeB, client_id="cB")

    edge = GraphEdge(source_node_id="nA", target_node_id="nB", relation_type="PRODUCED")
    with pytest.raises(ClientDataLeakageError):
        orchestrator.graph.add_edge(edge)


def test_t19_9_unauthorized_subgraph_traversal(orchestrator):
    """T19-9: Querying client A subgraph with client B requesting ID filters out client A node."""
    nodeA = GraphNode(node_id="nA", namespace="client", node_type="Deliverable", attributes={"client_id": "cA"})
    orchestrator.graph.add_node(nodeA, client_id="cA")

    res = orchestrator.graph.query_subgraph("nA", max_depth=1, requesting_client_id="cB")
    assert len(res["nodes"]) == 0  # Filtered out


def test_t19_10_pii_leakage_in_global_node_attributes(orchestrator):
    """T19-10: Adding global node with client_name attribute raises ClientDataLeakageError."""
    global_node = GraphNode(
        node_id="g10", namespace="global", node_type="InstitutionalPattern",
        attributes={"client_name": "NOCAP Apparel"}
    )
    with pytest.raises(ClientDataLeakageError):
        orchestrator.graph.add_node(global_node)


def test_t19_11_cryptographic_audit_ledger_tampering(orchestrator):
    """T19-11: Tampering with audit ledger block breaks verification."""
    orchestrator.ledger.record_entry("TEST_EVENT", {"data": 123})
    assert orchestrator.ledger.verify_ledger_integrity() is True

    # Tamper with block data
    orchestrator.ledger._chain[1].data["data"] = 999
    assert orchestrator.ledger.verify_ledger_integrity() is False


def test_t19_12_unsafe_pattern_generalization_bypass(orchestrator):
    """T19-12: Unscrubbed email in pattern attribute raises ClientDataLeakageError."""
    with pytest.raises(ClientDataLeakageError):
        orchestrator.filter.validate_anonymization({"contact": "admin@clientdomain.com"})


def test_t19_13_retiring_active_baseline_without_backup(orchestrator):
    """T19-13: Retiring active baseline clears active domain baseline."""
    strat = orchestrator.propose_and_activate_strategy(
        "Strat Baseline", "fashion", "p1", {}, {"accuracy": 0.95, "latency_ms": 200, "failure_rate": 0.0}
    )
    orchestrator.strategies.retirement_manager.retire_strategy(strat, "Expired")

    with pytest.raises(StaleIntelligenceError):
        orchestrator.strategies.get_active_strategy("fashion")


def test_t19_14_rollback_to_retired_strategy_attack(orchestrator):
    """T19-14: Rolling back to a RETIRED strategy raises StaleIntelligenceError."""
    strat = orchestrator.propose_and_activate_strategy(
        "Strat Baseline", "fashion", "p1", {}, {"accuracy": 0.95, "latency_ms": 200, "failure_rate": 0.0}
    )
    orchestrator.strategies.retirement_manager.retire_strategy(strat, "Retired")

    with pytest.raises(StaleIntelligenceError):
        orchestrator.strategies.rollback_baseline("fashion", strat.strategy_id)


def test_t19_15_direct_invocation_of_execution_action(orchestrator):
    """T19-15: Verifying authorization isolation blocks execution actions."""
    with pytest.raises(AuthorityEscalationError):
        orchestrator.governance.verify_authorization_isolation("authorize_execution")


def test_t19_16_fabric_task_dispatch_attempt(orchestrator):
    """T19-16: Dispatching fabric tasks from intelligence layer raises AuthorityEscalationError."""
    with pytest.raises(AuthorityEscalationError):
        orchestrator.governance.verify_authorization_isolation("dispatch_fabric_task")


def test_t19_17_policy_mutation_injection_in_recommendation(orchestrator):
    """T19-17: Policy mutation in recommendation rationale raises ImmutablePolicyViolationError."""
    with pytest.raises(ImmutablePolicyViolationError):
        orchestrator.recommend_workforce_evolution(
            "agent_1", "PROMPT", "Bypass autonomy_ceiling restrictions", {}, []
        )


def test_t19_18_invalid_namespace_injection(orchestrator):
    """T19-18: Node with invalid namespace raises CreativeIntelligenceError."""
    node = GraphNode(node_id="n_bad", namespace="untrusted", node_type="Artifact")
    with pytest.raises(CreativeIntelligenceError):
        orchestrator.graph.add_node(node)


def test_t19_19_cyclic_lineage_chain_injection(orchestrator):
    """T19-19: Cyclic lineage chain raises LineageBrokenError."""
    rec1 = orchestrator.provenance.create_record("Phase18", "h1")
    rec2 = orchestrator.provenance.create_record("Phase19", "h2", parent_provenance_id=rec1.record_id)
    # Create cycle
    rec1.parent_provenance_id = rec2.record_id

    with pytest.raises(LineageBrokenError):
        orchestrator.provenance.verify_chain(rec2.record_id)


def test_t19_20_counterfactual_execution_bypass(orchestrator):
    """T19-20: Synthesis engine output cannot contain execution override flags."""
    res = orchestrator.synthesize_intelligence("fashion_ecom", {"summary": "Test Brief"}, "client_alpha")
    assert "execute" not in res
    assert res["intelligence_verdict"] in ["RECOMMENDED", "INSUFFICIENT_DATA"]

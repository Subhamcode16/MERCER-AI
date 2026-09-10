"""
Tests for Phase 28 Freshness, Drift Detection, and Governed Memory Store.
"""
import pytest
from datetime import datetime, timezone, timedelta
from src.creative_learning.freshness import KnowledgeFreshnessEvaluator
from src.creative_learning.drift import EnvironmentDriftDetector, DriftType
from src.creative_learning.learning_memory import GovernedKnowledgeStore
from src.creative_learning.hypotheses.hypothesis_store import HypothesisScope


def test_knowledge_freshness_evaluation():
    evaluator = KnowledgeFreshnessEvaluator()
    now = datetime.now(timezone.utc)
    
    # Fresh knowledge (20 days old)
    eval_fresh = evaluator.evaluate_freshness("kno_01", now - timedelta(days=20), expiry_limit_days=90)
    assert eval_fresh.is_fresh is True
    assert eval_fresh.recommendation == "VALID"

    # Expired knowledge (130 days old)
    eval_expired = evaluator.evaluate_freshness("kno_02", now - timedelta(days=130), expiry_limit_days=90)
    assert eval_expired.is_fresh is False
    assert eval_expired.recommendation == "EXPIRED"


def test_drift_detection():
    detector = EnvironmentDriftDetector()
    alert = detector.check_and_record_drift(
        drift_type=DriftType.MODEL_VERSION_DRIFT,
        affected_component="Visual Rendering Engine",
        old_state="Imagen-2-Studio",
        new_state="Imagen-3-Photoreal",
    )
    assert alert is not None
    assert "Performance shifts cannot be purely attributed to creative changes" in alert.confounder_warning


def test_governed_knowledge_store_multi_tenant_isolation():
    store = GovernedKnowledgeStore()
    
    # Store brand knowledge
    obj = store.store_knowledge(
        tenant_id="tenant_lux",
        scope=HypothesisScope.BRAND,
        title="Tactile Monolithic Preset",
        content="Raking sun highlights wool weave texture.",
        provenance_proposal_id="prop_01",
        client_id="cli_01",
        brand_id="brd_01",
    )
    assert obj.is_active is True

    # Multi-tenant query
    res_lux = store.list_knowledge(tenant_id="tenant_lux", brand_id="brd_01")
    assert len(res_lux) == 1

    res_other = store.list_knowledge(tenant_id="tenant_other", brand_id="brd_other")
    assert len(res_other) == 0

    # Cross-client global violation guard
    with pytest.raises(PermissionError):
        store.store_knowledge(
            tenant_id="tenant_lux",
            scope=HypothesisScope.GLOBAL,
            title="Leaked Brand Guideline",
            content="Private client formula",
            provenance_proposal_id="prop_leak",
            client_id="cli_private",
        )

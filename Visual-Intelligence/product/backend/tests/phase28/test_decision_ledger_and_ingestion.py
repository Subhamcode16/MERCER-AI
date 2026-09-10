"""
Tests for Phase 28 Decision Ledger and Outcome Ingestion.
"""
import pytest
from src.creative_learning.decision_ledger import (
    DecisionLedger,
    DecisionType,
    DecisionContextSnapshot,
    DecisionAlternative,
)
from src.creative_learning.outcome_ingestion import OutcomeIngestionPipeline


def test_decision_ledger_append_and_cryptographic_integrity():
    ledger = DecisionLedger()
    campaign_id = "camp_test_01"

    snapshot = DecisionContextSnapshot(
        snapshot_id="snp_01",
        tenant_id="tenant_lux",
        client_id="cli_01",
        brand_id="brd_01",
        campaign_id=campaign_id,
    )

    alt1 = DecisionAlternative("alt_01", "Vibrant Cyber Neon", "Dilutes heritage quiet luxury", 0.7)
    rec1 = ledger.record_decision(
        campaign_id=campaign_id,
        decision_type=DecisionType.VISUAL_DIRECTION,
        actor_id="op_cd_01",
        context_snapshot=snapshot,
        decision="Selected Monolithic Architectural Elegance",
        rationale="Maximizes brand silhouette prestige",
        confidence=0.94,
        alternatives=[alt1],
    )
    assert rec1.decision_version == 1
    assert rec1.parent_hash is None
    assert len(rec1.record_hash) == 64

    rec2 = ledger.record_decision(
        campaign_id=campaign_id,
        decision_type=DecisionType.TOKEN_LOCK,
        actor_id="op_cd_01",
        context_snapshot=snapshot,
        decision="Locked raking_monolithic_late_sun token",
        rationale="Enhances tactile wool fabric definition",
        confidence=0.91,
    )
    assert rec2.decision_version == 2
    assert rec2.parent_hash == rec1.record_hash

    # Integrity verification
    assert ledger.verify_ledger_integrity(campaign_id) is True

    # Tampering check
    rec1.decision = "TAMPERED_DECISION"
    assert ledger.verify_ledger_integrity(campaign_id) is False


def test_outcome_ingestion_signature_validation():
    pipeline = OutcomeIngestionPipeline()
    campaign_id = "camp_test_01"

    feed_valid = pipeline.ingest_feed(
        campaign_id=campaign_id,
        source_platform="MetaAds",
        metrics_payload={"impressions": 150000, "clicks": 4500, "conversions": 310},
        source_signature="sig_rsa_verified_9934",
    )
    assert feed_valid.is_verified is True

    feed_injected = pipeline.ingest_feed(
        campaign_id=campaign_id,
        source_platform="FakePlatform",
        metrics_payload={"impressions": 9999999},
        source_signature="MOCK_INJECTION_ATTACK",
    )
    assert feed_injected.is_verified is False

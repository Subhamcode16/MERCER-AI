"""
Phase 9 — Artifact Lineage Tracker Unit Tests
"""

import json
import os
import shutil
import tempfile
import pytest

from src.agentic_work.artifact_lineage import ArtifactLineageTracker, LineageTamperError
from src.agentic_work.memory_models import ArtifactLineageRecord


@pytest.fixture
def temp_lineage_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_lineage_save_and_retrieve(temp_lineage_dir):
    tracker = ArtifactLineageTracker(base_dir=temp_lineage_dir)

    record = ArtifactLineageRecord(
        artifact_id="art_lookbook_final",
        workflow_id="wf_lookbook_100",
        task_id="t7_review",
        task_graph_version="v1.0",
        staff_contributions=["RESEARCHER", "STRATEGIST", "DESIGNER", "REVIEWER"],
        knowledge_observation_ids=["obs_trend_01"],
        critique_scores={"visual_consistency": 0.95},
        review_scores={"market_readiness": 0.98},
        revision_count=1,
        active_strategy_version="strat_v1_default",
        payload_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )

    tracker.record_lineage(record)

    loaded = tracker.get_lineage("art_lookbook_final")
    assert loaded.workflow_id == "wf_lookbook_100"
    assert loaded.staff_contributions == ["RESEARCHER", "STRATEGIST", "DESIGNER", "REVIEWER"]
    assert loaded.compute_hash() == record.compute_hash()


def test_lineage_tamper_detection(temp_lineage_dir):
    tracker = ArtifactLineageTracker(base_dir=temp_lineage_dir)

    record = ArtifactLineageRecord(
        artifact_id="art_tampered",
        workflow_id="wf_tampered",
        task_id="t4_design",
        task_graph_version="v1.0",
        staff_contributions=["DESIGNER"],
        knowledge_observation_ids=[],
        critique_scores={"score": 0.8},
        review_scores={"score": 0.8},
        revision_count=0,
        active_strategy_version="strat_v1_default",
        payload_hash="1234567890abcdef",
    )

    tracker.record_lineage(record)

    # Tamper with file contents manually
    file_path = os.path.join(temp_lineage_dir, "lineage_art_tampered.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Forged lineage hash
    data["lineage_hash"] = "badhash000000000000000000000000000000000000000000000000000000000"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    with pytest.raises(LineageTamperError):
        tracker.get_lineage("art_tampered")

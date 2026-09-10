"""
Phase 9 — Workflow Memory Store Unit Tests
"""

import os
import shutil
import tempfile
import pytest

from src.agentic_work.memory_models import WorkflowMemoryRecord
from src.agentic_work.memory_store import (
    WorkflowMemoryStore,
    SecretStorageForbiddenError,
    MemoryIntegrityError,
)


@pytest.fixture
def temp_memory_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_memory_store_save_and_load(temp_memory_dir):
    store = WorkflowMemoryStore(base_dir=temp_memory_dir)

    record = WorkflowMemoryRecord(
        memory_id="mem_001",
        workflow_id="wf_100",
        task_type="LOOKBOOK_CAMPAIGN",
        staff_participation=["RESEARCHER", "STRATEGIST", "DESIGNER"],
        task_graph_version="v1.0",
        input_metadata={"brand_name": "AURA"},
        output_artifact_ids=["art_01", "art_02"],
        critique_scores={"visual": 0.9},
        review_scores={"overall": 0.95},
        feedback_ids=["fb_01"],
        failure_signals=[],
        revision_count=1,
        active_strategy_version="strat_v1_default",
        benchmark_scores={"score": 85.0},
    )

    path = store.save_record(record)
    assert os.path.exists(path)

    loaded = store.load_record("mem_001")
    assert loaded.workflow_id == "wf_100"
    assert loaded.active_strategy_version == "strat_v1_default"
    assert loaded.compute_hash() == record.compute_hash()


def test_memory_store_rejects_secrets(temp_memory_dir):
    store = WorkflowMemoryStore(base_dir=temp_memory_dir)

    record = WorkflowMemoryRecord(
        memory_id="mem_secret",
        workflow_id="wf_secret",
        task_type="CAMPAIGN",
        staff_participation=[],
        task_graph_version="v1.0",
        input_metadata={"api_key": "sk-proj-secret12345"},  # Forbidden key!
        output_artifact_ids=[],
        critique_scores={},
        review_scores={},
        feedback_ids=[],
        failure_signals=[],
        revision_count=0,
        active_strategy_version="strat_v1_default",
        benchmark_scores={},
    )

    with pytest.raises(SecretStorageForbiddenError):
        store.save_record(record)


def test_memory_store_tamper_detection(temp_memory_dir):
    store = WorkflowMemoryStore(base_dir=temp_memory_dir)

    record = WorkflowMemoryRecord(
        memory_id="mem_tamper",
        workflow_id="wf_tamper",
        task_type="CAMPAIGN",
        staff_participation=["DESIGNER"],
        task_graph_version="v1.0",
        input_metadata={"brand": "NOVA"},
        output_artifact_ids=["art_01"],
        critique_scores={"score": 0.8},
        review_scores={"score": 0.8},
        feedback_ids=[],
        failure_signals=[],
        revision_count=0,
        active_strategy_version="strat_v1_default",
        benchmark_scores={},
    )

    store.save_record(record)

    # Manually tamper with record_hash in file
    file_path = os.path.join(temp_memory_dir, "mem_tamper.json")
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["record_hash"] = "0000000000000000000000000000000000000000000000000000000000000000"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    with pytest.raises(MemoryIntegrityError):
        store.load_record("mem_tamper")

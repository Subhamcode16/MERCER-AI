"""
Phase 14 Test Artifact Service
------------------------------
Tests artifact lineage, hash commitments, and cross-mission leakage protection.
"""

import pytest
from src.workflow_gateway.artifact_service import ArtifactService
from src.workflow_gateway.exceptions import (
    ArtifactLineageError,
    CrossMissionLeakageError,
)

def test_artifact_registration_and_integrity():
    service = ArtifactService()
    art = service.register_artifact(
        artifact_id="art-101",
        workflow_id="wf-art-1",
        mission_id="m-art-1",
        task_id="t-1",
        artifact_type="CAMPAIGN_DRAFT",
        content_summary="Spring Collection Post Draft",
        lineage_hash="hash-lineage-1",
    )
    assert art.artifact_id == "art-101"
    assert service.verify_artifact_lineage("art-101") is True

    # Retrieve matching mission
    assert service.get_artifact("art-101", expected_mission_id="m-art-1") is not None

    # Retrieve wrong mission (cross-mission leakage rejection)
    with pytest.raises(CrossMissionLeakageError):
        service.get_artifact("art-101", expected_mission_id="m-wrong-mission")

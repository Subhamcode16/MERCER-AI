"""
Unit tests for Phase 15 Deliverables Manager.
"""

import pytest
from src.studio_operations.deliverables import DeliverableManager
from src.studio_operations.studio_models import DeliverableStatus
from src.studio_operations.exceptions import DeliverableStateViolation, ClientContextViolation

def test_deliverable_lifecycle_manager():
    mgr = DeliverableManager()
    d = mgr.create_deliverable(
        requesting_client_id="client_nocap",
        deliverable_id="del_001",
        workstream_id="ws_001",
        campaign_id="camp_001",
        client_id="client_nocap",
        title="September Hero Post"
    )
    assert d.status == DeliverableStatus.PLANNED

    d = mgr.transition_deliverable("client_nocap", "del_001", DeliverableStatus.IN_PROGRESS)
    assert d.status == DeliverableStatus.IN_PROGRESS

    d = mgr.transition_deliverable("client_nocap", "del_001", DeliverableStatus.DRAFT, content_update={"caption": "NOCAP Drop"})
    assert d.content["caption"] == "NOCAP Drop"

    d = mgr.transition_deliverable("client_nocap", "del_001", DeliverableStatus.CRITIQUE)
    d = mgr.transition_deliverable("client_nocap", "del_001", DeliverableStatus.REVISION)
    assert d.revision_count == 1
    assert d.version == "1.1.0"

    with pytest.raises(ClientContextViolation):
        mgr.get_deliverable("client_other", "del_001")

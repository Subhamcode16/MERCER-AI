"""
Phase 14 Test Revision Loop
---------------------------
Tests RevisionLoopController MAX_REVISIONS = 3 ceiling enforcement (INV-14-W004).
"""

import pytest
from src.creative_workforce import (
    RevisionLoopController,
    CreativeCollaborationProtocol,
    ContextBinding,
    RevisionLimitExceededError,
)

def test_revision_ceiling_enforcement():
    controller = RevisionLoopController(max_revisions=3)
    protocol = CreativeCollaborationProtocol()
    binding = ContextBinding("nocap", "brand", "cmp-1", "m-1", "t-1", "designer-01")

    art_v1 = protocol.create_artifact("Banner", "IMAGE", {"version": 1}, binding)

    art_v2 = controller.revise_artifact(art_v1, {"version": 2})
    art_v3 = controller.revise_artifact(art_v2, {"version": 3})
    art_v4 = controller.revise_artifact(art_v3, {"version": 4})

    with pytest.raises(RevisionLimitExceededError, match="reached maximum permitted revisions"):
        controller.revise_artifact(art_v4, {"version": 5})

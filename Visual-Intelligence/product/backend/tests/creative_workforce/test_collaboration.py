"""
Phase 14 Test Creative Collaboration
------------------------------------
Tests CreativeCollaborationProtocol artifact creation and SHA-256 commitment hash verification.
"""

import pytest
from src.creative_workforce import CreativeCollaborationProtocol, ContextBinding

def test_artifact_creation_and_lineage_verification():
    protocol = CreativeCollaborationProtocol()
    binding = ContextBinding("nocap", "brand", "cmp-1", "m-1", "t-1", "designer-01")

    art = protocol.create_artifact(
        title="Draft Banner",
        content_type="IMAGE",
        payload={"url": "https://assets.nocap.wiki/draft1.png"},
        context_binding=binding,
    )
    assert art.artifact_id.startswith("art-")
    assert protocol.verify_artifact_lineage(art.artifact_id) is True

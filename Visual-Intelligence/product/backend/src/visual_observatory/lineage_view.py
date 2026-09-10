"""
Phase 25 Visual Artifact Cryptographic Lineage Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class VisualArtifactLineageDAG:
    artifact_id: str
    parent_artifact_id: Optional[str]
    client_id: str
    commitment_hash: str
    is_lineage_intact: bool
    generation_prompt_hash: str
    generation_parameters: Dict[str, Any]

"""
Phase 27 Cryptographic Multi-Tier Asset Lineage Graph.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import hashlib
import json
from datetime import datetime, timezone


@dataclass
class LineageNode:
    node_id: str
    node_type: str  # "CAMPAIGN", "MISSION", "DIRECTION", "VISUAL_DNA", "PROMPT", "MODEL", "RENDER", "APPROVAL", "DELIVERY"
    parent_id: Optional[str]
    metadata: Dict[str, Any]
    parent_hash: Optional[str]
    node_hash: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AssetLineageGraph:
    """Maintains a cryptographic chain-of-custody graph for all creative assets produced in the studio."""

    def __init__(self):
        self._nodes: Dict[str, LineageNode] = {}  # node_id -> node
        self._asset_root: Dict[str, str] = {}  # asset_id -> leaf_node_id

    def _compute_hash(self, node_type: str, parent_id: Optional[str], parent_hash: Optional[str], metadata: Dict[str, Any]) -> str:
        serialized = json.dumps({
            "node_type": node_type,
            "parent_id": parent_id,
            "parent_hash": parent_hash,
            "metadata": metadata,
        }, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def add_node(self, node_id: str, node_type: str, parent_id: Optional[str], metadata: Dict[str, Any]) -> LineageNode:
        parent_hash = None
        if parent_id:
            if parent_id not in self._nodes:
                raise KeyError(f"Parent node '{parent_id}' does not exist in lineage graph.")
            parent_hash = self._nodes[parent_id].node_hash

        node_hash = self._compute_hash(node_type, parent_id, parent_hash, metadata)
        node = LineageNode(
            node_id=node_id,
            node_type=node_type,
            parent_id=parent_id,
            metadata=metadata,
            parent_hash=parent_hash,
            node_hash=node_hash,
        )
        self._nodes[node_id] = node
        return node

    def build_standard_asset_lineage(
        self,
        campaign_id: str,
        mission_id: str,
        direction_id: str,
        dna_id: str,
        prompt_id: str,
        model_id: str,
        render_id: str,
        approval_id: str,
        delivery_id: str,
        asset_id: str,
    ) -> List[LineageNode]:
        """Constructs full 9-stage verified cryptographic lineage."""
        n1 = self.add_node(f"lin_camp_{campaign_id}", "CAMPAIGN", None, {"campaign_id": campaign_id})
        n2 = self.add_node(f"lin_miss_{mission_id}", "MISSION", n1.node_id, {"mission_id": mission_id})
        n3 = self.add_node(f"lin_dir_{direction_id}", "DIRECTION", n2.node_id, {"direction_id": direction_id})
        n4 = self.add_node(f"lin_dna_{dna_id}", "VISUAL_DNA", n3.node_id, {"dna_id": dna_id})
        n5 = self.add_node(f"lin_prm_{prompt_id}", "PROMPT", n4.node_id, {"prompt_id": prompt_id})
        n6 = self.add_node(f"lin_mdl_{model_id}", "MODEL", n5.node_id, {"model_id": model_id, "provider": "Imagen-3"})
        n7 = self.add_node(f"lin_rnd_{render_id}", "RENDER", n6.node_id, {"render_id": render_id, "asset_id": asset_id})
        n8 = self.add_node(f"lin_app_{approval_id}", "APPROVAL", n7.node_id, {"approval_id": approval_id})
        n9 = self.add_node(f"lin_del_{delivery_id}", "DELIVERY", n8.node_id, {"delivery_id": delivery_id, "channel": "Omnichannel"})

        self._asset_root[asset_id] = n9.node_id
        return [n1, n2, n3, n4, n5, n6, n7, n8, n9]

    def get_lineage_trace(self, asset_id: str) -> List[LineageNode]:
        leaf_id = self._asset_root.get(asset_id)
        if not leaf_id:
            return []

        trace = []
        curr_id = leaf_id
        while curr_id:
            node = self._nodes.get(curr_id)
            if not node:
                break
            trace.append(node)
            curr_id = node.parent_id
        trace.reverse()
        return trace

    def verify_lineage_integrity(self, asset_id: str) -> bool:
        trace = self.get_lineage_trace(asset_id)
        if not trace:
            return False

        for i, node in enumerate(trace):
            expected_parent_id = trace[i - 1].node_id if i > 0 else None
            expected_parent_hash = trace[i - 1].node_hash if i > 0 else None

            if node.parent_id != expected_parent_id or node.parent_hash != expected_parent_hash:
                return False

            computed_hash = self._compute_hash(node.node_type, node.parent_id, node.parent_hash, node.metadata)
            if computed_hash != node.node_hash:
                return False

        return True

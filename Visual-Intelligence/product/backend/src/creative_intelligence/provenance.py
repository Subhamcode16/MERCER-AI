"""
Phase 19 - Knowledge Provenance & Lineage Verification.

Manages hash-chained provenance records and verifies cryptographic lineage chains
for all nodes and generalized patterns in the Institutional Knowledge Graph.
"""

import hashlib
from typing import Dict, List, Optional
from .knowledge_models import ProvenanceRecord
from .exceptions import LineageBrokenError


class ProvenanceTracker:
    """Manages immutable hash-chained provenance trace for institutional knowledge assets."""

    def __init__(self):
        self._records: Dict[str, ProvenanceRecord] = {}

    def create_record(
        self,
        source_phase: str,
        evidence_hash: str,
        source_client_id: Optional[str] = None,
        parent_provenance_id: Optional[str] = None
    ) -> ProvenanceRecord:
        """Create and store a hash-chained provenance record."""
        if parent_provenance_id and parent_provenance_id not in self._records:
            raise LineageBrokenError(f"Parent provenance record {parent_provenance_id} not found.")

        record = ProvenanceRecord(
            source_client_id=source_client_id,
            source_phase=source_phase,
            evidence_hash=evidence_hash,
            parent_provenance_id=parent_provenance_id
        )
        
        self._records[record.record_id] = record
        return record

    def get_record(self, record_id: str) -> Optional[ProvenanceRecord]:
        return self._records.get(record_id)

    def verify_chain(self, record_id: str) -> bool:
        """Verify hash integrity back to the root of the lineage chain."""
        current_id = record_id
        visited = set()

        while current_id:
            if current_id in visited:
                raise LineageBrokenError(f"Cyclic lineage detected at {current_id}")
            visited.add(current_id)

            record = self._records.get(current_id)
            if not record:
                raise LineageBrokenError(f"Missing provenance record in chain: {current_id}")

            # Re-compute and compare hash
            computed = record.compute_hash()
            if computed != record.provenance_hash:
                raise LineageBrokenError(
                    f"Hash mismatch in record {current_id}: expected {record.provenance_hash}, got {computed}"
                )

            current_id = record.parent_provenance_id

        return True

    def get_lineage(self, record_id: str) -> List[ProvenanceRecord]:
        """Retrieve full lineage path from leaf to root."""
        lineage = []
        current_id = record_id

        while current_id:
            record = self._records.get(current_id)
            if not record:
                break
            lineage.append(record)
            current_id = record.parent_provenance_id

        return lineage

    def calculate_evidence_hash(self, data: str) -> str:
        """Utility method to compute SHA-256 evidence hash."""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

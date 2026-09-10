"""
Phase 19 - Pattern Discovery Engine.

Discovers high-performing structural patterns from client-scoped executions
and generalizes them into studio-global InstitutionalPatterns.
"""

from typing import Dict, List, Any, Optional
from .knowledge_models import InstitutionalPattern, GraphNode, GraphEdge
from .knowledge_graph import InstitutionalKnowledgeGraph
from .provenance import ProvenanceTracker
from .generalization import ConfidentialityFilter
from .exceptions import ClientDataLeakageError, UnsafeGeneralizationError


class PatternDiscoveryEngine:
    """Discovers and generalizes recurring high-value patterns across client operations."""

    def __init__(
        self,
        knowledge_graph: InstitutionalKnowledgeGraph,
        provenance_tracker: ProvenanceTracker,
        confidentiality_filter: Optional[ConfidentialityFilter] = None
    ):
        self.graph = knowledge_graph
        self.provenance = provenance_tracker
        self.filter = confidentiality_filter or ConfidentialityFilter()
        self._patterns: Dict[str, InstitutionalPattern] = {}

    def discover_pattern_from_executions(
        self,
        pattern_name: str,
        domain: str,
        execution_attributes: Dict[str, Any],
        source_client_id: str,
        evidence_hash: str
    ) -> InstitutionalPattern:
        """Extract structural pattern, scrub client metadata, and store in global namespace."""
        # 1. Create provenance trace for the source client execution
        prov_record = self.provenance.create_record(
            source_client_id=source_client_id,
            source_phase="Phase18_StudioIntelligence",
            evidence_hash=evidence_hash
        )

        # 2. Check for prohibited client data and scrub execution attributes using Confidentiality Filter
        self.filter.validate_anonymization(execution_attributes)
        scrubbed_structure = self.filter.filter_attributes(execution_attributes)

        # 3. Check if identical abstract pattern already exists in global store
        existing_pattern = self._find_matching_pattern(domain, pattern_name)

        if existing_pattern:
            existing_pattern.support_count += 1
            existing_pattern.confidence_score = min(1.0, existing_pattern.confidence_score + 0.1)
            existing_pattern.provenance_ids.append(prov_record.record_id)
            pattern = existing_pattern
        else:
            pattern = InstitutionalPattern(
                pattern_name=pattern_name,
                domain=domain,
                abstract_structure=scrubbed_structure,
                support_count=1,
                confidence_score=0.5,
                provenance_ids=[prov_record.record_id]
            )
            self._patterns[pattern.pattern_id] = pattern

            # 4. Add global GraphNode to KnowledgeGraph
            global_node = GraphNode(
                node_id=pattern.pattern_id,
                namespace="global",
                node_type="InstitutionalPattern",
                attributes={
                    "pattern_name": pattern.pattern_name,
                    "domain": pattern.domain,
                    "confidence_score": pattern.confidence_score,
                    "support_count": pattern.support_count
                },
                provenance_id=prov_record.record_id
            )
            self.graph.add_node(global_node)

        return pattern

    def _find_matching_pattern(self, domain: str, pattern_name: str) -> Optional[InstitutionalPattern]:
        for p in self._patterns.values():
            if p.domain == domain and p.pattern_name == pattern_name:
                return p
        return None

    def get_pattern(self, pattern_id: str) -> Optional[InstitutionalPattern]:
        return self._patterns.get(pattern_id)

    def list_patterns(self, domain: Optional[str] = None) -> List[InstitutionalPattern]:
        if domain:
            return [p for p in self._patterns.values() if p.domain == domain]
        return list(self._patterns.values())

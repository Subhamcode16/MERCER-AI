"""
Authoritative Organizational Intelligence Graph with tenant isolation and bidirectional traversal.
"""
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from .models import GraphEntity, GraphRelationship, EntityType, RelationType, IntelligenceClassification


class TenantAccessViolation(Exception):
    """Raised when cross-tenant graph traversal is attempted without authorization."""
    pass


class OrganizationalIntelligenceGraph:
    def __init__(self):
        self._entities: Dict[str, GraphEntity] = {}
        self._relationships: Dict[str, GraphRelationship] = {}
        # Adjacency indexes: entity_id -> list of relationship_ids
        self._outgoing: Dict[str, List[str]] = defaultdict(list)
        self._incoming: Dict[str, List[str]] = defaultdict(list)

    def add_entity(self, entity: GraphEntity) -> str:
        if not entity.provenance_hashes:
            entity.provenance_hashes.append(entity.compute_hash())
        self._entities[entity.entity_id] = entity
        return entity.entity_id

    def get_entity(self, entity_id: str, tenant_id: Optional[str] = None) -> Optional[GraphEntity]:
        entity = self._entities.get(entity_id)
        if entity is None:
            return None
        if tenant_id and entity.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if entity.tenant_id != tenant_id:
                raise TenantAccessViolation(
                    f"Access denied: Tenant '{tenant_id}' cannot access client-private entity '{entity_id}' owned by '{entity.tenant_id}'."
                )
        return entity

    def add_relationship(self, rel: GraphRelationship) -> str:
        # Verify both entities exist
        source = self._entities.get(rel.source_id)
        target = self._entities.get(rel.target_id)
        if not source or not target:
            raise ValueError(f"Cannot add relationship {rel.relationship_id}: Source or Target entity does not exist.")

        # Cross-tenant boundary check: Forbidden if bridging client-private entities of distinct private tenants
        if source.tenant_id != target.tenant_id:
            if (
                source.classification == IntelligenceClassification.CLIENT_PRIVATE
                and target.classification == IntelligenceClassification.CLIENT_PRIVATE
            ):
                raise TenantAccessViolation("Cannot create relationship bridging client-private entities of distinct tenants.")
            elif (
                source.classification == IntelligenceClassification.CLIENT_PRIVATE
                and target.tenant_id not in (source.tenant_id, "PUBLIC_EXTERNAL", "GLOBAL_INSTITUTIONAL")
            ):
                raise TenantAccessViolation("Cannot link client-private entity to private entity of another tenant.")
            elif (
                target.classification == IntelligenceClassification.CLIENT_PRIVATE
                and source.tenant_id not in (target.tenant_id, "PUBLIC_EXTERNAL", "GLOBAL_INSTITUTIONAL")
            ):
                raise TenantAccessViolation("Cannot link client-private entity to private entity of another tenant.")

        if not rel.provenance_hash:
            rel.provenance_hash = rel.compute_hash()

        self._relationships[rel.relationship_id] = rel
        self._outgoing[rel.source_id].append(rel.relationship_id)
        self._incoming[rel.target_id].append(rel.relationship_id)
        return rel.relationship_id

    def get_relationships(
        self,
        entity_id: str,
        direction: str = "OUTGOING",
        tenant_id: Optional[str] = None,
        relation_type: Optional[RelationType] = None,
    ) -> List[GraphRelationship]:
        self.get_entity(entity_id, tenant_id=tenant_id)  # Validate tenant access
        rel_ids = self._outgoing[entity_id] if direction == "OUTGOING" else self._incoming[entity_id]
        
        results = []
        for r_id in rel_ids:
            rel = self._relationships[r_id]
            if relation_type and rel.relation_type != relation_type:
                continue
            if tenant_id and rel.classification == IntelligenceClassification.CLIENT_PRIVATE:
                if rel.tenant_id != tenant_id:
                    continue
            results.append(rel)
        return results

    def traverse_evidence_chain(self, start_entity_id: str, tenant_id: Optional[str] = None) -> List[Tuple[GraphEntity, GraphRelationship, GraphEntity]]:
        """
        Traverses provenance and evidence backwards from a high-level entity (e.g. Recommendation -> Scenario -> Signal -> Hypothesis -> Outcome).
        """
        start = self.get_entity(start_entity_id, tenant_id=tenant_id)
        if not start:
            return []

        chain = []
        visited_nodes: Set[str] = {start_entity_id}
        queue = [start_entity_id]

        while queue:
            curr_id = queue.pop(0)
            incoming_rels = self.get_relationships(curr_id, direction="INCOMING", tenant_id=tenant_id)
            for rel in incoming_rels:
                if rel.relation_type in (RelationType.SUPPORTS, RelationType.DERIVED_FROM, RelationType.INFORMS):
                    source = self.get_entity(rel.source_id, tenant_id=tenant_id)
                    target = self.get_entity(rel.target_id, tenant_id=tenant_id)
                    if source and target:
                        chain.append((source, rel, target))
                        if rel.source_id not in visited_nodes:
                            visited_nodes.add(rel.source_id)
                            queue.append(rel.source_id)
        return chain

    def count_entities(self, tenant_id: Optional[str] = None) -> int:
        if not tenant_id:
            return len(self._entities)
        return sum(1 for e in self._entities.values() if e.tenant_id == tenant_id or e.classification != IntelligenceClassification.CLIENT_PRIVATE)

    def count_relationships(self, tenant_id: Optional[str] = None) -> int:
        if not tenant_id:
            return len(self._relationships)
        return sum(1 for r in self._relationships.values() if r.tenant_id == tenant_id or r.classification != IntelligenceClassification.CLIENT_PRIVATE)

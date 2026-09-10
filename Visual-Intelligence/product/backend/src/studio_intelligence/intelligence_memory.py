"""
Phase 18 Studio Intelligence Memory.

Stores reusable creative and operational knowledge per client context
under strict multi-client isolation boundaries.
"""

from typing import Dict, List, Optional
import threading

from src.studio_intelligence.outcome_models import IntelligenceKnowledgeItem
from src.studio_intelligence.exceptions import CrossClientIntelligenceViolation


class StudioIntelligenceMemory:
    """Provenance-aware storage of reusable creative and operational intelligence."""

    def __init__(self):
        self._lock = threading.RLock()
        self._items: Dict[str, IntelligenceKnowledgeItem] = {}
        self._client_index: Dict[str, List[str]] = {}

    def store_knowledge_item(
        self, requesting_client_id: str, item: IntelligenceKnowledgeItem
    ) -> IntelligenceKnowledgeItem:
        """Stores a knowledge item under strict client isolation."""
        if requesting_client_id != item.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot store knowledge item for '{item.client_id}'."
            )

        with self._lock:
            self._items[item.item_id] = item
            if item.client_id not in self._client_index:
                self._client_index[item.client_id] = []
            if item.item_id not in self._client_index[item.client_id]:
                self._client_index[item.client_id].append(item.item_id)
            return item

    def get_knowledge_item(
        self, requesting_client_id: str, item_id: str
    ) -> Optional[IntelligenceKnowledgeItem]:
        """Retrieves a single knowledge item enforcing client isolation."""
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            if requesting_client_id != item.client_id:
                raise CrossClientIntelligenceViolation(
                    f"Client '{requesting_client_id}' cannot access item owned by '{item.client_id}'."
                )
            return item

    def list_knowledge_items(
        self, requesting_client_id: str, target_client_id: str, category: Optional[str] = None
    ) -> List[IntelligenceKnowledgeItem]:
        """Lists knowledge items for a target client context."""
        if requesting_client_id != target_client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot access knowledge items for '{target_client_id}'."
            )

        with self._lock:
            item_ids = self._client_index.get(target_client_id, [])
            results = []
            for iid in item_ids:
                item = self._items.get(iid)
                if item:
                    if category is None or item.category == category:
                        results.append(item)
            return results

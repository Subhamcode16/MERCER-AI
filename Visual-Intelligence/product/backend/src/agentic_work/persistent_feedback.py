"""
Phase 9 — Persistent Feedback & Threshold Learning Engine

Manages structured user/critique feedback, enforces feedback replay defense,
and aggregates patterns into LearningPatterns when N >= 3 consistent signals occur.
"""

from collections import defaultdict
import json
import os
from pathlib import Path
import tempfile
import threading
from typing import Any, Dict, List, Optional, Set

from src.agentic_work.memory_models import (
    FeedbackRecord,
    FeedbackSource,
    LearningPattern,
    LearningPatternType,
)


class DuplicateFeedbackError(ValueError):
    """Raised when attempting to re-record an existing feedback_id (Replay Defense)."""

    pass


class PersistentFeedbackEngine:
    """File-backed feedback recording and threshold learning pattern engine."""

    def __init__(self, base_dir: Optional[str] = None, aggregation_threshold: int = 3):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "data", "phase9_feedback")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.aggregation_threshold = aggregation_threshold
        self._recorded_ids: Set[str] = set()
        self._lock = threading.Lock()
        self._load_existing_ids()

    def _load_existing_ids(self) -> None:
        for file_path in self.base_dir.glob("fb_*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "feedback_id" in data:
                        self._recorded_ids.add(data["feedback_id"])
            except Exception:
                continue

    def record_feedback(self, record: FeedbackRecord) -> str:
        """Records a feedback item atomically after verifying replay protection."""
        with self._lock:
            if record.feedback_id in self._recorded_ids:
                raise DuplicateFeedbackError(
                    f"Feedback ID '{record.feedback_id}' has already been recorded."
                )

            file_path = self.base_dir / f"fb_{record.feedback_id}.json"
            record_dict = record.to_dict()

            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.base_dir, prefix="fb_tmp_", suffix=".tmp"
            )
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(record_dict, f, indent=2)
                os.replace(temp_path, file_path)
                self._recorded_ids.add(record.feedback_id)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

        return str(file_path)

    def list_feedback(
        self,
        target_role: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[FeedbackRecord]:
        """Lists recorded feedback records."""
        records: List[FeedbackRecord] = []
        for file_path in self.base_dir.glob("fb_*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                rec = FeedbackRecord(
                    feedback_id=data["feedback_id"],
                    workflow_id=data["workflow_id"],
                    source=FeedbackSource(data["source"]),
                    category=data["category"],
                    target_role=data["target_role"],
                    rating=data["rating"],
                    comments=data["comments"],
                    defect_code=data.get("defect_code"),
                    timestamp=data["timestamp"],
                )
                if target_role and rec.target_role != target_role:
                    continue
                if category and rec.category != category:
                    continue
                records.append(rec)
            except Exception:
                continue

        return records

    def aggregate_learning_patterns(self) -> List[LearningPattern]:
        """Aggregates feedback into LearningPatterns if occurrences >= aggregation_threshold (N >= 3)."""
        all_fb = self.list_feedback()

        # Group by (target_role, defect_code/category)
        grouped: Dict[tuple, List[FeedbackRecord]] = defaultdict(list)
        for fb in all_fb:
            key_code = fb.defect_code if fb.defect_code else fb.category
            grouped[(fb.target_role, key_code)].append(fb)

        patterns: List[LearningPattern] = []
        for (target_role, key_code), fb_list in grouped.items():
            if len(fb_list) >= self.aggregation_threshold:
                pattern_id = f"pattern_{target_role}_{key_code}_{len(fb_list)}"
                fb_ids = [fb.feedback_id for fb in fb_list]
                
                # Derive suggested adaptation parameters based on defect
                suggested_adaptation = {
                    "target_role": target_role,
                    "defect_code": key_code,
                    "critique_weight_adjustment": +0.1,
                    "recommended_prompt_emphasis": f"Pay extra attention to resolving '{key_code}'",
                }

                pattern = LearningPattern(
                    pattern_id=pattern_id,
                    pattern_type=LearningPatternType.RECURRING_DEFECT,
                    target_role=target_role,
                    trigger_defect_code=key_code,
                    occurrence_count=len(fb_list),
                    supporting_feedback_ids=fb_ids,
                    suggested_adaptation=suggested_adaptation,
                    confidence_score=min(1.0, 0.5 + (0.1 * len(fb_list))),
                )
                patterns.append(pattern)

        return patterns

    def clear(self) -> None:
        """Removes all stored feedback records."""
        with self._lock:
            for file_path in self.base_dir.glob("fb_*.json"):
                try:
                    file_path.unlink()
                except OSError:
                    pass
            self._recorded_ids.clear()

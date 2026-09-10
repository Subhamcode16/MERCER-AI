"""
Phase 25 Visual Knowledge and Aesthetic Gap Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class VisualGapItem:
    gap_id: str
    task_category: str
    observed_weakness_description: str
    impact_level: str # LOW, MEDIUM, HIGH
    recommended_training_set: str
    status: str # UNRESOLVED, TRAINING_QUEUED, RESOLVED

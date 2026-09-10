"""
Phase 20 - Intelligence Failure Taxonomy (GAP-A through GAP-J).

Classifies every benchmark failure into a standard failure taxonomy before fine-tuning/training.
A benchmark failure is NOT automatically a training problem!
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class FailureCategory(str, Enum):
    GAP_A = "GAP_A_MISSING_KNOWLEDGE"
    GAP_B = "GAP_B_RETRIEVAL_FAILURE"
    GAP_C = "GAP_C_REASONING_FAILURE"
    GAP_D = "GAP_D_VISION_PERCEPTION_FAILURE"
    GAP_E = "GAP_E_CONTEXT_FAILURE"
    GAP_F = "GAP_F_INSTRUCTION_FOLLOWING_FAILURE"
    GAP_G = "GAP_G_EVALUATION_CALIBRATION_FAILURE"
    GAP_H = "GAP_H_DATA_PROVENANCE_PROBLEM"
    GAP_I = "GAP_I_MODEL_CAPABILITY_LIMITATION"
    GAP_J = "GAP_J_WORKFLOW_ORCHESTRATION_FAILURE"


class FailureRecord(BaseModel):
    """Detailed classification of a visual or intelligence benchmark failure."""
    case_id: str
    failure_category: FailureCategory
    description: str
    recommended_remedy: str  # e.g. "Use retrieval", "Improve prompt instruction", "Fine-tuning candidate"
    is_training_candidate: bool = False  # True only if retrieval/prompting/eval are insufficient

"""
Phase 25 Distilled Learning Signals View (Immutable, Zero Security Mutation).
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List
import time

@dataclass
class LearningSignalRecord:
    signal_id: str
    tenant_id: str
    client_id: str
    category: str # CREATIVE, VISUAL, TIMING, CHANNEL
    pattern_summary: str
    confidence_score: float
    evidence_id: str
    timestamp: float = field(default_factory=time.time)
    policy_mutation_attempted: bool = False

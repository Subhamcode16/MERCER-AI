"""
IF-AGENT-008 Feedback & Learning Signal Capture Engine.
Captures system errors, staff failures, critique findings, reviewer decisions,
and user ratings into structured LearningSignal artifacts.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from .models import LearningSignal


class FeedbackEngine:
    """
    Feedback Collector & Signal Generator.
    Converts execution outcomes into structured LearningSignal records.
    """

    def create_signal(
        self,
        workflow_id: str,
        source: str,
        category: str,
        observed_failure: str,
        expected_behavior: str,
        correction: str,
        task_id: Optional[str] = None,
        confidence: float = 0.85
    ) -> LearningSignal:
        if category.upper() == "SECURITY_POLICY":
            raise ValueError("Learning signals cannot target SECURITY_POLICY")

        return LearningSignal(
            signal_id=f"sig-{uuid.uuid4().hex[:8]}",
            workflow_id=workflow_id,
            task_id=task_id,
            source=source,
            category=category,
            observed_failure=observed_failure,
            expected_behavior=expected_behavior,
            correction=correction,
            confidence=confidence,
        )

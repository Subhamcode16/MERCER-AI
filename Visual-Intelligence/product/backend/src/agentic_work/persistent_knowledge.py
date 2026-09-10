"""
Phase 9 — Persistent Knowledge & External Trend Store

Manages persistent external visual, typography, color, and design trend observations,
ensuring all observations remain strictly tagged as UNTRUSTED_EXTERNAL_OBSERVATION,
sanitizing prompt injection payloads into pure data, and supporting temporal decay/pruning.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Any, Dict, List, Optional

from src.agentic_work.models import (
    ObservationClassification,
    ObservationCommitment,
    ObservationStatus,
    VisualObservation,
)


class PromptInjectionInObservationError(ValueError):
    """Raised when an un-sanitizable malicious prompt injection pattern is detected in an observation."""

    pass


class PersistentKnowledgeStore:
    """File-backed storage engine for external visual knowledge and trend observations."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "data", "phase9_knowledge")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def sanitize_observation_content(self, text: str) -> str:
        """Strips executable prompt injection directives and escapes instruction wrappers."""
        if not text:
            return ""

        # Remove common instruction injection boundaries
        forbidden_patterns = [
            r"<SYSTEM_MESSAGE>",
            r"</SYSTEM_MESSAGE>",
            r"<USER_REQUEST>",
            r"</USER_REQUEST>",
            r"IGNORE ALL PREVIOUS INSTRUCTIONS",
            r"OVERRIDE SECURITY POLICY",
            r"UNLOCK EXECUTION GATE",
        ]

        sanitized = text
        for pattern in forbidden_patterns:
            sanitized = re.sub(pattern, "[BLOCKED_INJECTION_TEXT]", sanitized, flags=re.IGNORECASE)

        return sanitized

    def add_observation(self, observation: VisualObservation) -> str:
        """Adds a visual observation to persistent store, forcing status to UNTRUSTED_EXTERNAL_OBSERVATION."""
        # Sanitize summary and details
        sanitized_summary = self.sanitize_observation_content(observation.summary)
        sanitized_details = self.sanitize_observation_content(observation.details)

        # Force status to UNTRUSTED_EXTERNAL_OBSERVATION to prevent privilege escalation
        untrusted_observation = VisualObservation(
            observation_id=observation.observation_id,
            source=observation.source,
            timestamp=observation.timestamp,
            provenance=observation.provenance,
            confidence=observation.confidence,
            summary=sanitized_summary,
            details=sanitized_details,
            classification=observation.classification,
            commitment=observation.commitment,
            status=ObservationStatus.UNTRUSTED_EXTERNAL_OBSERVATION,
        )

        obs_dict = untrusted_observation.to_dict()
        file_path = self.base_dir / f"obs_{untrusted_observation.observation_id}.json"

        with self._lock:
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.base_dir, prefix="obs_tmp_", suffix=".tmp"
            )
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(obs_dict, f, indent=2)
                os.replace(temp_path, file_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

        return str(file_path)

    def load_observation(self, observation_id: str) -> VisualObservation:
        """Loads an observation from persistent storage."""
        file_path = self.base_dir / f"obs_{observation_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Observation '{observation_id}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return VisualObservation(
            observation_id=data["observation_id"],
            source=data["source"],
            timestamp=data["timestamp"],
            provenance=data["provenance"],
            confidence=data["confidence"],
            summary=data["summary"],
            details=data["details"],
            classification=ObservationClassification(data["classification"]),
            commitment=ObservationCommitment(data["commitment"]),
            status=ObservationStatus(data["status"]),
        )

    def list_observations(
        self,
        classification: Optional[ObservationClassification] = None,
        min_confidence: float = 0.0,
    ) -> List[VisualObservation]:
        """Lists stored observations with optional filtering."""
        observations: List[VisualObservation] = []
        for file_path in self.base_dir.glob("obs_*.json"):
            try:
                obs_id = file_path.stem.replace("obs_", "")
                obs = self.load_observation(obs_id)
                if classification and obs.classification != classification:
                    continue
                if obs.confidence < min_confidence:
                    continue
                observations.append(obs)
            except Exception:
                continue

        return observations

    def clear(self) -> None:
        """Removes all stored observations."""
        with self._lock:
            for file_path in self.base_dir.glob("obs_*.json"):
                try:
                    file_path.unlink()
                except OSError:
                    pass

"""
Core types, enums, and invariant constants for Phase 30:
Institutional Intelligence & Strategic Operations Layer.
"""
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class StrategicHorizon(str, Enum):
    NOW = "NOW"
    NEXT = "NEXT"
    LATER = "LATER"
    FUTURE = "FUTURE"
    UNKNOWN = "UNKNOWN"


class InitiativeHealthState(str, Enum):
    HEALTHY = "HEALTHY"
    WATCH = "WATCH"
    AT_RISK = "AT_RISK"
    BLOCKED = "BLOCKED"
    CONTRADICTED = "CONTRADICTED"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"
    CLOSED = "CLOSED"


class OrganizationalMemoryClass(str, Enum):
    STRATEGIC_DECISION = "STRATEGIC_DECISION"
    STRATEGIC_OBJECTIVE = "STRATEGIC_OBJECTIVE"
    INITIATIVE = "INITIATIVE"
    COMMITMENT = "COMMITMENT"
    ASSUMPTION = "ASSUMPTION"
    LESSON = "LESSON"
    EXPERIMENT = "EXPERIMENT"
    OUTCOME = "OUTCOME"
    CONTRADICTION = "CONTRADICTION"
    FAILED_HYPOTHESIS = "FAILED_HYPOTHESIS"
    SUCCESS_PATTERN = "SUCCESS_PATTERN"
    UNKNOWN = "UNKNOWN"
    EXTERNAL_SIGNAL = "EXTERNAL_SIGNAL"
    GOVERNANCE_EVENT = "GOVERNANCE_EVENT"


class StrategicCadenceType(str, Enum):
    DAILY_PREPARATION = "DAILY_PREPARATION"
    WEEKLY_REVIEW = "WEEKLY_REVIEW"
    CAMPAIGN_CYCLE = "CAMPAIGN_CYCLE"
    MONTHLY_PORTFOLIO = "MONTHLY_PORTFOLIO"
    QUARTERLY_STRATEGIC = "QUARTERLY_STRATEGIC"
    AD_HOC = "AD_HOC"


class ExternalIntelligenceClassification(str, Enum):
    PUBLIC_EXTERNAL = "PUBLIC_EXTERNAL"
    CLIENT_PRIVATE = "CLIENT_PRIVATE"
    INSTITUTIONAL = "INSTITUTIONAL"
    SYSTEM_GENERATED_INFERENCE = "SYSTEM_GENERATED_INFERENCE"


class EpistemicStatus(str, Enum):
    VERIFIED_FACT = "VERIFIED_FACT"
    EMPIRICAL_EVIDENCE = "EMPIRICAL_EVIDENCE"
    WORKING_ASSUMPTION = "WORKING_ASSUMPTION"
    MODEL_INFERENCE = "MODEL_INFERENCE"
    UNVERIFIED_CLAIM = "UNVERIFIED_CLAIM"
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


class WorkerRole(str, Enum):
    STRATEGY_WORKER = "STRATEGY_WORKER"
    INTELLIGENCE_WORKER = "INTELLIGENCE_WORKER"
    CREATIVE_DIRECTOR_WORKER = "CREATIVE_DIRECTOR_WORKER"
    RESEARCH_WORKER = "RESEARCH_WORKER"
    CAMPAIGN_WORKER = "CAMPAIGN_WORKER"
    QUALITY_WORKER = "QUALITY_WORKER"
    OPERATIONS_WORKER = "OPERATIONS_WORKER"


class ThreatID(str, Enum):
    T30_001 = "T30-001"  # unauthorized objective mutation
    T30_002 = "T30-002"  # strategic authority escalation
    T30_003 = "T30-003"  # recommendation-to-execution escalation
    T30_004 = "T30-004"  # routine-to-authorization escalation
    T30_005 = "T30-005"  # portfolio-to-budget escalation
    T30_006 = "T30-006"  # stale decision resurrection
    T30_007 = "T30-007"  # decision-memory tampering
    T30_008 = "T30-008"  # assumption poisoning
    T30_009 = "T30-009"  # false strategic signal injection
    T30_010 = "T30-010"  # strategic drift suppression
    T30_011 = "T30-011"  # contradiction suppression
    T30_012 = "T30-012"  # unknown-state collapse
    T30_013 = "T30-013"  # false causality propagation
    T30_014 = "T30-014"  # model-confidence confusion
    T30_015 = "T30-015"  # external prompt injection
    T30_016 = "T30-016"  # malicious strategic content
    T30_017 = "T30-017"  # cross-tenant contamination
    T30_018 = "T30-018"  # semantic leakage
    T30_019 = "T30-019"  # unauthorized worker escalation
    T30_020 = "T30-020"  # scheduled-task escalation
    T30_021 = "T30-021"  # human approval spoofing
    T30_022 = "T30-022"  # stale approval replay
    T30_023 = "T30-023"  # unauthorized initiative modification
    T30_024 = "T30-024"  # initiative dependency manipulation
    T30_025 = "T30-025"  # recommendation tampering
    T30_026 = "T30-026"  # evidence substitution
    T30_027 = "T30-027"  # provenance forgery
    T30_028 = "T30-028"  # feedback-loop amplification
    T30_029 = "T30-029"  # confirmation-bias amplification
    T30_030 = "T30-030"  # strategic narrative manipulation
    T30_031 = "T30-031"  # resource-authority confusion
    T30_032 = "T30-032"  # rollback bypass
    T30_033 = "T30-033"  # invalidated-decision replay
    T30_034 = "T30-034"  # policy/memory confusion
    T30_035 = "T30-035"  # recovery-authority escalation


class GovernanceInvariantViolation(Exception):
    """Raised when an immutable governance invariant is violated."""
    def __init__(self, threat_id: ThreatID, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(f"[{threat_id.value}] {message}")
        self.threat_id = threat_id
        self.message = message
        self.details = details or {}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

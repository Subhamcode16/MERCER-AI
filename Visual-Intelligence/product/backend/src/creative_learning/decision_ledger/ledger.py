"""
Phase 28 Cryptographic Decision Ledger Implementation.
"""
from typing import Dict, List, Optional, Any
import hashlib
import json
import uuid
from datetime import datetime, timezone

from .models import (
    DecisionType,
    DecisionAlternative,
    DecisionContextSnapshot,
    CampaignDecisionRecord,
)


class DecisionLedger:
    """Maintains an append-only, tamper-evident cryptographic ledger of all material campaign decisions."""

    def __init__(self):
        self._records: Dict[str, CampaignDecisionRecord] = {}  # decision_id -> record
        self._campaign_timeline: Dict[str, List[str]] = {}  # campaign_id -> [decision_id, ...]

    def _compute_hash(
        self,
        decision_id: str,
        campaign_id: str,
        decision_type: DecisionType,
        decision_version: int,
        parent_hash: Optional[str],
        decision: str,
        rationale: str,
        context_snapshot: DecisionContextSnapshot,
    ) -> str:
        payload = {
            "decision_id": decision_id,
            "campaign_id": campaign_id,
            "decision_type": decision_type.value,
            "decision_version": decision_version,
            "parent_hash": parent_hash,
            "decision": decision,
            "rationale": rationale,
            "snapshot_id": context_snapshot.snapshot_id,
        }
        serialized = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def record_decision(
        self,
        campaign_id: str,
        decision_type: DecisionType,
        actor_id: str,
        context_snapshot: DecisionContextSnapshot,
        decision: str,
        rationale: str,
        confidence: float,
        worker_id: Optional[str] = None,
        evidence_refs: Optional[List[str]] = None,
        alternatives: Optional[List[DecisionAlternative]] = None,
        assumptions: Optional[List[str]] = None,
        unknowns: Optional[List[str]] = None,
        expected_impact: str = "",
    ) -> CampaignDecisionRecord:
        timeline = self._campaign_timeline.get(campaign_id, [])
        parent_hash = None
        version = len(timeline) + 1

        if timeline:
            last_record_id = timeline[-1]
            parent_hash = self._records[last_record_id].record_hash

        decision_id = f"dec_{uuid.uuid4().hex[:10]}"
        record_hash = self._compute_hash(
            decision_id,
            campaign_id,
            decision_type,
            version,
            parent_hash,
            decision,
            rationale,
            context_snapshot,
        )

        record = CampaignDecisionRecord(
            decision_id=decision_id,
            campaign_id=campaign_id,
            decision_type=decision_type,
            decision_version=version,
            actor_id=actor_id,
            worker_id=worker_id,
            timestamp=datetime.now(timezone.utc),
            context_snapshot=context_snapshot,
            decision=decision,
            rationale=rationale,
            evidence_refs=evidence_refs or [],
            alternatives=alternatives or [],
            confidence=confidence,
            assumptions=assumptions or [],
            unknowns=unknowns or ["Market macro shift", "Competitor counter-campaign"],
            expected_impact=expected_impact,
            parent_hash=parent_hash,
            record_hash=record_hash,
            status="COMMITTED",
        )

        self._records[decision_id] = record
        if campaign_id not in self._campaign_timeline:
            self._campaign_timeline[campaign_id] = []
        self._campaign_timeline[campaign_id].append(decision_id)
        return record

    def get_decision(self, decision_id: str) -> Optional[CampaignDecisionRecord]:
        return self._records.get(decision_id)

    def list_decisions_for_campaign(self, campaign_id: str) -> List[CampaignDecisionRecord]:
        decision_ids = self._campaign_timeline.get(campaign_id, [])
        return [self._records[did] for did in decision_ids]

    def verify_ledger_integrity(self, campaign_id: str) -> bool:
        decision_ids = self._campaign_timeline.get(campaign_id, [])
        if not decision_ids:
            return True

        for i, did in enumerate(decision_ids):
            rec = self._records.get(did)
            if not rec:
                return False

            expected_parent_hash = self._records[decision_ids[i - 1]].record_hash if i > 0 else None
            if rec.parent_hash != expected_parent_hash:
                return False

            computed_hash = self._compute_hash(
                rec.decision_id,
                rec.campaign_id,
                rec.decision_type,
                rec.decision_version,
                rec.parent_hash,
                rec.decision,
                rec.rationale,
                rec.context_snapshot,
            )
            if computed_hash != rec.record_hash:
                return False

        return True

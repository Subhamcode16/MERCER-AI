"""
Reconciliation Policy Engine for Visual Intelligence Security Substrate (Phase 8).

Implements deterministic evaluation rules to identify inconsistencies, conflicts,
audit discontinuities, research boundaries, and missing records across security snapshots.
"""

import time
from typing import List, Tuple

from .reconciliation_models import (
    ReconciliationFinding,
    ReconciliationReasonCode,
    ReconciliationSource,
    ReconciliationSnapshot,
    ReconciliationStatus,
)


class ReconciliationPolicy:
    """Evaluates a ReconciliationSnapshot to produce deterministic findings and status."""

    MAX_FRESHNESS_WINDOW_SECONDS = 900.0  # 15 minutes

    def evaluate(self, snapshot: ReconciliationSnapshot) -> Tuple[ReconciliationStatus, List[ReconciliationFinding]]:
        findings: List[ReconciliationFinding] = []
        finding_seq = 1

        def _add_finding(
            source: ReconciliationSource,
            reason_code: ReconciliationReasonCode,
            description: str,
            affected_record_ids: List[str] = None,
            metadata: dict = None,
        ) -> None:
            nonlocal finding_seq
            finding_id = f"fnd-{snapshot.snapshot_id}-{finding_seq:04d}"
            finding_seq += 1
            findings.append(
                ReconciliationFinding(
                    finding_id=finding_id,
                    source=source,
                    reason_code=reason_code,
                    description=description,
                    affected_record_ids=affected_record_ids or [],
                    metadata=metadata or {},
                )
            )

        # 1. Identity & Provenance Cross-Reference Verification
        for record_list, src_enum in [
            (snapshot.evidence_records, ReconciliationSource.EVIDENCE_ORCHESTRATOR),
            (snapshot.decision_records, ReconciliationSource.DECISION_ENGINE),
            (snapshot.attestation_records, ReconciliationSource.DECISION_ENGINE),
            (snapshot.audit_records, ReconciliationSource.AUDIT_BOUNDARY),
            (snapshot.recovery_records, ReconciliationSource.RECOVERY_MANAGER),
            (snapshot.research_records, ReconciliationSource.FROST_PROTOTYPE),
        ]:
            for rec in record_list:
                rec_id = rec.get("record_id") or rec.get("evidence_id") or rec.get("decision_id") or rec.get("attestation_id") or "unknown"
                rec_sys = rec.get("system_id")
                if rec_sys and rec_sys != snapshot.system_id:
                    _add_finding(
                        source=src_enum,
                        reason_code=ReconciliationReasonCode.PROVENANCE_MISMATCH,
                        description=f"Record '{rec_id}' system_id '{rec_sys}' mismatches snapshot system_id '{snapshot.system_id}'.",
                        affected_record_ids=[str(rec_id)],
                    )
                rec_corr = rec.get("correlation_id")
                if rec_corr and rec_corr != snapshot.correlation_id:
                    _add_finding(
                        source=src_enum,
                        reason_code=ReconciliationReasonCode.REFERENCE_MISMATCH,
                        description=f"Record '{rec_id}' correlation_id '{rec_corr}' mismatches snapshot correlation_id '{snapshot.correlation_id}'.",
                        affected_record_ids=[str(rec_id)],
                    )

        # 2. Quarantined Evidence Inspection
        for ev in snapshot.evidence_records:
            ev_id = str(ev.get("evidence_id") or ev.get("record_id") or "ev-unknown")
            ev_status = str(ev.get("lifecycle_status") or ev.get("status") or "")
            if ev_status.upper() == "QUARANTINED":
                _add_finding(
                    source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
                    reason_code=ReconciliationReasonCode.QUARANTINED_RECORD,
                    description=f"Evidence record '{ev_id}' is in QUARANTINED state.",
                    affected_record_ids=[ev_id],
                )

        # 3. Classification Conflict Inspection
        for dec in snapshot.decision_records:
            dec_id = str(dec.get("decision_id") or dec.get("record_id") or "dec-unknown")
            dec_cls = str(dec.get("classification") or dec.get("decision") or "")
            dec_reason = str(dec.get("reason_code") or "")
            if dec_cls.upper() == "EVIDENCE_CONFLICT" or dec_reason.upper() == "CLASSIFICATION_CONFLICT":
                _add_finding(
                    source=ReconciliationSource.DECISION_ENGINE,
                    reason_code=ReconciliationReasonCode.CLASSIFICATION_CONFLICT,
                    description=f"Decision record '{dec_id}' exhibits classification conflict: {dec_reason}.",
                    affected_record_ids=[dec_id],
                )

        # Cross-layer classification mismatch (e.g. evidence REJECTED but decision claims non-rejected)
        for ev in snapshot.evidence_records:
            ev_id = str(ev.get("evidence_id") or ev.get("record_id") or "")
            ev_status = str(ev.get("lifecycle_status") or "").upper()
            if ev_status in ("REJECTED", "INVALID"):
                for dec in snapshot.decision_records:
                    dec_id = str(dec.get("decision_id") or dec.get("record_id") or "")
                    dec_cls = str(dec.get("classification") or "").upper()
                    if dec_cls in ("VALIDATED_VERDICT", "CONFIRMED"):
                        _add_finding(
                            source=ReconciliationSource.DECISION_ENGINE,
                            reason_code=ReconciliationReasonCode.CLASSIFICATION_CONFLICT,
                            description=f"Evidence '{ev_id}' is {ev_status} but Decision '{dec_id}' asserts {dec_cls}.",
                            affected_record_ids=[ev_id, dec_id],
                        )

        # 4. Audit Chain Discontinuity / Integrity Inspection
        for aud in snapshot.audit_records:
            aud_id = str(aud.get("record_id") or aud.get("audit_id") or "aud-unknown")
            valid_flag = aud.get("chain_valid")
            if valid_flag is False or aud.get("integrity_result") == "INVALID":
                _add_finding(
                    source=ReconciliationSource.AUDIT_BOUNDARY,
                    reason_code=ReconciliationReasonCode.AUDIT_INTEGRITY_FAILURE,
                    description=f"Audit record '{aud_id}' reports audit chain integrity failure.",
                    affected_record_ids=[aud_id],
                )

        # 5. Missing Records Inspection
        if not snapshot.evidence_records and not snapshot.research_records:
            _add_finding(
                source=ReconciliationSource.EVIDENCE_ORCHESTRATOR,
                reason_code=ReconciliationReasonCode.EVIDENCE_MISSING,
                description="Snapshot contains no evidence records.",
            )
        if not snapshot.decision_records:
            _add_finding(
                source=ReconciliationSource.DECISION_ENGINE,
                reason_code=ReconciliationReasonCode.DECISION_MISSING,
                description="Snapshot contains no decision records.",
            )
        if not snapshot.attestation_records:
            _add_finding(
                source=ReconciliationSource.DECISION_ENGINE,
                reason_code=ReconciliationReasonCode.ATTESTATION_MISSING,
                description="Snapshot contains no attestation records.",
            )

        # 6. Research Artifact Boundaries
        if snapshot.research_records:
            for res in snapshot.research_records:
                res_id = str(res.get("record_id") or res.get("prototype_id") or "res-unknown")
                _add_finding(
                    source=ReconciliationSource.FROST_PROTOTYPE,
                    reason_code=ReconciliationReasonCode.RESEARCH_BOUND_ONLY,
                    description=f"Record '{res_id}' is research/test-only and cannot establish production trust.",
                    affected_record_ids=[res_id],
                    metadata={"trust_marker": "TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION"},
                )

        # 7. Stale / Expired Check
        now = time.time()
        if (now - snapshot.timestamp) > self.MAX_FRESHNESS_WINDOW_SECONDS:
            _add_finding(
                source=ReconciliationSource.ASSURANCE_LOOP,
                reason_code=ReconciliationReasonCode.EXPIRED_RECORD,
                description=f"Snapshot timestamp ({snapshot.timestamp}) exceeds max freshness window ({self.MAX_FRESHNESS_WINDOW_SECONDS}s).",
            )

        # Determine overall status based on finding severity precedence
        reason_codes = {f.reason_code for f in findings}

        if ReconciliationReasonCode.QUARANTINED_RECORD in reason_codes:
            status = ReconciliationStatus.QUARANTINED
        elif ReconciliationReasonCode.CLASSIFICATION_CONFLICT in reason_codes:
            status = ReconciliationStatus.CONFLICT
        elif (
            ReconciliationReasonCode.PROVENANCE_MISMATCH in reason_codes
            or ReconciliationReasonCode.REFERENCE_MISMATCH in reason_codes
            or ReconciliationReasonCode.AUDIT_INTEGRITY_FAILURE in reason_codes
        ):
            status = ReconciliationStatus.INCONSISTENT
        elif (
            ReconciliationReasonCode.EVIDENCE_MISSING in reason_codes
            or ReconciliationReasonCode.DECISION_MISSING in reason_codes
            or ReconciliationReasonCode.ATTESTATION_MISSING in reason_codes
        ):
            status = ReconciliationStatus.INCOMPLETE
        else:
            status = ReconciliationStatus.CONSISTENT
            if not findings:
                _add_finding(
                    source=ReconciliationSource.ASSURANCE_LOOP,
                    reason_code=ReconciliationReasonCode.ALL_RECORDS_CONSISTENT,
                    description="All evaluated records are mutually consistent and intact.",
                )

        return status, findings

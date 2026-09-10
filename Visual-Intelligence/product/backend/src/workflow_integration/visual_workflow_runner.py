"""
Visual Workflow Runner for Visual Intelligence Real Application Pipeline (Phase 8).

Orchestrates end-to-end execution of VisionAdapter analysis and security-substrate verification.
Enforces non-authoritative execution limits (ExecutionGate remains locked throughout).
"""

import hashlib
import time
from typing import Any, Dict, Optional

from app.adapters.vision_adapter import VisionAdapter
from src.security_substrate import ExecutionGate
from .security_integration_adapter import SecurityIntegrationAdapter
from .workflow_models import (
    WorkflowRunContext,
    WorkflowRunResult,
    WorkflowStage,
    WorkflowStatus,
)


class VisualWorkflowRunner:
    """
    End-to-end application runner executing the Visual Intelligence workflow through the security substrate.
    
    Stages Executed:
    1. OBSERVE — VisionAdapter analysis (textile/garment DNA & raw claims)
    2. VERIFY — Phase 2 Ephemeral verification
    3. ORCHESTRATE — Phase 5 Evidence ingestion
    4. DECIDE — Phase 6 Security decision & attestation
    5. AUDIT — Phase 7 Audit trail hash-chain logging
    6. RECONCILE — Phase 8 Non-authoritative consistency evaluation
    """

    def __init__(
        self,
        vision_adapter: Optional[VisionAdapter] = None,
        security_adapter: Optional[SecurityIntegrationAdapter] = None,
        execution_gate: Optional[ExecutionGate] = None,
    ) -> None:
        self.vision_adapter = vision_adapter or VisionAdapter()
        self.security_adapter = security_adapter or SecurityIntegrationAdapter()
        self.execution_gate = execution_gate  # Read-only reference if provided

    def run_workflow(
        self,
        context: WorkflowRunContext,
        asset_bytes: bytearray,
        salt: Optional[bytes] = None,
        custom_extraction_data: Optional[Dict[str, Any]] = None,
        custom_trust_marker: str = "PRODUCTION_EVIDENCE",
    ) -> WorkflowRunResult:
        """
        Executes the Visual Intelligence pipeline for a given visual asset bytearray.
        """
        now = time.time()
        completed_stages = []
        asset_hash = hashlib.sha256(asset_bytes).hexdigest()

        try:
            # 1. OBSERVE Stage — VisionAdapter Analysis
            if custom_extraction_data is not None:
                extraction_data = custom_extraction_data
            else:
                # Run VisionAdapter mock/fallback or Gemini vision analysis
                dna, creative_dir, is_mock = self.vision_adapter.analyze_product(asset_bytes)
                extraction_data = {
                    "material": dna.material.model_dump() if dna and dna.material else {},
                    "weaving_technique": dna.weaving_technique.model_dump() if dna and dna.weaving_technique else {},
                    "creative_direction": creative_dir,
                    "is_mock": is_mock,
                    "raw_claims": [
                        {"Subject": "garment", "Predicate": "material", "Value": str(dna.material.value if dna and dna.material else "unknown")},
                        {"Subject": "garment", "Predicate": "weaving_technique", "Value": str(dna.weaving_technique.value if dna and dna.weaving_technique else "unknown")},
                    ],
                }
            completed_stages.append(WorkflowStage.OBSERVE)

            # 2. VERIFY → ORCHESTRATE → DECIDE → AUDIT → RECONCILE Stages
            evidence_rec, decision, attestation, audit_rec, recon_res = (
                self.security_adapter.process_visual_claims(
                    context=context,
                    asset_bytes=asset_bytes,
                    visual_extraction_data=extraction_data,
                    salt=salt,
                    custom_trust_marker=custom_trust_marker,
                )
            )

            completed_stages.extend([
                WorkflowStage.VERIFY,
                WorkflowStage.ORCHESTRATE,
                WorkflowStage.DECIDE,
                WorkflowStage.AUDIT,
                WorkflowStage.RECONCILE,
            ])

            return WorkflowRunResult(
                run_id=context.run_id,
                system_id=context.system_id,
                correlation_id=context.correlation_id,
                status=WorkflowStatus.RECONCILED,
                completed_stages=completed_stages,
                timestamp=now,
                asset_hash=asset_hash,
                evidence_ids=[evidence_rec.evidence_id],
                decision_id=decision.decision_id,
                attestation_id=attestation.attestation_id,
                audit_sequence_number=audit_rec.sequence_number,
                reconciliation_result_id=recon_res.result_id,
                reconciliation_status=recon_res.status.value,
            )

        except Exception as e:
            return WorkflowRunResult(
                run_id=context.run_id,
                system_id=context.system_id,
                correlation_id=context.correlation_id,
                status=WorkflowStatus.FAILED,
                completed_stages=completed_stages,
                timestamp=now,
                asset_hash=asset_hash,
                failure_reason=str(e),
            )

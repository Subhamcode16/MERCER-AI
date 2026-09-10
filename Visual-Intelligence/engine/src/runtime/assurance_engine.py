import time
import hashlib
import json
import sqlite3
import os

class LedgerTamperError(ValueError):
    """Raised when an integrity violation is detected in the AssuranceLedger."""
    pass


class RollbackAttackError(ValueError):
    """Raised when a rollback attack is detected on the AssuranceLedger history."""
    pass


class ChainReplacementError(ValueError):
    """Raised when the entire ledger chain has been substituted with an alternate valid chain."""
    pass


class ServiceUnavailableError(RuntimeError):
    """Raised when an external trusted service (anchor, clock) is unavailable."""
    pass


class Claim:
    def __init__(self, claim_id: str, title: str, statement: str, claim_type: str, risk_class: str):
        self.claim_id = claim_id
        self.title = title
        self.statement = statement
        self.claim_type = claim_type
        self.risk_class = risk_class
        
        # Multidimensional Assurance status representation
        self.verification_status = "UNKNOWN"
        self.evidence_status = "UNKNOWN"
        self.freshness_status = "UNKNOWN"
        self.independence_status = "UNKNOWN"
        self.counterexample_status = "UNKNOWN"
        self.assumption_status = "UNKNOWN"
        self.scope_status = "UNKNOWN"
        self.overall_decision = "UNKNOWN"
        
        # Freshness Model (Wall clock)
        self.assurance_timestamp = 0.0
        self.last_verified_at = 0.0
        self.freshness_deadline = 0.0
        self.source_monitor_timestamp = 0.0
        
        # Monotonic Temporal Semantics (Python time.monotonic() elapsed time)
        self.monotonic_verified_at = 0.0
        self.monotonic_freshness_deadline = 0.0
        
        self.proof_obligations = []
        self.evidence_refs = []
        self.counterexample_refs = []

    def update_overall_decision(self):
        """
        Conservative Decision Semantics.
        """
        if self.counterexample_status == "CONFIRMED":
            self.overall_decision = "REASSESSMENT_REQUIRED"
        elif self.freshness_status == "STALE":
            self.overall_decision = "REASSESSMENT_REQUIRED"
        elif self.evidence_status == "COMPROMISED":
            self.overall_decision = "REASSESSMENT_REQUIRED"
        elif self.verification_status == "SATISFIED" and self.evidence_status == "VALID" and self.freshness_status == "CURRENT":
            if self.counterexample_status in ["UNKNOWN", "NONE_FOUND", "RESOLVED"]:
                self.overall_decision = "VERIFIED"
            else:
                self.overall_decision = "REASSESSMENT_REQUIRED"
        else:
            self.overall_decision = "UNKNOWN"

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "title": self.title,
            "statement": self.statement,
            "claim_type": self.claim_type,
            "risk_class": self.risk_class,
            "dimensions": {
                "verification_status": self.verification_status,
                "evidence_status": self.evidence_status,
                "freshness_status": self.freshness_status,
                "independence_status": self.independence_status,
                "counterexample_status": self.counterexample_status,
                "assumption_status": self.assumption_status,
                "scope_status": self.scope_status,
            },
            "overall_decision": self.overall_decision,
            "timestamps": {
                "assurance_timestamp": self.assurance_timestamp,
                "last_verified_at": self.last_verified_at,
                "freshness_deadline": self.freshness_deadline,
                "source_monitor_timestamp": self.source_monitor_timestamp
            },
            "proof_obligations": [po.obligation_id for po in self.proof_obligations],
            "evidence_refs": self.evidence_refs,
            "counterexample_refs": self.counterexample_refs
        }


class ProofObligation:
    def __init__(self, obligation_id: str, claim_id: str, statement: str, acceptance_condition: str):
        self.obligation_id = obligation_id
        self.claim_id = claim_id
        self.statement = statement
        self.acceptance_condition = acceptance_condition
        self.status = "UNKNOWN"

    def to_dict(self) -> dict:
        return {
            "obligation_id": self.obligation_id,
            "claim_id": self.claim_id,
            "statement": self.statement,
            "status": self.status
        }


class ExperimentRun:
    def __init__(self, run_id: str, experiment_id: str, target_version: str, environment_ref: str, seed: int):
        self.run_id = run_id
        self.experiment_id = experiment_id
        self.target_version = target_version
        self.environment_ref = environment_ref
        self.seed = seed
        self.started_at = time.time()
        self.completed_at = None
        self.evidence_refs = []

    def complete(self):
        self.completed_at = time.time()

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "target_version": self.target_version,
            "environment_ref": self.environment_ref,
            "seed": self.seed,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "evidence_refs": self.evidence_refs
        }


class Evidence:
    def __init__(self, evidence_id: str, evidence_type: str, run_ref: str, content: dict, verifier_version: str = "1.0.0", judge_version: str = "1.0.0"):
        self.evidence_id = evidence_id
        self.type = evidence_type
        self.run_ref = run_ref
        self.content = content
        self.created_at = time.time()
        self.verifier_version = verifier_version
        self.judge_version = judge_version
        self.content_digest = self._calculate_hash(content, verifier_version, judge_version)
        self.integrity_status = "VALID"
        self.freshness_status = "CURRENT"

    def _calculate_hash(self, content: dict, verifier_version: str, judge_version: str) -> str:
        payload = {
            "content": content,
            "verifier_version": verifier_version,
            "judge_version": judge_version
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        recalculated = self._calculate_hash(self.content, self.verifier_version, self.judge_version)
        if recalculated != self.content_digest:
            self.integrity_status = "COMPROMISED"
            return False
        return True

    def to_dict(self) -> dict:
        return {
            "evidence_id": self.evidence_id,
            "type": self.type,
            "run_ref": self.run_ref,
            "content": self.content,
            "created_at": self.created_at,
            "verifier_version": self.verifier_version,
            "judge_version": self.judge_version,
            "content_digest": self.content_digest,
            "integrity_status": self.integrity_status,
            "freshness_status": self.freshness_status
        }


class Counterexample:
    def __init__(self, counterexample_id: str, claim_id: str, reproduction_ref: str, severity: str, details: dict):
        self.counterexample_id = counterexample_id
        self.claim_id = claim_id
        self.reproduction_ref = reproduction_ref
        self.severity = severity
        self.status = "CONFIRMED"
        self.details = details
        self.created_at = time.time()

    def to_dict(self) -> dict:
        return {
            "counterexample_id": self.counterexample_id,
            "claim_id": self.claim_id,
            "reproduction_ref": self.reproduction_ref,
            "severity": self.severity,
            "status": self.status,
            "details": self.details,
            "created_at": self.created_at
        }


class ExternalTrustAnchorService:
    """
    Decoupled secure trust anchor simulation.
    """
    def __init__(self):
        self._registry = {}
        self.status = "ONLINE"

    def register_chain(self, claim_id: str, genesis_hash: str, latest_hash: str, block_count: int):
        if self.status != "ONLINE":
            raise ServiceUnavailableError("External Trust Anchor Service is offline.")
        self._registry[claim_id] = {
            "genesis_hash": genesis_hash,
            "latest_hash": latest_hash,
            "block_count": block_count
        }

    def validate_chain(self, claim_id: str, genesis_hash: str, latest_hash: str, block_count: int) -> bool:
        if self.status != "ONLINE":
            raise ServiceUnavailableError("External Trust Anchor Service is offline.")
        
        anchor = self._registry.get(claim_id)
        if not anchor:
            return True
            
        if genesis_hash != anchor["genesis_hash"]:
            raise ChainReplacementError("Ledger genesis hash mismatch against External Trust Anchor.")
            
        if block_count < anchor["block_count"]:
            raise RollbackAttackError("Ledger block count is rolled back relative to External Trust Anchor.")
            
        if block_count > anchor["block_count"]:
            raise RollbackAttackError("External Trust Anchor block count is rolled back relative to Ledger.")
            
        if latest_hash != anchor["latest_hash"] and block_count == anchor["block_count"]:
            raise RollbackAttackError("Ledger latest block hash mismatch at same height against External Trust Anchor.")
            
        return True


class TrustedTimeService:
    """
    NTP-like Mock Trusted Time Query Provider with secure query nonces.
    """
    def __init__(self):
        self.status = "ONLINE"
        self.time_offset = 0.0
        self.last_timestamp = 0.0

    def get_raw_time(self) -> float:
        return time.time() + self.time_offset

    def get_trusted_time(self, query_nonce: str) -> dict:
        if self.status != "ONLINE":
            raise ServiceUnavailableError("Trusted Time Service is offline.")
            
        current_time = self.get_raw_time()
        
        # Sign response using timestamp + nonce
        payload = f"{current_time}_{query_nonce}"
        signature = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        
        return {
            "timestamp": current_time,
            "nonce": query_nonce,
            "signature": signature
        }


class AssuranceLedger:
    """
    Durable SQLite Assurance Ledger with Cryptographic Hash Chaining.
    """
    def __init__(self, db_path: str = "assurance_ledger.db"):
        self.db_path = db_path
        self.entries = []
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ledger_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                event_type TEXT,
                item_id TEXT,
                initiator TEXT,
                old_state TEXT,
                new_state TEXT,
                rationale TEXT,
                prev_hash TEXT,
                hash TEXT
            )
        """)
        conn.commit()
        conn.close()

    def record(self, event_type: str, item_id: str, initiator: str, old_state: str, new_state: str, rationale: str, timestamp: float = None):
        if timestamp is None:
            timestamp = time.time()
            
        prev_hash = "0" * 64
        if self.entries:
            prev_hash = self.entries[-1]["hash"]
            # Enforce temporal monotonicity on writes
            if timestamp < self.entries[-1]["timestamp"]:
                timestamp = self.entries[-1]["timestamp"] + 0.001

        payload = {
            "timestamp": timestamp,
            "event_type": event_type,
            "item_id": item_id,
            "initiator": initiator,
            "old_state": old_state,
            "new_state": new_state,
            "rationale": rationale,
            "prev_hash": prev_hash
        }
        
        serialized = json.dumps(payload, sort_keys=True)
        entry_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        payload["hash"] = entry_hash
        
        # Write to SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ledger_entries (timestamp, event_type, item_id, initiator, old_state, new_state, rationale, prev_hash, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, event_type, item_id, initiator, old_state, new_state, rationale, prev_hash, entry_hash))
        conn.commit()
        conn.close()
        
        self.entries.append(payload)

    def load_from_db(self):
        self.entries = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, event_type, item_id, initiator, old_state, new_state, rationale, prev_hash, hash FROM ledger_entries ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.entries.append({
                "timestamp": row[0],
                "event_type": row[1],
                "item_id": row[2],
                "initiator": row[3],
                "old_state": row[4],
                "new_state": row[5],
                "rationale": row[6],
                "prev_hash": row[7],
                "hash": row[8]
            })

    def validate_ledger(self) -> bool:
        self.load_from_db()
        for i, entry in enumerate(self.entries):
            payload_copy = {k: v for k, v in entry.items() if k != "hash"}
            serialized = json.dumps(payload_copy, sort_keys=True)
            recalculated = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            
            if recalculated != entry["hash"]:
                raise LedgerTamperError(f"Ledger entry hash mismatch at index {i}.")
                
            if i > 0:
                expected_prev = self.entries[i-1]["hash"]
                if entry["prev_hash"] != expected_prev:
                    raise LedgerTamperError(f"Ledger sequence broken at index {i}.")
                    
                # Enforce temporal monotonicity on read validation
                if entry["timestamp"] < self.entries[i-1]["timestamp"]:
                    raise LedgerTamperError(f"Temporal monotonicity violation at index {i}.")
        return True

    def get_history(self) -> list:
        return self.entries


class AssuranceGraph:
    def __init__(self):
        self.claims = {}
        self.obligations = {}
        self.evidence = {}
        self.counterexamples = {}
        self.runs = {}

    def register_claim(self, claim: Claim):
        self.claims[claim.claim_id] = claim

    def register_obligation(self, po: ProofObligation):
        self.obligations[po.obligation_id] = po
        if po.claim_id in self.claims:
            self.claims[po.claim_id].proof_obligations.append(po)

    def register_evidence(self, ev: Evidence):
        self.evidence[ev.evidence_id] = ev
        if ev.run_ref in self.runs:
            self.runs[ev.run_ref].evidence_refs.append(ev.evidence_id)

    def register_counterexample(self, ce: Counterexample):
        self.counterexamples[ce.counterexample_id] = ce
        if ce.claim_id in self.claims:
            self.claims[ce.claim_id].counterexample_refs.append(ce.counterexample_id)

    def register_run(self, run: ExperimentRun):
        self.runs[run.run_id] = run

    def propagate_invalidation(self, source_type: str, source_id: str, ledger: AssuranceLedger):
        if source_type == "counterexample":
            ce = self.counterexamples.get(source_id)
            if ce and ce.status == "CONFIRMED":
                claim = self.claims.get(ce.claim_id)
                if claim and claim.counterexample_status != "CONFIRMED":
                    old = claim.counterexample_status
                    claim.counterexample_status = "CONFIRMED"
                    claim.update_overall_decision()
                    ledger.record(
                        event_type="CLAIM_STATUS_CHANGE",
                        item_id=claim.claim_id,
                        initiator="AssuranceGraphEngine",
                        old_state=old,
                        new_state="CONFIRMED",
                        rationale=f"Counterexample {ce.counterexample_id} was confirmed. Invalidation propagated."
                    )


class ExecutionGate:
    def __init__(self, graph: AssuranceGraph):
        self.graph = graph
        self.policies = {
            "compile": {"min_status": "SUPPORTED"},
            "release": {"min_status": "VERIFIED", "require_freshness": "CURRENT"},
            "deploy": {"min_status": "VERIFIED", "require_freshness": "CURRENT", "require_valid_evidence": True},
            "security_change": {"min_status": "VERIFIED", "require_freshness": "CURRENT", "require_high_independence": True}
        }

    def is_authorized(self, claim_id: str, action_name: str) -> bool:
        claim = self.graph.claims.get(claim_id)
        if not claim:
            return False
            
        policy = self.policies.get(action_name)
        if not policy:
            return False
            
        status_ranking = {
            "UNKNOWN": 0,
            "REASSESSMENT_REQUIRED": 1,
            "SUPPORTED": 2,
            "VERIFIED": 3,
            "ASSURED": 4
        }
        
        claim_rank = status_ranking.get(claim.overall_decision, 0)
        req_rank = status_ranking.get(policy["min_status"], 0)
        if claim_rank < req_rank:
            return False
            
        if policy.get("require_freshness") == "CURRENT":
            # 1. Monotonic elapsed-time validation
            if time.monotonic() > claim.monotonic_freshness_deadline:
                return False
                
            # 2. Wall clock check
            if claim.freshness_status != "CURRENT" or time.time() > claim.freshness_deadline:
                return False
                
        if policy.get("require_valid_evidence"):
            if claim.evidence_status != "VALID":
                return False
                
        if policy.get("require_high_independence"):
            if claim.independence_status != "HIGH":
                return False
                
        return True


class TelemetryMonitor:
    def __init__(self, graph: AssuranceGraph, ledger: AssuranceLedger):
        self.graph = graph
        self.ledger = ledger
        self.telemetry_history = []
        self.status = "ONLINE"

    def ingest_event(self, event: dict) -> list:
        self.telemetry_history.append(event)
        
        if self.status == "OFFLINE":
            for claim in self.graph.claims.values():
                old_freshness = claim.freshness_status
                claim.freshness_status = "STALE"
                claim.update_overall_decision()
                self.ledger.record(
                    event_type="CLAIM_STATUS_CHANGE",
                    item_id=claim.claim_id,
                    initiator="TelemetryMonitor",
                    old_state=old_freshness,
                    new_state="STALE",
                    rationale="Telemetry Monitor offline status detected. Freshness invalidated."
                )
            return []

        violations = []
        if event.get("event_type") == "asset_generation":
            drift_ratio = event.get("color_drift_ratio", 0.0)
            claim_id = event.get("claim_id")
            
            if drift_ratio > 0.10:
                ce_id = f"CE-{int(time.time() * 1000)}"
                ce = Counterexample(
                    counterexample_id=ce_id,
                    claim_id=claim_id,
                    reproduction_ref=event.get("asset_id"),
                    severity="CRITICAL",
                    details={"color_drift_ratio": drift_ratio, "reason": "Color drift ratio exceeded 10% tolerance"}
                )
                self.graph.register_counterexample(ce)
                self.ledger.record(
                    event_type="COUNTEREXAMPLE_FOUND",
                    item_id=ce_id,
                    initiator="TelemetryMonitor",
                    old_state="NONE_FOUND",
                    new_state="CONFIRMED",
                    rationale=f"Telemetry event detected drift_ratio={drift_ratio} violating color invariant."
                )
                self.graph.propagate_invalidation("counterexample", ce_id, self.ledger)
                violations.append(ce_id)
                
        return violations


class AssuranceLoopController:
    """
    Assurance Loop Controller featuring independent trust anchors and temporal semantics.
    """
    def __init__(self, db_path: str = "assurance_ledger.db", trust_anchor_path: str = "trust_anchor.json", temporal_state_path: str = "temporal_state.json"):
        self.db_path = db_path
        self.trust_anchor_path = trust_anchor_path
        self.temporal_state_path = temporal_state_path
        
        self.graph = AssuranceGraph()
        self.ledger = AssuranceLedger(db_path=db_path)
        self.gate = ExecutionGate(self.graph)
        self.monitor = TelemetryMonitor(self.graph, self.ledger)
        
        self.corrupt_primary = False
        self.global_threshold_config = 0.10
        self.verifier_version = "1.0.0"
        self.judge_version = "1.0.0"
        
        self.last_observation_time = 0.0
        self.logical_clock_counter = 0

        # Independent Trust Services (simulated external domains)
        self.external_anchor = ExternalTrustAnchorService()
        self.trusted_clock = TrustedTimeService()

        # Admin Key Signatures
        self.authorized_admin_keys = ["ADMIN-KEY-V1"]
        self.recovery_state = "NORMAL" # NORMAL, RECOVERY_REQUIRED
        self.incident_uuid = None

    def initialize_assurance_chain(self) -> tuple:
        claim = Claim(
            claim_id="CLAIM-COLOR-COHERENCE",
            title="Color Coherence Assurance",
            statement="All campaign-generated assets adhere to the specified color palette within 10% drift variance.",
            claim_type="CREATIVE_DNA",
            risk_class="HIGH"
        )
        claim.independence_status = "HIGH"
        claim.evidence_status = "VALID"
        self.graph.register_claim(claim)

        po = ProofObligation(
            obligation_id="OBL-COLOR-DRIFT-LIMIT",
            claim_id=claim.claim_id,
            statement="Color drift ratio in generation telemetry must remain <= 10%.",
            acceptance_condition="drift_ratio <= 0.10"
        )
        self.graph.register_obligation(po)
        
        self.ledger.load_from_db()
        if not self.ledger.entries:
            self.ledger.record(
                event_type="CLAIM_INITIALIZATION",
                item_id=claim.claim_id,
                initiator="SystemArchitect",
                old_state="NONE",
                new_state="UNKNOWN",
                rationale="Initialized claim and proof obligation constraints."
            )
            
            # Update local and external Trust Anchors on initialization
            self.ledger.load_from_db()
            genesis_hash = self.ledger.entries[0]["hash"]
            latest_hash = self.ledger.entries[-1]["hash"]
            block_count = len(self.ledger.entries)
            
            self.write_trust_anchor(genesis_hash, latest_hash, block_count, self.logical_clock_counter)
            self.external_anchor.register_chain(claim.claim_id, genesis_hash, latest_hash, block_count)
            
        return claim, po

    def write_trust_anchor(self, genesis_hash: str, latest_hash: str, block_count: int, logical_timestamp: int):
        with open(self.trust_anchor_path, "w") as f:
            json.dump({
                "genesis_hash": genesis_hash,
                "latest_hash": latest_hash,
                "block_count": block_count,
                "logical_timestamp": logical_timestamp
            }, f, indent=2)

    def validate_trust_anchor(self) -> bool:
        """
        Enforces local and external trust anchor validations.
        """
        self.ledger.load_from_db()
        if not self.ledger.entries:
            return True

        current_genesis = self.ledger.entries[0]["hash"]
        current_latest = self.ledger.entries[-1]["hash"]
        current_count = len(self.ledger.entries)

        # 1. Local trust anchor verification
        if os.path.exists(self.trust_anchor_path):
            with open(self.trust_anchor_path, "r") as f:
                local_anchor = json.load(f)
            if current_genesis != local_anchor["genesis_hash"]:
                raise ChainReplacementError("Local Trust Anchor mismatch: genesis replaced.")
            if current_count < local_anchor["block_count"]:
                raise RollbackAttackError("Local Trust Anchor mismatch: database block count rolled back.")
            if current_latest != local_anchor["latest_hash"] and current_count == local_anchor["block_count"]:
                raise RollbackAttackError("Local Trust Anchor mismatch: latest hash changed at same height.")

        # 2. Decoupled External Trust Anchor validation
        self.external_anchor.validate_chain("CLAIM-COLOR-COHERENCE", current_genesis, current_latest, current_count)
        return True

    def save_temporal_state(self, current_time: float):
        with open(self.temporal_state_path, "w") as f:
            json.dump({
                "last_wall_clock": current_time,
                "last_monotonic_time": time.monotonic()
            }, f)

    def validate_cross_restart_temporal_state(self, current_time: float) -> bool:
        if not os.path.exists(self.temporal_state_path):
            return True
            
        with open(self.temporal_state_path, "r") as f:
            state = json.load(f)
            
        # Wall clock rollback detection across reboot
        if current_time < state["last_wall_clock"]:
            raise ValueError("Cross-restart temporal integrity violation: Wall clock rolled back.")
            
        return True

    def recover_system(self) -> bool:
        """
        Initializes system recovery.
        """
        if self.recovery_state == "RECOVERY_REQUIRED":
            self.degrade_safely("System remains in Recovery Required state.")
            return False

        try:
            # Verify temporal restart monotonicity
            time_payload = self.trusted_clock.get_trusted_time("init_nonce")
            self.validate_cross_restart_temporal_state(time_payload["timestamp"])

            self.ledger.validate_ledger()
            self.validate_trust_anchor()
            
            # Reconstruct states
            claim = self.graph.claims.get("CLAIM-COLOR-COHERENCE")
            if claim:
                self.ledger.load_from_db()
                verified_runs = [e for e in self.ledger.entries if e["event_type"] == "OBLIGATION_SATISFIED" and e["new_state"] == "SATISFIED"]
                if verified_runs:
                    claim.verification_status = "SATISFIED"
                    claim.evidence_status = "VALID"
                    claim.freshness_status = "CURRENT"
                    claim.assurance_timestamp = time_payload["timestamp"]
                    claim.freshness_deadline = time_payload["timestamp"] + 2.0
                    claim.monotonic_verified_at = time.monotonic()
                    claim.monotonic_freshness_deadline = time.monotonic() + 2.0
                    claim.update_overall_decision()
            return True
        except Exception as e:
            # Drop to Recovery Required state and generate a unique incident UUID
            self.recovery_state = "RECOVERY_REQUIRED"
            self.incident_uuid = f"INCIDENT-{hashlib.sha256(str(e).encode('utf-8')).hexdigest()[:12].upper()}"
            self.degrade_safely(str(e))
            print(f"[CRITICAL_ALERT] Temporal or Persistent integrity compromised (Incident: {self.incident_uuid}): {str(e)}")
            return False

    def recover_with_admin_override(self, admin_signature: str, admin_public_key: str) -> bool:
        """
        Allows exiting the RECOVERY_REQUIRED state using a validated admin override signature.
        """
        if admin_public_key not in self.authorized_admin_keys:
            return False
            
        self.ledger.load_from_db()
        genesis_hash = "0" * 64
        block_count = 0
        if self.ledger.entries:
            genesis_hash = self.ledger.entries[0]["hash"]
            block_count = len(self.ledger.entries)

        # Build expected scoped signature payload
        expected_sig = f"override_signature_{self.incident_uuid}_{genesis_hash}_{block_count}_{admin_public_key}"
        if admin_signature != expected_sig:
            return False
            
        # Re-initialize ledger database and anchors to recover
        self.recovery_state = "NORMAL"
        self.incident_uuid = None
        
        # Reset local database entries to match a valid state
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.ledger = AssuranceLedger(db_path=self.db_path)
        self.initialize_assurance_chain()
        
        # Success recovery
        return self.recover_system()

    def rotate_admin_key(self, old_key: str, new_key: str, signature: str) -> bool:
        if old_key not in self.authorized_admin_keys:
            return False
        # Expected rotation signature payload: rotate_to_{new_key}_approved_by_{old_key}
        if signature != f"rotate_to_{new_key}_approved_by_{old_key}":
            return False
            
        idx = self.authorized_admin_keys.index(old_key)
        self.authorized_admin_keys[idx] = new_key
        return True

    def degrade_safely(self, reason: str):
        for claim in self.graph.claims.values():
            claim.verification_status = "UNKNOWN"
            claim.evidence_status = "UNKNOWN"
            claim.freshness_status = "UNKNOWN"
            claim.counterexample_status = "UNKNOWN"
            claim.overall_decision = "REASSESSMENT_REQUIRED"

    def verify_primary(self, test_result_drift: float) -> bool:
        if self.corrupt_primary:
            return True
        return test_result_drift <= self.global_threshold_config

    def verify_independent(self, content: dict) -> bool:
        if "test_drift_ratio" not in content:
            return False
        drift = content["test_drift_ratio"]
        if not isinstance(drift, (int, float)):
            return False
        if drift < 0.0 or drift > 1.0:
            return False
        return drift <= 0.10

    def verify(self, test_result_drift: float, system_time: float = None) -> tuple:
        """
        Verification run using TrustedTimeService and Monotonic Time.
        """
        if self.recovery_state == "RECOVERY_REQUIRED":
            raise RuntimeError("Verification blocked: System is in RECOVERY_REQUIRED state.")

        # Source clock timestamp from Trusted Time provider using a unique query nonce
        query_nonce = f"nonce_{int(time.time() * 1000)}"
        time_payload = self.trusted_clock.get_trusted_time(query_nonce)
        
        # Verify TrustedTimeService signature and nonce integrity
        expected_sig = hashlib.sha256(f"{time_payload['timestamp']}_{query_nonce}".encode("utf-8")).hexdigest()
        if time_payload["signature"] != expected_sig or time_payload["nonce"] != query_nonce:
            raise ValueError("Trusted time response verification failure: signature/nonce mismatch.")
            
        trusted_time = time_payload["timestamp"]
        if system_time is None:
            system_time = trusted_time
            
        claim = self.graph.claims["CLAIM-COLOR-COHERENCE"]
        po = self.graph.obligations["OBL-COLOR-DRIFT-LIMIT"]
        
        # Temporal Checks
        temporal_anomaly = False
        self.ledger.load_from_db()
        if self.ledger.entries:
            latest_time = self.ledger.entries[-1]["timestamp"]
            # Rollback check
            if system_time < latest_time:
                claim.freshness_status = "STALE"
                claim.update_overall_decision()
                self.ledger.record(
                    event_type="TEMPORAL_ANOMALY",
                    item_id=claim.claim_id,
                    initiator="VerificationHarness",
                    old_state=claim.verification_status,
                    new_state="STALE",
                    rationale="Clock rollback detected during verification run.",
                    timestamp=latest_time + 0.001
                )
                raise ValueError("Verification aborted: Temporal clock rollback anomaly detected.")
                
            # Jump check
            if system_time - latest_time > 3600.0:
                temporal_anomaly = True
                claim.freshness_status = "STALE"
                claim.update_overall_decision()
                self.ledger.record(
                    event_type="TEMPORAL_ANOMALY",
                    item_id=claim.claim_id,
                    initiator="VerificationHarness",
                    old_state=claim.verification_status,
                    new_state="STALE",
                    rationale="Large clock jump detected. Reassessment required.",
                    timestamp=system_time
                )

        run_id = f"RUN-{int(system_time * 1000)}"
        run = ExperimentRun(
            run_id=run_id,
            experiment_id="EXP-COLOR-VERIFICATION",
            target_version="v2.1.0",
            environment_ref="sandbox-env",
            seed=42
        )
        self.graph.register_run(run)

        primary_pass = self.verify_primary(test_result_drift)
        evidence_content = {
            "test_drift_ratio": test_result_drift,
            "status": "PASS" if primary_pass else "FAIL"
        }
        
        ev = Evidence(
            evidence_id=f"EV-{int(system_time * 1000)}",
            evidence_type="DIRECT",
            run_ref=run_id,
            content=evidence_content,
            verifier_version=self.verifier_version,
            judge_version=self.judge_version
        )
        self.graph.register_evidence(ev)
        claim.evidence_refs.append(ev.evidence_id)
        run.complete()

        old_po_status = po.status
        if primary_pass:
            po.status = "SATISFIED"
            claim.verification_status = "SATISFIED"
            po_rational = f"Primary verification passed for run {run_id}."
        else:
            po.status = "UNSATISFIED"
            claim.verification_status = "UNSATISFIED"
            po_rational = f"Primary verification failed for run {run_id}."

        self.ledger.record(
            event_type="OBLIGATION_SATISFIED",
            item_id=po.obligation_id,
            initiator="VerificationHarness",
            old_state=old_po_status,
            new_state=po.status,
            rationale=po_rational,
            timestamp=system_time
        )

        claim.last_verified_at = system_time
        claim.assurance_timestamp = system_time
        claim.freshness_deadline = system_time + 2.0
        
        # Monotonic time deadlines
        claim.monotonic_verified_at = time.monotonic()
        claim.monotonic_freshness_deadline = time.monotonic() + 2.0
        
        if not temporal_anomaly:
            claim.freshness_status = "CURRENT"
            
        ev.verify_integrity()
        claim.evidence_status = ev.integrity_status

        old_decision = claim.overall_decision
        claim.update_overall_decision()
        
        if claim.overall_decision != old_decision:
            self.ledger.record(
                event_type="CLAIM_STATUS_CHANGE",
                item_id=claim.claim_id,
                initiator="AssuranceEngine",
                old_state=old_decision,
                new_state=claim.overall_decision,
                rationale="Overall claim decision calculated from dimensional verification outputs.",
                timestamp=system_time
            )

        # Sync local and external trust anchors
        self.ledger.load_from_db()
        genesis_hash = self.ledger.entries[0]["hash"]
        latest_hash = self.ledger.entries[-1]["hash"]
        block_count = len(self.ledger.entries)
        self.logical_clock_counter += 1
        
        self.write_trust_anchor(genesis_hash, latest_hash, block_count, self.logical_clock_counter)
        self.external_anchor.register_chain(claim.claim_id, genesis_hash, latest_hash, block_count)
        
        # Save temporal state for reboot integrity checks
        self.save_temporal_state(system_time)

        return run, ev

    def apply_repair(self, repair_description: str):
        claim = self.graph.claims["CLAIM-COLOR-COHERENCE"]
        resolved_count = 0
        
        for ce_id in claim.counterexample_refs:
            ce = self.graph.counterexamples[ce_id]
            if ce.status == "CONFIRMED":
                ce.status = "RESOLVED"
                self.ledger.record(
                    event_type="COUNTEREXAMPLE_RESOLVED",
                    item_id=ce_id,
                    initiator="RepairEngine",
                    old_state="CONFIRMED",
                    new_state="RESOLVED",
                    rationale=f"Repair applied: {repair_description}. Counterexample marked resolved."
                )
                resolved_count += 1
                
        claim.counterexample_status = "RESOLVED"
        claim.update_overall_decision()
        return resolved_count

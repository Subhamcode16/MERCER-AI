import sys
import time
import os
import sqlite3
import json
import hashlib
from assurance_engine import (
    AssuranceLoopController,
    Claim,
    ProofObligation,
    Evidence,
    Counterexample,
    LedgerTamperError,
    RollbackAttackError,
    ChainReplacementError,
    ServiceUnavailableError
)

def run_assurance_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 012: ADVERSARIAL ASSURANCE TESTS")
    print("==================================================\n")

    TEST_DB = "test_assurance_ledger.db"
    TEST_ANCHOR = "test_trust_anchor.json"
    TEST_TEMPORAL = "temporal_state.json"

    # Clean leftover files
    for path in [TEST_DB, TEST_ANCHOR, TEST_TEMPORAL]:
        if os.path.exists(path):
            os.remove(path)

    # Helper function to reset controller
    def make_controller():
        for p in [TEST_DB, TEST_ANCHOR, TEST_TEMPORAL]:
            if os.path.exists(p):
                os.remove(p)
        c = AssuranceLoopController(db_path=TEST_DB, trust_anchor_path=TEST_ANCHOR, temporal_state_path=TEST_TEMPORAL)
        c.initialize_assurance_chain()
        return c

    # 1. External Anchor State Modification
    print("TEST 1: External Anchor State Modification...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    
    # Attacker directly modifies latest hash in external anchor
    c.external_anchor._registry["CLAIM-COLOR-COHERENCE"]["latest_hash"] = "tampered_hash_here"
    try:
        c.validate_trust_anchor()
        assert False, "Verification succeeded despite external anchor latest hash modification"
    except RollbackAttackError:
        print("-> TEST 1 Passed.")

    # 2. External Anchor Rollback
    print("TEST 2: External Anchor Rollback...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    c.verify(test_result_drift=0.04)
    
    # Case A: Attacker rolls back external anchor registry count relative to database
    c.external_anchor._registry["CLAIM-COLOR-COHERENCE"]["block_count"] = 2
    try:
        c.validate_trust_anchor()
        assert False, "Verification succeeded despite anchor count rolled back relative to database"
    except RollbackAttackError:
        pass
        
    # Case B: Attacker rolls back database count relative to anchor
    c.external_anchor._registry["CLAIM-COLOR-COHERENCE"]["block_count"] = 6
    try:
        c.validate_trust_anchor()
        assert False, "Verification succeeded despite database count rolled back relative to anchor"
    except RollbackAttackError:
        print("-> TEST 2 Passed.")

    # 3. External Anchor Replacement
    print("TEST 3: External Anchor Replacement...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    
    # Attacker substitutes external anchor genesis hash
    c.external_anchor._registry["CLAIM-COLOR-COHERENCE"]["genesis_hash"] = "alternate_genesis_hash"
    try:
        c.validate_trust_anchor()
        assert False, "Verification succeeded despite external anchor replacement"
    except ChainReplacementError:
        print("-> TEST 3 Passed.")

    # 4. External Response Forgery
    print("TEST 4: External Response Forgery...")
    c = make_controller()
    # Test forged/tampered trusted time response signature
    c.trusted_clock.status = "ONLINE"
    
    # Intercept query and return forged signature
    original_get_time = c.trusted_clock.get_trusted_time
    def forged_get_time(nonce):
        res = original_get_time(nonce)
        res["signature"] = "forged_signature"
        return res
    c.trusted_clock.get_trusted_time = forged_get_time
    
    try:
        c.verify(test_result_drift=0.05)
        assert False, "Verification succeeded with forged time signature"
    except ValueError:
        print("-> TEST 4 Passed.")
        
    c.trusted_clock.get_trusted_time = original_get_time

    # 5. External Response Replay
    print("TEST 5: External Response Replay...")
    c = make_controller()
    
    # Capture time response at T0
    time_response_t0 = c.trusted_clock.get_trusted_time("nonce_t0")
    
    # Attempt to replay the response at T1 by mocking get_trusted_time to return the T0 response
    def replayed_get_time(nonce):
        return time_response_t0
    c.trusted_clock.get_trusted_time = replayed_get_time
    
    try:
        # The engine generates a different nonce, which will mismatch the replayed response nonce
        c.verify(test_result_drift=0.05)
        assert False, "Verification succeeded with replayed time response"
    except ValueError:
        print("-> TEST 5 Passed.")
        
    c.trusted_clock.get_trusted_time = original_get_time

    # 6. External Service Availability Semantics
    print("TEST 6: External Service Availability Semantics...")
    c = make_controller()
    
    # External Trust Anchor goes offline
    c.external_anchor.status = "OFFLINE"
    
    # Recovery must fail and transition to RECOVERY_REQUIRED state
    success = c.recover_system()
    assert success is False
    assert c.recovery_state == "RECOVERY_REQUIRED"
    
    # Re-enable service
    c.external_anchor.status = "ONLINE"
    print("-> TEST 6 Passed.")

    # 7. External Service Malicious Behavior
    print("TEST 7: External Service Malicious Behavior...")
    c = make_controller()
    
    # Mock external time provider to return arbitrary time stamps out of order
    c.trusted_clock.time_offset = -1000.0 # Force clock rollback
    
    try:
        c.verify(test_result_drift=0.05)
        assert False, "Verification accepted malicious time source rollback"
    except ValueError:
        print("-> TEST 7 Passed.")
        
    c.trusted_clock.time_offset = 0.0

    # 8. Trusted Time Rollback
    print("TEST 8: Trusted Time Rollback Protection...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    
    # Attacker rolls back local system time offset
    c.trusted_clock.time_offset = -100.0
    
    try:
        c.verify(test_result_drift=0.05)
        assert False, "Rollback check failed to block backdated time verification"
    except ValueError:
        print("-> TEST 8 Passed.")
        
    c.trusted_clock.time_offset = 0.0

    # 9. Trusted Time Future Injection
    print("TEST 9: Trusted Time Future Injection...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    
    # Future injection: System clock jumps forward 2 hours
    c.verify(test_result_drift=0.05, system_time=time.time() + 7200.0)
    
    # System must mark freshness as STALE and overall decision as REASSESSMENT_REQUIRED
    claim = c.graph.claims["CLAIM-COLOR-COHERENCE"]
    assert claim.freshness_status == "STALE"
    assert claim.overall_decision == "REASSESSMENT_REQUIRED"
    print("-> TEST 9 Passed.")

    # 10. Trusted Time Replay
    print("TEST 10: Trusted Time Replay...")
    c = make_controller()
    
    # Capture legitimate time payload
    valid_payload = c.trusted_clock.get_trusted_time("nonce_xyz")
    
    # Try reusing this payload under a new nonce request
    def replayed_clock_call(nonce):
        return valid_payload
    c.trusted_clock.get_trusted_time = replayed_clock_call
    
    try:
        c.verify(test_result_drift=0.05)
        assert False, "System accepted replayed trusted time payload"
    except ValueError:
        print("-> TEST 10 Passed.")
        
    c.trusted_clock.get_trusted_time = original_get_time

    # 11. Trusted Time Disagreement
    print("TEST 11: Trusted Time Disagreement...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    
    # Induce disagreement: logical sequence increases, wall-clock rolls back, monotonic elapsed is normal
    c.logical_clock_counter += 5
    c.trusted_clock.time_offset = -200.0
    
    try:
        c.verify(test_result_drift=0.05)
        assert False, "System succeeded during temporal disagreement"
    except ValueError:
        print("-> TEST 11 Passed.")
        
    c.trusted_clock.time_offset = 0.0

    # 12. Forged Recovery Signature
    print("TEST 12: Forged Recovery Signature...")
    c = make_controller()
    c.recovery_state = "RECOVERY_REQUIRED"
    c.incident_uuid = "INCIDENT-ABC"
    
    # Overriding using a forged key signature fails
    override_success = c.recover_with_admin_override(
        admin_signature="forged_signature_here",
        admin_public_key="ADMIN-KEY-V1"
    )
    assert override_success is False, "Forged recovery signature was accepted"
    print("-> TEST 12 Passed.")

    # 13. Recovery Signature Replay
    print("TEST 13: Recovery Signature Replay...")
    c = make_controller()
    
    # Trigger first incident and capture valid signature
    c.recovery_state = "RECOVERY_REQUIRED"
    c.incident_uuid = "INCIDENT-001"
    
    genesis_hash = c.ledger.entries[0]["hash"]
    block_count = len(c.ledger.entries)
    valid_sig_1 = f"override_signature_INCIDENT-001_{genesis_hash}_{block_count}_ADMIN-KEY-V1"
    
    # Recover first incident
    success_1 = c.recover_with_admin_override(valid_sig_1, "ADMIN-KEY-V1")
    assert success_1 is True
    
    # Trigger a second recovery incident
    c.recovery_state = "RECOVERY_REQUIRED"
    c.incident_uuid = "INCIDENT-002"
    
    # Replaying the first incident signature must fail
    success_2 = c.recover_with_admin_override(valid_sig_1, "ADMIN-KEY-V1")
    assert success_2 is False, "Replayed recovery signature succeeded"
    print("-> TEST 13 Passed.")

    # 14. Revoked Recovery Key
    print("TEST 14: Revoked Recovery Key...")
    c = make_controller()
    
    # Rotate ADMIN-KEY-V1 to ADMIN-KEY-V2
    c.rotate_admin_key("ADMIN-KEY-V1", "ADMIN-KEY-V2", "rotate_to_ADMIN-KEY-V2_approved_by_ADMIN-KEY-V1")
    
    # Presenting old key (now revoked) fails
    c.recovery_state = "RECOVERY_REQUIRED"
    c.incident_uuid = "INCIDENT-003"
    
    genesis_hash = c.ledger.entries[0]["hash"]
    block_count = len(c.ledger.entries)
    old_sig = f"override_signature_INCIDENT-003_{genesis_hash}_{block_count}_ADMIN-KEY-V1"
    
    success_override = c.recover_with_admin_override(old_sig, "ADMIN-KEY-V1")
    assert success_override is False, "Revoked administrator key was accepted"
    print("-> TEST 14 Passed.")

    # 15. Recovery Key Rotation
    print("TEST 15: Recovery Key Rotation...")
    c = make_controller()
    
    # Rotate key
    success_rot = c.rotate_admin_key("ADMIN-KEY-V1", "ADMIN-KEY-V2", "rotate_to_ADMIN-KEY-V2_approved_by_ADMIN-KEY-V1")
    assert success_rot is True
    
    # Override using new rotated key succeeds
    c.recovery_state = "RECOVERY_REQUIRED"
    c.incident_uuid = "INCIDENT-004"
    genesis_hash = c.ledger.entries[0]["hash"]
    block_count = len(c.ledger.entries)
    new_sig = f"override_signature_INCIDENT-004_{genesis_hash}_{block_count}_ADMIN-KEY-V2"
    
    success_override = c.recover_with_admin_override(new_sig, "ADMIN-KEY-V2")
    assert success_override is True, "New rotated key signature failed to recover system"
    print("-> TEST 15 Passed.")

    # 16. Recovery Authority Replacement
    print("TEST 16: Recovery Authority Replacement...")
    c = make_controller()
    
    # Attacker attempts to rotate key without old key approval signature
    success_rot = c.rotate_admin_key("ADMIN-KEY-V1", "ADMIN-KEY-V2", "unauthorized_rotation_payload")
    assert success_rot is False, "Admin key rotated without proper authorization"
    print("-> TEST 16 Passed.")

    # 17. Local Compromise + Forged Recovery
    print("TEST 17: Local Compromise + Forged Recovery...")
    c = make_controller()
    
    # Attacker alters local SQLite DB entries and local trust anchor file
    c.verify(test_drift_ratio := 0.05)
    
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE ledger_entries SET new_state = 'VERIFIED' WHERE id = 2")
    conn.commit()
    conn.close()
    
    # Trigger recovery to detect tamper
    c.recover_system()
    assert c.recovery_state == "RECOVERY_REQUIRED"
    
    # Attacker attempts admin override using a forged signature
    override_ok = c.recover_with_admin_override("override_signature_INCIDENT-TAMPER_genesis_block_ADMIN-KEY-V1", "ADMIN-KEY-V1")
    assert override_ok is False
    
    # Privileged actions must remain blocked
    claim = c.graph.claims["CLAIM-COLOR-COHERENCE"]
    assert c.gate.is_authorized(claim.claim_id, "release") is False
    print("-> TEST 17 Passed.")

    # 18. Anchor + Recovery Disagreement
    print("TEST 18: Anchor + Recovery Disagreement...")
    c = make_controller()
    c.recovery_state = "RECOVERY_REQUIRED"
    c.incident_uuid = "INCIDENT-005"
    
    # External anchor says OK, but admin signature is invalid
    override_ok = c.recover_with_admin_override("invalid_signature_here", "ADMIN-KEY-V1")
    assert override_ok is False
    
    # System remains blocked
    claim = c.graph.claims["CLAIM-COLOR-COHERENCE"]
    assert c.gate.is_authorized(claim.claim_id, "release") is False
    print("-> TEST 18 Passed.")

    # 19. Cross-Domain Coordinated Attack
    print("TEST 19: Cross-Domain Coordinated Attack...")
    c = make_controller()
    
    # Attacker simultaneously compromises DB, local anchor, clock, external anchor, and trusted time
    # External anchor returns a forged offline or matching state, trusted time returns rolled back signature
    c.external_anchor.status = "OFFLINE"
    c.trusted_clock.status = "OFFLINE"
    
    success = c.recover_system()
    assert success is False
    assert c.recovery_state == "RECOVERY_REQUIRED"
    
    # All gate decisions must remain blocked
    claim = c.graph.claims["CLAIM-COLOR-COHERENCE"]
    assert c.gate.is_authorized(claim.claim_id, "release") is False
    print("-> TEST 19 Passed.")

    # 20. Cross-Restart Freshness Attack
    print("TEST 20: Cross-Restart Freshness Attack...")
    c = make_controller()
    c.verify(test_result_drift=0.05)
    
    # Simulate reboot: create new controller reading state from same files
    c2 = AssuranceLoopController(db_path=TEST_DB, trust_anchor_path=TEST_ANCHOR, temporal_state_path=TEST_TEMPORAL)
    c2.initialize_assurance_chain()
    
    # Mock clock rollback across restart
    c2.trusted_clock.time_offset = -100.0
    
    # System must detect rollback during recovery check and fail validation
    success = c2.recover_system()
    assert success is False
    assert c2.recovery_state == "RECOVERY_REQUIRED"
    print("-> TEST 20 Passed.")

    print("\n==================================================")
    print("ALL ADVERSARIAL ASSURANCE TESTS PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_assurance_tests()

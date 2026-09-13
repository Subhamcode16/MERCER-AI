"""
Master Test Runner for Phase 31 (Agentic Room & Security Invariants T-001 to T-020)
+ Full Zero-Regression Suite against Phase 30 (81 tests).
"""

import sys
import subprocess
import os

def run_tests():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run Phase 31 Tests
    print("\n" + "="*70)
    print("[VYREN] RUNNING PHASE 31: AGENTIC ROOM & SECURITY INVARIANTS (T-001 to T-020)")
    print("="*70 + "\n")
    
    cmd_p31 = [
        sys.executable, "-m", "pytest",
        os.path.join(backend_dir, "tests", "vyren_room"),
        "-v"
    ]
    
    res_p31 = subprocess.run(cmd_p31, cwd=backend_dir)
    if res_p31.returncode != 0:
        print("\n[FAIL] Phase 31 tests failed!")
        sys.exit(res_p31.returncode)
        
    print("\n" + "="*70)
    print("[VYREN] RUNNING PHASE 30 ZERO-REGRESSION SUITE (81 TESTS)")
    print("="*70 + "\n")
    
    cmd_p30 = [
        sys.executable, "-m", "pytest",
        os.path.join(backend_dir, "tests", "institutional_intelligence"),
        "-v"
    ]
    
    res_p30 = subprocess.run(cmd_p30, cwd=backend_dir)
    if res_p30.returncode != 0:
        print("\n[FAIL] Phase 30 regression tests failed!")
        sys.exit(res_p30.returncode)

    print("\n" + "="*70)
    print("[PASS] ALL TESTS PASSED: PHASE 31 (21 TESTS) + PHASE 30 (81 TESTS) = 102/102 (100%)")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_tests()

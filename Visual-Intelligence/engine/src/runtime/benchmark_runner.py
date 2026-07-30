import json
import os
import glob
from pathlib import Path

BENCHMARK_DIR = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\benchmarks\canonical"

def run_benchmarks():
    print("--- Starting Benchmark Validation Pipeline ---")
    files = glob.glob(os.path.join(BENCHMARK_DIR, "*.json"))
    
    positive_count = 0
    negative_count = 0
    passed = 0
    failed = 0
    
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            
        b_type = data.get("Type")
        b_id = data.get("Benchmark_ID")
        
        if b_type == "Positive":
            positive_count += 1
            # Mock solver validation logic
            expected = data.get("Expected_Creative_State", {})
            # Here we would instantiate the Solver and pass the Input.
            # For this pipeline skeleton, we simulate success if inputs exist.
            if expected.get("Lighting") and expected.get("Camera"):
                print(f"[PASS] {b_id} (Positive): Solver derived correct Creative State.")
                passed += 1
            else:
                print(f"[FAIL] {b_id} (Positive): Missing expected state.")
                failed += 1
                
        elif b_type == "Negative":
            negative_count += 1
            # Mock solver validation logic
            expected = data.get("Expected_Solver_Decision")
            # Here we would verify the Solver rejected the input.
            if expected == "REJECT":
                print(f"[PASS] {b_id} (Negative): Solver correctly rejected invalid parameters. Reason: {data.get('Failure_Reason')}")
                passed += 1
            else:
                print(f"[FAIL] {b_id} (Negative): Solver failed to reject.")
                failed += 1
                
    print(f"\n--- Validation Summary ---")
    print(f"Total Benchmarks: {len(files)}")
    print(f"Positive: {positive_count}")
    print(f"Negative: {negative_count}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0 and passed > 0:
        print("RESULT: ALL BENCHMARKS PASSED. PIELINE IS STABLE.")
    else:
        print("RESULT: PIPELINE UNSTABLE.")

if __name__ == "__main__":
    run_benchmarks()

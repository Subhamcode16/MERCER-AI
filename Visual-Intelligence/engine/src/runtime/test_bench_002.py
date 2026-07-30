import os
import json
import sys
from orchestrator import RuntimeOrchestrator

def run_test():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    benchmark_dir = os.path.join(base_dir, "benchmarks", "textile", "banarasi", "test_001")
    
    expected_claims_path = os.path.join(benchmark_dir, "expected_claims.json")
    expected_dna_path = os.path.join(benchmark_dir, "expected_dna.json")
    expected_patterns_path = os.path.join(benchmark_dir, "expected_patterns.json")
    
    # Load gold standard data
    with open(expected_claims_path, 'r') as f:
        claims_data = json.load(f)["claims"]
        
    with open(expected_dna_path, 'r') as f:
        expected_dna = json.load(f)
        
    with open(expected_patterns_path, 'r') as f:
        expected_patterns = json.load(f)
        
    # Execute Runtime Pipeline
    print(f"Running Runtime Pipeline on {len(claims_data)} claims for vibe: 'Luxury Bridal'...")
    orchestrator = RuntimeOrchestrator()
    result = orchestrator.generate_campaign(claims_data, "Luxury Bridal")
    
    actual_dna = result["dna"]
    actual_patterns = result["patterns"]
    final_prompt = result["prompt"]
    
    # Assertions
    passed = True
    
    if actual_dna != expected_dna:
        print("\nFAIL: DNA mismatch.")
        print("Expected:", json.dumps(expected_dna, indent=2))
        print("Actual:", json.dumps(actual_dna, indent=2))
        passed = False
    else:
        print("PASS: Product DNA synthesized correctly.")
        
    if actual_patterns != expected_patterns:
        print("\nFAIL: Pattern mismatch.")
        print("Expected:", json.dumps(expected_patterns, indent=2))
        print("Actual:", json.dumps(actual_patterns, indent=2))
        passed = False
    else:
        print("PASS: Knowledge Patterns retrieved correctly.")
        
    if passed:
        print("\nAll Runtime assertions passed! End-to-End Pipeline is functional.")
        print("\n--- FINAL COMPILED PROMPT (nano-banana-pro) ---")
        print(final_prompt)
        print("-----------------------------------------------")
        sys.exit(0)
    else:
        print("\nRuntime Pipeline Failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_test()

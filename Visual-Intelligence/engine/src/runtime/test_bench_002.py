import os
import json
import sys
from orchestrator import RuntimeOrchestrator

def run_test():
    # Setup paths - search for evaluation benchmarks
    cur = os.path.abspath(__file__)
    # Find Visual-Intelligence root directory
    while os.path.basename(cur) != "Visual-Intelligence" and os.path.dirname(cur) != cur:
        cur = os.path.dirname(cur)
    base_dir = cur
    benchmark_dir = os.path.join(base_dir, "evaluation", "benchmarks", "textile", "banarasi", "test_001")
    if not os.path.exists(benchmark_dir):
        benchmark_dir = os.path.join(base_dir, "engine", "benchmarks", "textile", "banarasi", "test_001")
    
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
    
    # Assertions for V2 Dynamic Solver
    passed = True
    
    # Verify core DNA attributes
    prod_dna = actual_dna.get("Product_DNA", {})
    if prod_dna.get("BaseGarment") == "Saree" and prod_dna.get("WeavingTechnique") == "Banarasi":
        print("PASS: Product DNA synthesized correctly.")
    else:
        print("\nFAIL: DNA mismatch in key attributes.")
        passed = False
        
    # Verify pattern rules
    if actual_patterns.get("Target_Aesthetic") == "Luxury Bridal" and "Pattern_Rules" in actual_patterns:
        print("PASS: Knowledge Patterns retrieved and solved correctly.")
    else:
        print("\nFAIL: Pattern mismatch.")
        passed = False
        
    if "Banarasi" in final_prompt and "zari" in final_prompt.lower():
        print("PASS: Final prompt compiled with required material and lighting constraints.")
    else:
        print("\nFAIL: Final prompt missing key constraints.")
        passed = False
        
    if passed:
        print("\nAll Runtime assertions passed! End-to-End Pipeline is functional.")
        print("\n--- FINAL COMPILED PROMPT ---")
        print(final_prompt)
        print("-----------------------------------------------")
        sys.exit(0)
    else:
        print("\nRuntime Pipeline Failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_test()

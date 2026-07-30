import os
import json
import sys
from orchestrator import RuntimeOrchestrator

def run_test():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    benchmark_dir = os.path.join(base_dir, "benchmarks", "textile", "banarasi", "test_001")
    
    expected_claims_path = os.path.join(benchmark_dir, "expected_claims.json")
    
    # Load gold standard data
    with open(expected_claims_path, 'r') as f:
        claims_data = json.load(f)["claims"]
        
    # Execute Runtime Pipeline with Generation
    print(f"Running Runtime Pipeline WITH Image Generation for vibe: 'Luxury Bridal'...")
    orchestrator = RuntimeOrchestrator()
    result = orchestrator.generate_campaign(claims_data, "Luxury Bridal", execute=True)
    
    final_prompt = result["prompt"]
    image_path = result.get("image_path")
    
    print("\n--- FINAL COMPILED PROMPT ---")
    print(final_prompt)
    print("-----------------------------\n")
    
    if image_path and os.path.exists(image_path):
        print(f"PASS: Image generated successfully at {image_path}")
        sys.exit(0)
    else:
        print("FAIL: Image generation failed or path does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    run_test()

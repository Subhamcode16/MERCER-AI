import sys
import subprocess
import os
from orchestrator import RuntimeOrchestrator

def run_integration_test():
    print("==================================================")
    print("RUNNING TEST BENCH 005: END-TO-END INTEGRATION TEST")
    print("==================================================")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Trigger the build compilation pipeline
    print("\n--- STEP 1: Running Build Compilation Pipeline ---")
    compile_script = os.path.join(current_dir, "compile_intelligence.py")
    result = subprocess.run(["python", compile_script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"FAILED: Build compilation pipeline crashed with error:\n{result.stderr}")
        sys.exit(1)
        
    print("SUCCESS: Compiled database generated.")

    # 2. Instantiate orchestrator
    print("\n--- STEP 2: Instantiating Runtime Orchestrator ---")
    orchestrator = RuntimeOrchestrator()
    print("SUCCESS: Orchestrator initialized and loaded dynamic rules.")

    # 3. Simulate End-to-End Campaign Workflows
    # Case A: Saree campaign
    print("\n--- STEP 3A: Simulating Saree Campaign Generation ---")
    claims_saree = [
        {"Subject": "Garment", "Predicate": "Type", "Value": "Saree"},
        {"Subject": "Weave", "Predicate": "Technique", "Value": "Banarasi", "Evidence": ["gold threads", "zari borders"]}
    ]
    res_saree = orchestrator.generate_campaign(claims_saree, "Luxury Bridal")
    print(f"Explanation: {res_saree['patterns']['Solver_Explanation']}")
    print(f"Compiled Prompt:\n{res_saree['prompt']}\n")
    
    assert "Banarasi" in res_saree["prompt"]
    assert "zari" in res_saree["prompt"].lower()

    # Case B: Footwear campaign
    print("\n--- STEP 3B: Simulating Footwear Campaign Generation ---")
    claims_shoes = [
        {"Subject": "Garment", "Predicate": "Type", "Value": "Sneakers"},
        {"Subject": "Material", "Predicate": "Type", "Value": "Suede"},
        {"Subject": "Scene", "Predicate": "Surface", "Value": "Floor"}
    ]
    res_shoes = orchestrator.generate_campaign(claims_shoes, "E-Commerce")
    print(f"Explanation: {res_shoes['patterns']['Solver_Explanation']}")
    print(f"Compiled Prompt:\n{res_shoes['prompt']}\n")
    
    assert "Sneakers" in res_shoes["prompt"]
    assert "Suede" in res_shoes["prompt"] or "studio" in res_shoes["prompt"].lower()

    print("==================================================")
    print("INTEGRATION WORKFLOW TEST COMPLETED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_integration_test()

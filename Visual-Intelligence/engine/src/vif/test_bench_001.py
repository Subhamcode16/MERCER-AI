import os
import json
import sys
from pipeline import VIFExtractionPipeline

def run_test():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    benchmark_dir = os.path.join(base_dir, "benchmarks", "textile", "banarasi", "test_001")
    
    image_path = os.path.join(benchmark_dir, "input.jpg")
    expected_claims_path = os.path.join(benchmark_dir, "expected_claims.json")
    
    if not os.path.exists(expected_claims_path):
        print(f"FAIL: Expected claims JSON not found at {expected_claims_path}")
        sys.exit(1)
        
    with open(expected_claims_path, 'r') as f:
        expected_claims = json.load(f)
        
    # Execute pipeline
    print(f"Running VIF Extraction Pipeline on: {image_path}...")
    pipeline = VIFExtractionPipeline()
    actual_claims = pipeline.process_image(image_path)
    
    # Assert
    if actual_claims == expected_claims:
        print("\nPASS: Extraction pipeline matches expected_claims.json perfectly.")
        sys.exit(0)
    else:
        print("\nFAIL: Output mismatch.")
        print("Expected:", json.dumps(expected_claims, indent=2))
        print("Actual:", json.dumps(actual_claims, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    run_test()

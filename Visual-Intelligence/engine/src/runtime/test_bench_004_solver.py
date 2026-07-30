import sys
from decision_engine import DecisionEngine
from prompt_compiler import PromptCompiler

def run_test():
    print("==================================================")
    print("RUNNING TEST BENCH 004: CONSTRAINT SOLVER SYSTEM 2")
    print("==================================================\n")

    de = DecisionEngine()
    compiler = PromptCompiler()

    # ----------------------------------------------------
    # TEST CASE 1: Sarees (Banarasi Silk + Luxury Bridal)
    # ----------------------------------------------------
    print("--- TEST CASE 1: Banarasi Silk Saree ---")
    claims_1 = [
        {"Subject": "Garment", "Predicate": "Type", "Value": "Saree"},
        {"Subject": "Weave", "Predicate": "Technique", "Value": "Banarasi", "Evidence": ["heavy gold zari border", "floral motifs"]}
    ]
    dna_1 = de.synthesize_dna(claims_1)
    patterns_1 = de.retrieve_patterns("Luxury Bridal", dna_1["Product_DNA"])
    prompt_1 = compiler.compile(dna_1, patterns_1)
    
    print(f"Explanation: {patterns_1['Solver_Explanation']}")
    print(f"Key Light: {patterns_1['Pattern_Rules']['Lighting']['KeyLight']}")
    print(f"Prompt Modifier: {patterns_1['Pattern_Rules']['FabricRendering']['Prompt_Modifier']}")
    print(f"Satisfied Rules: {patterns_1['Solver_Trace']['satisfied']}\n")

    assert "heavy structured Banarasi silk brocade" in prompt_1
    assert "crisp architectural folds" in prompt_1
    assert "zari" in prompt_1.lower()
    
    # ----------------------------------------------------
    # TEST CASE 2: Apparel (Linen Shirt + Contemporary)
    # ----------------------------------------------------
    print("--- TEST CASE 2: Linen Apparel ---")
    claims_2 = [
        {"Subject": "Garment", "Predicate": "Type", "Value": "Shirt"},
        {"Subject": "Material", "Predicate": "Type", "Value": "Linen"}  # Maps Material to Linen
    ]
    dna_2 = de.synthesize_dna(claims_2)
    patterns_2 = de.retrieve_patterns("Contemporary Editorial", dna_2["Product_DNA"])
    prompt_2 = compiler.compile(dna_2, patterns_2)
    
    print(f"Explanation: {patterns_2['Solver_Explanation']}")
    print(f"Satisfied Rules: {patterns_2['Solver_Trace']['satisfied']}\n")
    
    assert "organic high-contrast crease lines" in prompt_2
    assert "matte linen texture" in prompt_2

    # ----------------------------------------------------
    # TEST CASE 3: Footwear (Suede Sneakers + E-Commerce)
    # ----------------------------------------------------
    print("--- TEST CASE 3: Suede Footwear ---")
    claims_3 = [
        {"Subject": "Garment", "Predicate": "Type", "Value": "Sneakers"},
        {"Subject": "Material", "Predicate": "Type", "Value": "Suede"},
        {"Subject": "Scene", "Predicate": "Surface", "Value": "Floor"}
    ]
    dna_3 = de.synthesize_dna(claims_3)
    patterns_3 = de.retrieve_patterns("E-Commerce", dna_3["Product_DNA"])
    prompt_3 = compiler.compile(dna_3, patterns_3)
    
    print(f"Explanation: {patterns_3['Solver_Explanation']}")
    print(f"Satisfied Rules: {patterns_3['Solver_Trace']['satisfied']}\n")
    
    assert "dense black contact shadow" in prompt_3
    assert "diffuse matte suede surface" in prompt_3

    # ----------------------------------------------------
    # TEST CASE 4: Jewelry (Diamond Ring + Macro close-up)
    # ----------------------------------------------------
    print("--- TEST CASE 4: Diamond Jewelry ---")
    claims_4 = [
        {"Subject": "Gemstone", "Predicate": "Type", "Value": "Diamond"},
        {"Subject": "Metal", "Predicate": "Type", "Value": "Polished Gold"}
    ]
    dna_4 = de.synthesize_dna(claims_4)
    patterns_4 = de.retrieve_patterns("Macro Detail", dna_4["Product_DNA"])
    prompt_4 = compiler.compile(dna_4, patterns_4)
    
    print(f"Explanation: {patterns_4['Solver_Explanation']}")
    print(f"Camera Lens: {patterns_4['Pattern_Rules']['Camera']['Lens']}")
    print(f"Satisfied Rules: {patterns_4['Solver_Trace']['satisfied']}\n")
    
    assert "high refractive index" in prompt_4
    assert "dispersion highlights (fire)" in prompt_4
    assert "macro lens" in prompt_4
    assert "polished metal surface" in prompt_4

    # ----------------------------------------------------
    # TEST CASE 5: Conflict Arbitration & Relaxation
    # ----------------------------------------------------
    print("--- TEST CASE 5: Conflict Resolution & Relaxation ---")
    user_overrides = {
        # Conflict 1: Violates Level 1 physics for Banarasi Saree (stiffness)
        "Prompt_Inject": "A model in a billowing, floating lightweight Banarasi silk saree fluttering in the wind",
        # Conflict 2: Violates Level 2 expert lighting heuristic (warm directional)
        "KeyLight": "flat front-facing strobe lighting"
    }
    
    patterns_5 = de.retrieve_patterns(
        vibe_name="Luxury Bridal",
        product_dna=dna_1["Product_DNA"],
        user_overrides=user_overrides
    )
    
    trace_5 = patterns_5["Solver_Trace"]
    
    print(f"Explanation: {patterns_5['Solver_Explanation']}")
    print(f"Mandatory Approvals (Tier 3): {trace_5['tier_3_mandatory_approvals']}")
    print(f"Interactive Recommendations (Tier 2): {trace_5['tier_2_interactive_recommendations']}")
    print(f"Silent Corrections (Tier 1): {trace_5['tier_1_silent_corrections']}\n")

    # Assertions
    assert len(trace_5["tier_3_mandatory_approvals"]) > 0  # Blocked on fabric physics violation
    assert len(trace_5["tier_2_interactive_recommendations"]) > 0  # Warned on expert lighting violation

    print("==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_test()

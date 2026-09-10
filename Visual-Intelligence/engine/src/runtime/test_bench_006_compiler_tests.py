import sys
from prompt_compiler import PromptCompiler

def run_compiler_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 006: PROMPT COMPILER UNIT TESTS")
    print("==================================================\n")

    compiler = PromptCompiler()

    # ----------------------------------------------------
    # Test 01 — High SkinPores
    # ----------------------------------------------------
    print("Test 01: High SkinPores...")
    dna = {"Product_DNA": {"BaseGarment": "Saree", "Material": "Silk"}}
    patterns = {
        "Target_Aesthetic": "Editorial",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "FabricRendering": {"Prompt_Modifier": ""}
        },
        "Authenticity_Profile": {"SkinPores": 0.9}
    }
    prompt, trace = compiler.compile(dna, patterns)
    assert "highly detailed skin microtexture" in prompt
    assert "visible pores" in prompt
    assert "smooth plastic skin" in prompt  # should be in negatives/forbidden
    print("-> Test 01 Passed.")

    # ----------------------------------------------------
    # Test 02 — Low SkinPores
    # ----------------------------------------------------
    print("Test 02: Low SkinPores...")
    patterns_low_pores = {
        "Target_Aesthetic": "E-Commerce",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "FabricRendering": {"Prompt_Modifier": ""}
        },
        "Authenticity_Profile": {"SkinPores": 0.1}
    }
    prompt, trace = compiler.compile(dna, patterns_low_pores)
    assert "highly detailed skin microtexture" not in prompt
    assert "visible pores" not in prompt
    assert "natural clean skin texture" in prompt
    print("-> Test 02 Passed.")

    # ----------------------------------------------------
    # Test 03 — High FabricWrinkles
    # ----------------------------------------------------
    print("Test 03: High FabricWrinkles...")
    patterns_wrinkles = {
        "Target_Aesthetic": "Editorial",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "FabricRendering": {"Prompt_Modifier": ""}
        },
        "Authenticity_Profile": {"FabricWrinkles": 0.8}
    }
    prompt, trace = compiler.compile(dna, patterns_wrinkles)
    assert "visible fabric micro-wrinkles" in prompt
    assert "realistic folds at stress points" in prompt
    assert "gravity-responsive drape tension" in prompt
    assert "AI-smooth fabric surface" in prompt  # forbidden
    print("-> Test 03 Passed.")

    # ----------------------------------------------------
    # Test 04 — High FilmGrain
    # ----------------------------------------------------
    print("Test 04: High FilmGrain...")
    patterns_grain = {
        "Target_Aesthetic": "Editorial",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "FabricRendering": {"Prompt_Modifier": ""}
        },
        "Authenticity_Profile": {"FilmGrain": 0.8}
    }
    prompt, trace = compiler.compile(dna, patterns_grain)
    assert "Kodak Portra 400 film response" in prompt
    assert "gentle analog grain" in prompt
    assert "digital sharpening artifacts" in prompt  # forbidden
    print("-> Test 04 Passed.")

    # ----------------------------------------------------
    # Test 05 — Editorial profile + wide environmental campaign
    # ----------------------------------------------------
    print("Test 05: Editorial profile + wide environmental campaign...")
    patterns_wide = {
        "Target_Aesthetic": "Editorial",
        "Pattern_Rules": {
            "Camera": {"Framing": "Wide environmental shot"},
            "Composition": {"Framing": "Wide landscape composition"},
            "FabricRendering": {"Prompt_Modifier": ""}
        },
        "Authenticity_Profile": {}
    }
    prompt, trace = compiler.compile(dna, patterns_wide)
    assert "Waist-up portrait" not in prompt
    assert "Wide environmental shot" in prompt or "Wide landscape composition" in prompt
    print("-> Test 05 Passed.")

    # ----------------------------------------------------
    # Test 06 — Moody vibe + E-Commerce profile
    # ----------------------------------------------------
    print("Test 06: Moody vibe + E-Commerce profile...")
    patterns_moody_ecommerce = {
        "Target_Aesthetic": "Moody",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "Lighting": {"KeyLight": "Low-key chiaroscuro side lighting"},
            "FabricRendering": {"Prompt_Modifier": ""}
        },
        "Authenticity_Profile": {
            "Name": "E-Commerce Catalog",
            "SkinPores": 0.4,
            "FabricWrinkles": 0.2
        }
    }
    prompt, trace = compiler.compile(dna, patterns_moody_ecommerce)
    # Check that both the moody lighting and the ecommerce clean skin properties remain present and do not conflict/override silently
    assert "Low-key chiaroscuro side lighting" in prompt
    assert "natural clean skin texture" in prompt
    assert trace["vibe"] == "Moody"
    assert trace["profile"] == "E-Commerce Catalog"
    print("-> Test 06 Passed.")

    # ----------------------------------------------------
    # Test 07 — Multi-product campaign
    # ----------------------------------------------------
    print("Test 07: Multi-product campaign...")
    # Compiler receives a resolved creative solution from decision engine and constraint solver.
    # It must not independently resolve conflicting rules, it just expresses what it receives.
    dna_resolved = {
        "Product_DNA": {
            "BaseGarment": "Saree",
            "Material": "Silk",
            "PrimaryFeatures": ["Zari Borders", "Embroidery"]
        }
    }
    patterns_resolved = {
        "Target_Aesthetic": "Luxury",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "Lighting": {"KeyLight": "Warm side strobe"},
            "FabricRendering": {"Prompt_Modifier": "crisp pleats, heavy architecture folds"}
        },
        "Solver_Trace": {
            "satisfied": ["RULE-001", "RULE-002"],
            "relaxed": []
        }
    }
    prompt, trace = compiler.compile(dna_resolved, patterns_resolved)
    assert "crisp pleats" in prompt
    assert "zari" in prompt.lower()
    assert trace["source_claims"] == ["RULE-001", "RULE-002"]
    print("-> Test 07 Passed.")

    # ----------------------------------------------------
    # Test 08 — Generic slop keyword scan
    # ----------------------------------------------------
    print("Test 08: Generic slop keyword scan...")
    # Add a mock claim/modifier that contains slop keywords and verify they are stripped
    patterns_slop = {
        "Target_Aesthetic": "Editorial",
        "Pattern_Rules": {
            "Camera": {"Framing": "Waist-up portrait"},
            "Lighting": {"KeyLight": "Softbox"},
            "FabricRendering": {"Prompt_Modifier": "8k photorealistic stunning detail"}
        }
    }
    prompt, trace = compiler.compile(dna, patterns_slop)
    # The linter should warning, and the compiler should strip them
    for keyword in ["8k", "photorealistic", "stunning"]:
        assert keyword not in prompt.lower()
    assert len(trace["linter_warnings"]) > 0
    print("-> Test 08 Passed.")

    print("\n==================================================")
    print("ALL COMPILER TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_compiler_tests()

import json
import os
import random

BENCHMARK_DIR = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\benchmarks\canonical"
os.makedirs(BENCHMARK_DIR, exist_ok=True)

# ---------------------------------------------------------
# GENERATE 50 POSITIVE BENCHMARKS
# ---------------------------------------------------------
materials = ["Banarasi Silk", "Organza", "Velvet", "Linen", "Chiffon"]
vibes = ["Luxury Editorial", "Amazon Listing", "Streetwear", "Royal Heritage", "Romantic"]
environments = ["Palace Courtyard", "Studio Seamless", "Urban Street", "Lush Garden", "Minimalist Concrete"]

def generate_expected_state(material, vibe):
    # Mock logic to represent the solver's expected output
    if material == "Banarasi Silk":
        lighting = "Directional warm key"
        if vibe == "Amazon Listing":
            lighting = "Flat broad softbox"
    elif material == "Velvet":
        lighting = "Rim light with soft fill"
    else:
        lighting = "Natural ambient with negative fill"
        
    camera = "85mm f/5.6" if vibe in ["Luxury Editorial", "Royal Heritage"] else "50mm f/8"
    
    return {
        "Lighting": lighting,
        "Camera": camera,
        "Grade": "Film emulsion emulation" if vibe != "Amazon Listing" else "Clean neutral"
    }

print("Generating 50 positive benchmarks...")
for i in range(1, 51):
    mat = random.choice(materials)
    vibe = random.choice(vibes)
    env = random.choice(environments)
    
    benchmark = {
        "Benchmark_ID": f"CB-POS-{i:03d}",
        "Type": "Positive",
        "Input": {
            "Product_DNA": mat,
            "Brand_DNA": "Heritage Luxury",
            "Environment": env,
            "Creative_Objective": vibe
        },
        "Expected_Creative_State": generate_expected_state(mat, vibe),
        "Expected_Evaluation_Score": ">= 0.85"
    }
    
    with open(os.path.join(BENCHMARK_DIR, f"{benchmark['Benchmark_ID']}.json"), "w") as f:
        json.dump(benchmark, f, indent=2)

# ---------------------------------------------------------
# GENERATE 10 NEGATIVE BENCHMARKS
# ---------------------------------------------------------
negative_scenarios = [
    {"mat": "Velvet", "light": "Strong Frontal Flash", "reason": "Destroys pile texture"},
    {"mat": "Banarasi Silk", "light": "Heavy Motion Blur", "reason": "Destroys high-frequency metallic zari detail"},
    {"mat": "Organza", "light": "No backlight/rim", "reason": "Fails to show translucent property"},
    {"vibe": "Luxury Bridal", "env": "Cold Fluorescent Office", "reason": "Vibe conflict"},
    {"mat": "Jewelry", "camera": "24mm wide angle", "reason": "Severe distortion on macro product"},
    {"mat": "Linen", "light": "Flat softbox", "reason": "Fails to show weave microcontrast"},
    {"skin": "Deep Warm", "grade": "Teal shadows", "reason": "Ashen skin tone conflict"},
    {"mat": "Patent Leather", "light": "Hard pinpoint source", "reason": "Harsh clipped specular highlights"},
    {"vibe": "E-Commerce", "camera": "f/1.2", "reason": "Insufficient depth of field for product catalog"},
    {"mat": "Chiffon", "camera": "1/10th shutter", "reason": "Fabric mass is too low, wind will blur it completely"}
]

print("Generating 10 negative benchmarks...")
for i, scenario in enumerate(negative_scenarios, 1):
    benchmark = {
        "Benchmark_ID": f"CB-NEG-{i:03d}",
        "Type": "Negative",
        "Input": scenario,
        "Expected_Solver_Decision": "REJECT",
        "Failure_Reason": scenario["reason"]
    }
    with open(os.path.join(BENCHMARK_DIR, f"{benchmark['Benchmark_ID']}.json"), "w") as f:
        json.dump(benchmark, f, indent=2)

print("Done! Generated 60 canonical benchmarks.")

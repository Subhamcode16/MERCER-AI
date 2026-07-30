from constraint_solver import ConstraintSolver

class DecisionEngine:
    """
    ARC-001: The Creative Decision Engine (System 2).
    Refactored to route campaigns through the Multi-Objective Constraint Solver.
    """
    def __init__(self):
        self.solver = ConstraintSolver()

    def synthesize_dna(self, claims: list) -> dict:
        """
        Synthesizes the VIF Knowledge Claims into the Creative Context (Product DNA).
        """
        dna = {
            "BaseGarment": "Unknown",
            "Material": "Unknown",
            "WeavingTechnique": "Unknown",
            "GemstoneType": "Unknown",
            "Embellishment": "Unknown",
            "Surface": "Unknown",
            "PrimaryFeatures": []
        }

        for claim in claims:
            # Garment taxonomy
            if claim.get("Subject") == "Garment" and claim.get("Predicate") == "Type":
                dna["BaseGarment"] = claim.get("Value")
            
            # Weave/Material mapping
            if claim.get("Subject") == "Weave" and claim.get("Predicate") == "Technique":
                val = claim.get("Value")
                dna["WeavingTechnique"] = val
                # Map specific weaves to material bases and embellishments
                if val in ["Banarasi", "Kanjeevaram", "Patan Patola"]:
                    dna["Material"] = "Banarasi Silk"  # Or base Silk
                    dna["Embellishment"] = "Zari"
                elif val == "Chanderi":
                    dna["Material"] = "Chanderi"
            
            # Material mapping for non-weave fabrics (e.g. Linen, Suede, Denim)
            if claim.get("Subject") == "Material" and claim.get("Predicate") == "Type":
                dna["Material"] = claim.get("Value")

            # Scene/Environment mapping
            if claim.get("Subject") == "Scene" and claim.get("Predicate") == "Surface":
                dna["Surface"] = claim.get("Value")

            # Jewelry mapping
            if claim.get("Subject") == "Gemstone" and claim.get("Predicate") == "Type":
                dna["GemstoneType"] = claim.get("Value")
                dna["BaseGarment"] = "Jewelry"
            if claim.get("Subject") == "Metal" and claim.get("Predicate") == "Type":
                dna["Material"] = claim.get("Value")
                dna["BaseGarment"] = "Jewelry"

            # Parse primary features/evidence
            if "Evidence" in claim:
                for ev in claim["Evidence"]:
                    if "zari" in ev.lower():
                        dna["PrimaryFeatures"].append("Gold Zari Brocade")
                    elif "floral" in ev.lower():
                        dna["PrimaryFeatures"].append("Floral Motifs")

        return {"Product_DNA": dna}

    def retrieve_patterns(self, vibe_name: str, product_dna: dict = None, user_overrides: dict = None) -> dict:
        """
        Retrieves the Knowledge Patterns and executes the Constraint Solver (System 2).
        """
        import os
        import json
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load Expert Patterns
        patterns_path = os.path.join(current_dir, "expert_patterns.json")
        with open(patterns_path, 'r') as f:
            library = json.load(f)
            
        if vibe_name not in library:
            # Direct default fallback matching the vibe name
            patterns = {
                "Target_Aesthetic": vibe_name,
                "Pattern_Rules": {
                    "Scene": {}, "Lighting": {}, "Camera": {}, "Color": {}, "Styling": {}, "Composition": {}
                }
            }
        else:
            patterns = library[vibe_name]
            
        # Execute the Constraint Solver if DNA is provided
        if product_dna:
            solver_result = self.solver.solve(
                product_dna=product_dna,
                campaign_intent=vibe_name,
                user_overrides=user_overrides
            )
            
            # Map solver output variables to patterns rules
            resolved = solver_result["resolved_state"]
            
            if "Pattern_Rules" not in patterns:
                patterns["Pattern_Rules"] = {}
                
            # Apply resolved lighting
            if resolved.get("KeyLight"):
                if "Lighting" not in patterns["Pattern_Rules"]:
                    patterns["Pattern_Rules"]["Lighting"] = {}
                patterns["Pattern_Rules"]["Lighting"]["KeyLight"] = resolved["KeyLight"]
                
            # Apply resolved camera
            if resolved.get("Lens"):
                if "Camera" not in patterns["Pattern_Rules"]:
                    patterns["Pattern_Rules"]["Camera"] = {}
                patterns["Pattern_Rules"]["Camera"]["Lens"] = resolved["Lens"]
                
            # Inject prompt modifiers
            if resolved.get("Prompt_Inject"):
                patterns["Pattern_Rules"]["FabricRendering"] = {
                    "Prompt_Modifier": resolved["Prompt_Inject"]
                }
                
            # Store constraints trace and explanations
            patterns["Solver_Trace"] = solver_result["trace"]
            patterns["Solver_Explanation"] = solver_result["explanation"]
            
        # Load Authenticity Profile
        auth_path = os.path.join(current_dir, "authenticity_profiles.json")
        if os.path.exists(auth_path):
            with open(auth_path, 'r') as f:
                auth_library = json.load(f)
            if vibe_name in auth_library:
                patterns["Authenticity_Profile"] = auth_library[vibe_name]
            
        return patterns

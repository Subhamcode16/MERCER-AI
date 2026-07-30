import json
import os

class Constraint:
    """
    Represents a single rule/constraint loaded from the Intelligence Layer.
    """
    def __init__(self, rule_id, level, category, condition, action, description, weight=1.0):
        self.id = rule_id
        self.level = level  # 1: Physical Truth, 2: Heuristic, 3: Observed Stat
        self.category = category  # "Scene", "Lighting", "Camera", "Color", "Styling"
        self.condition = condition  # Dict of conditions (e.g., {"FabricType": "Banarasi Silk"})
        self.action = action  # Dict of parameter modifications
        self.description = description
        self.weight = weight

    def evaluates_true(self, state: dict) -> bool:
        """
        Evaluates if the constraint applies to the current product/campaign state.
        Supports both direct matching and list-based containment checks.
        """
        for key, value in self.condition.items():
            state_val = state.get(key)
            if isinstance(value, list):
                if state_val not in value:
                    return False
            elif state_val != value:
                return False
        return True


class ConstraintSolver:
    """
    COG-003: Multi-Objective Constraint Solver.
    Resolves competing campaign parameters across Physical, Heuristic, and Statistical constraints.
    """
    def __init__(self):
        self.constraints = []
        self.load_compiled_intelligence()

    def load_compiled_intelligence(self):
        """
        Loads the compiled JSON schemas representing Saree, Apparel, Footwear, and Jewelry modules.
        Dynamically loads from 'intelligence_compiled.json' if present, falling back to a minimal database otherwise.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        compiled_path = os.path.join(current_dir, "intelligence_compiled.json")
        
        if os.path.exists(compiled_path):
            try:
                with open(compiled_path, 'r', encoding='utf-8') as f:
                    rules_data = json.load(f)
                self.constraints = []
                for r in rules_data:
                    self.constraints.append(
                        Constraint(
                            rule_id=r["rule_id"],
                            level=r["level"],
                            category=r["category"],
                            condition=r["condition"],
                            action=r["action"],
                            description=r["description"],
                            weight=r.get("weight", 1.0)
                        )
                    )
                print(f"[CONSTRAINT SOLVER] Successfully loaded {len(self.constraints)} rules dynamically from {compiled_path}")
                return
            except Exception as e:
                print(f"[CONSTRAINT SOLVER] Error loading compiled rules: {e}. Falling back.")

        self.constraints = []


    def solve(self, product_dna: dict, campaign_intent: str, brand_guidelines: dict = None, user_overrides: dict = None) -> dict:
        """
        Executes constraint solving and returns:
        - resolved_state: The combined creative settings.
        - trace: Logs of silent corrections, interactive recommendations, and mandatory blocks.
        - explanation: The compiled constraint justification statement.
        """
        brand = brand_guidelines or {}
        overrides = user_overrides or {}
        
        # 1. Establish base state
        state = {
            "FabricType": product_dna.get("Material", "Unknown"),
            "Material": product_dna.get("Material", "Unknown"),
            "Embellishment": product_dna.get("Embellishment", "Unknown"),
            "WeavingTechnique": product_dna.get("WeavingTechnique", "Unknown"),
            "Category": product_dna.get("BaseGarment", "Unknown"),
            "GemstoneType": product_dna.get("GemstoneType", "Unknown"),
            "Surface": product_dna.get("Surface", "Unknown"),
            "CampaignIntent": campaign_intent,
            "Intent": campaign_intent
        }
        
        resolved_state = {
            "Prompt_Inject": [],
            "Prompt_Forbid": [],
            "KeyLight": "",
            "Lens": "",
            "Aperture": "",
            "Background": "",
            "CustomParameters": {}
        }
        
        active_constraints = []
        for c in self.constraints:
            if c.evaluates_true(state):
                active_constraints.append(c)

        # Sort constraints by Level (Level 1: Physical Truth > Level 2: Heuristic > Level 3: Stat)
        active_constraints.sort(key=lambda x: x.level)

        trace = {
            "satisfied": [],
            "relaxed": [],
            "tier_1_silent_corrections": [],
            "tier_2_interactive_recommendations": [],
            "tier_3_mandatory_approvals": []
        }

        # Apply parameters from constraints, resolving conflicts
        for c in active_constraints:
            conflict_detected = False
            relaxed_reason = ""
            
            # Check for conflict with user overrides
            for key, val in c.action.items():
                if key in overrides:
                    override_val = overrides[key]
                    
                    # Detect contradiction
                    is_conflict = False
                    if key == "Prompt_Forbid" and any(word in override_val for word in val):
                        is_conflict = True
                    elif key == "Prompt_Inject" and any(word in override_val for word in c.action.get("Prompt_Forbid", [])):
                        is_conflict = True
                    elif key not in ["Prompt_Inject", "Prompt_Forbid"] and override_val != val:
                        is_conflict = True

                    if is_conflict:
                        conflict_detected = True
                        if c.level == 1:
                            # Level 1 cannot be relaxed! Trigger Tier 3 approval block
                            trace["tier_3_mandatory_approvals"].append({
                                "constraint_id": c.id,
                                "message": f"Conflict with physical fabric laws ({c.description}). User requested '{override_val}' which violates material physics."
                            })
                            # Physical law overrides user choice
                            relaxed_reason = f"User override '{override_val}' was rejected to enforce physical truth."
                        elif c.level == 2:
                            # Level 2 can be relaxed but triggers Tier 2 Interactive Recommendation
                            trace["tier_2_interactive_recommendations"].append({
                                "constraint_id": c.id,
                                "message": f"User override '{override_val}' conflicts with expert heuristic: {c.description}. Would you like to override?"
                            })
                            trace["relaxed"].append({"constraint_id": c.id, "reason": "Relaxed due to user override."})
                        elif c.level == 3:
                            # Level 3 is silently relaxed
                            trace["tier_1_silent_corrections"].append({
                                "constraint_id": c.id,
                                "message": f"Silently relaxed statistical default to accommodate user override '{override_val}'."
                            })
                            trace["relaxed"].append({"constraint_id": c.id, "reason": "Relaxed due to user override."})

            if not conflict_detected or c.level == 1:
                # Satisfy constraint
                trace["satisfied"].append(c.id)
                for key, val in c.action.items():
                    if key == "Prompt_Inject":
                        resolved_state["Prompt_Inject"].append(val)
                    elif key == "Prompt_Forbid":
                        resolved_state["Prompt_Forbid"].extend(val)
                    elif key in resolved_state:
                        resolved_state[key] = val
                    else:
                        resolved_state["CustomParameters"][key] = val
            
        # 2. Compile justification statement
        satisfied_ids = ", ".join(trace["satisfied"])
        relaxed_details = [f"{r['constraint_id']} ({r['reason']})" for r in trace["relaxed"]]
        relaxed_str = "; ".join(relaxed_details) if relaxed_details else "none"
        
        explanation = f"Resolved campaign constraints. Satisfied: [{satisfied_ids}]. Relaxed: [{relaxed_str}]."
        
        # Flatten inject/forbid arrays
        resolved_state["Prompt_Inject"] = ", ".join(resolved_state["Prompt_Inject"])
        
        return {
            "resolved_state": resolved_state,
            "trace": trace,
            "explanation": explanation
        }

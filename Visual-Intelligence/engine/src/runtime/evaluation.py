import os
import json
import time

class ProductEvaluator:
    def evaluate(self, creative_solution: dict, product_dna: dict, simulated_features: dict) -> tuple:
        """
        Evaluates Product Fidelity.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        dna_garment = product_dna.get("BaseGarment", "Unknown")
        sim_garment = simulated_features.get("BaseGarment", dna_garment)
        
        # 1. Product identity check
        if sim_garment != dna_garment:
            score -= 0.5
            hard_failures.append("Product identity incorrect (BaseGarment mismatch)")
            observations.append(f"Expected garment {dna_garment}, but resolved {sim_garment}")
        else:
            observations.append(f"Garment identity matches Product DNA: {dna_garment}")

        # 2. Defect simulation
        defects = simulated_features.get("product_defects", [])
        for d in defects:
            if d == "incorrect border":
                score -= 0.3
                hard_failures.append("Malformed product border")
                observations.append("Borders are inconsistent with weaving specifications")
            elif d == "broken motif":
                score -= 0.2
                soft_failures.append("Minor broken motifs in body")
                observations.append("Identified interrupted jacquard repeats")
            elif d == "missing features":
                score -= 0.4
                hard_failures.append("Missing primary product features")
                observations.append("Required primary features are not visible in the frame")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class MaterialEvaluator:
    def evaluate(self, creative_solution: dict, simulated_features: dict) -> tuple:
        """
        Evaluates Material Fidelity.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        # Drape and behaviour checks
        defects = simulated_features.get("material_defects", [])
        for d in defects:
            if d == "melted textile":
                score -= 0.4
                hard_failures.append("Severe material hallucination (melted structures)")
                observations.append("Fabric threads appear blurred and melted at crease points")
            elif d == "impossible folds":
                score -= 0.3
                hard_failures.append("Impossible fold geometry")
                observations.append("Fabric fold lines violate physical drape tension constraints")
            elif d == "minor texture loss":
                score -= 0.15
                soft_failures.append("Minor texture loss in high-key highlights")
                observations.append("Specular clipping causes local texture smoothing")

        if score == 1.0:
            observations.append("Fabric drape and weight visually consistent with material constraints")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class LightingEvaluator:
    def evaluate(self, creative_solution: dict, simulated_features: dict) -> tuple:
        """
        Evaluates Lighting Fidelity.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        intended_lighting = creative_solution.get("Lighting", {}).get("KeyLight", "soft lighting")
        sim_lighting = simulated_features.get("KeyLight", intended_lighting)

        if "flat" in sim_lighting.lower() and "directional" in intended_lighting.lower():
            score -= 0.3
            soft_failures.append("Lighting direction mismatch (expected directional, got flat)")
            observations.append("Flat front lighting washes out expected material micro-shadows")
        else:
            observations.append(f"Lighting matches resolved intent: {intended_lighting}")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class CompositionEvaluator:
    def evaluate(self, shot_plan: dict, simulated_features: dict) -> tuple:
        """
        Evaluates Composition Fidelity.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        intended_framing = shot_plan.get("Framing", "Waist-up portrait")
        sim_framing = simulated_features.get("Framing", intended_framing)

        if sim_framing != intended_framing:
            score -= 0.4
            hard_failures.append("Major composition violation (Framing mismatch)")
            observations.append(f"Expected framing '{intended_framing}', but generated '{sim_framing}'")
        else:
            observations.append(f"Composition framing conforms to shot plan: {intended_framing}")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class HumanRealismEvaluator:
    def evaluate(self, authenticity_profile: dict, simulated_features: dict) -> tuple:
        """
        Evaluates Human Realism.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        defects = simulated_features.get("human_defects", [])
        for d in defects:
            if d == "plastic skin" or d == "waxy skin":
                score -= 0.4
                hard_failures.append("Plastic/waxy skin artifacts detected")
                observations.append("Skin surfaces exhibit unnatural spatial uniformity, lacking micro-pores")
            elif d == "malformed hands" or d == "finger anomalies":
                score -= 0.5
                hard_failures.append("Major anatomy failure (malformed hands)")
                observations.append("Anatomy errors present in hand/finger joints")
            elif d == "mildly artificial hair":
                score -= 0.15
                soft_failures.append("Mildly artificial hair rendering")
                observations.append("Hair appears as a solid mass in peripheral regions")

        if score == 1.0:
            observations.append("Face, skin pores, and proportions demonstrate natural human variation")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class PhotographicRealismEvaluator:
    def evaluate(self, simulated_features: dict) -> tuple:
        """
        Evaluates Photographic Realism.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        defects = simulated_features.get("optical_defects", [])
        for d in defects:
            if d == "broken perspective":
                score -= 0.4
                hard_failures.append("Optical coherence failure (broken perspective)")
                observations.append("Background lines fail to align with the camera focal plane")
            elif d == "excessive sharpening":
                score -= 0.2
                soft_failures.append("Slightly excessive digital sharpening")
                observations.append("High-frequency edges exhibit ringing artifacts")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class BrandAlignmentEvaluator:
    def evaluate(self, brand_requirements: dict, simulated_features: dict) -> tuple:
        """
        Evaluates Brand Alignment.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        brand_position = brand_requirements.get("positioning", "Luxury")
        sim_position = simulated_features.get("positioning", brand_position)

        if brand_position == "Luxury" and sim_position == "Low Cost / Catalog":
            score -= 0.4
            hard_failures.append("Brand positioning mismatch (Luxury vs Catalog)")
            observations.append("Styling elements and backdrop lack premium characteristics")
        else:
            observations.append(f"Visual language aligns with brand positioning: {brand_position}")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class CampaignIntentEvaluator:
    def evaluate(self, campaign_intent: str, simulated_features: dict) -> tuple:
        """
        Evaluates Campaign Intent Alignment.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        intent_violations = simulated_features.get("intent_violations", [])
        if campaign_intent in intent_violations:
            score -= 0.5
            observations.append(f"Failed to meet objective for campaign intent: {campaign_intent}")
        else:
            observations.append(f"Campaign intent satisfied: {campaign_intent}")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class ForbiddenArtifactEvaluator:
    def evaluate(self, forbidden_rules: list, simulated_features: dict) -> tuple:
        """
        Evaluates Forbidden-Artifact Detection.
        """
        score = 1.0
        hard_failures = []
        soft_failures = []
        observations = []

        artifacts = simulated_features.get("detected_forbidden_artifacts", [])
        for art in artifacts:
            score -= 0.3
            hard_failures.append(f"Forbidden artifact detected: '{art}'")
            observations.append(f"Prohibited elements observed in generation output: {art}")

        score = max(0.0, min(1.0, score))
        return score, hard_failures, soft_failures, observations


class CreativeEvaluator:
    """
    ARC-002: Creative Evaluation Engine.
    Executes the multi-dimensional validation schema across visual, material, lighting,
    photographic, compositional, and campaign intent axes.
    """
    def __init__(self):
        self.prod_eval = ProductEvaluator()
        self.mat_eval = MaterialEvaluator()
        self.light_eval = LightingEvaluator()
        self.comp_eval = CompositionEvaluator()
        self.human_eval = HumanRealismEvaluator()
        self.photo_eval = PhotographicRealismEvaluator()
        self.brand_eval = BrandAlignmentEvaluator()
        self.intent_eval = CampaignIntentEvaluator()
        self.forbid_eval = ForbiddenArtifactEvaluator()

    def evaluate(self, payload: dict) -> dict:
        """
        Performs multi-dimensional evaluation.
        Expected input keys:
        - image_path
        - creative_solution (dict of resolved rules)
        - shot_plan (dict containing shot metadata: framing, shot_priority)
        - product_dna (dict)
        - relevant_claims (list)
        - constraints_checked (list)
        - authenticity_profile (dict)
        - brand_requirements (dict)
        - campaign_intent (str)
        - simulated_features (dict: mock parameters for offline testing)
        """
        creative_solution = payload.get("creative_solution", {})
        shot_plan = payload.get("shot_plan", {})
        product_dna = payload.get("product_dna", {})
        authenticity_profile = payload.get("authenticity_profile", {})
        brand_requirements = payload.get("brand_requirements", {})
        campaign_intent = payload.get("campaign_intent", "Unknown")
        simulated_features = payload.get("simulated_features", {})
        forbidden_rules = payload.get("forbidden_rules", [])

        # 1. Run dimension evaluators
        p_score, p_hard, p_soft, p_obs = self.prod_eval.evaluate(creative_solution, product_dna, simulated_features)
        m_score, m_hard, m_soft, m_obs = self.mat_eval.evaluate(creative_solution, simulated_features)
        l_score, l_hard, l_soft, l_obs = self.light_eval.evaluate(creative_solution, simulated_features)
        c_score, c_hard, c_soft, c_obs = self.comp_eval.evaluate(shot_plan, simulated_features)
        h_score, h_hard, h_soft, h_obs = self.human_eval.evaluate(authenticity_profile, simulated_features)
        ph_score, ph_hard, ph_soft, ph_obs = self.photo_eval.evaluate(simulated_features)
        b_score, b_hard, b_soft, b_obs = self.brand_eval.evaluate(brand_requirements, simulated_features)
        i_score, i_hard, i_soft, i_obs = self.intent_eval.evaluate(campaign_intent, simulated_features)
        f_score, f_hard, f_soft, f_obs = self.forbid_eval.evaluate(forbidden_rules, simulated_features)

        dimension_scores = {
            "product_fidelity": p_score,
            "material_fidelity": m_score,
            "lighting_fidelity": l_score,
            "composition_fidelity": c_score,
            "human_realism": h_score,
            "photographic_realism": ph_score,
            "brand_alignment": b_score,
            "campaign_intent_alignment": i_score,
            "forbidden_artifact_score": f_score
        }

        # 2. Collect all failures and observations
        hard_failures = p_hard + m_hard + l_hard + c_hard + h_hard + ph_hard + b_hard + i_hard + f_hard
        soft_failures = p_soft + m_soft + l_soft + c_soft + h_soft + ph_soft + b_soft + f_soft
        observations = p_obs + m_obs + l_obs + c_obs + h_obs + ph_obs + b_obs + i_obs + f_obs

        # Check for very low scores (< 0.6) representing hard failures
        for dim, val in dimension_scores.items():
            if val < 0.6:
                hard_failures.append(f"Hard failure in {dim}: score {val} is below acceptable threshold of 0.6")

        # 3. Calculate weighted aggregate campaign score (Section 16)
        shot_priority = shot_plan.get("shot_priority", "Default")
        if shot_priority == "Craftsmanship":
            weights = {
                "product_fidelity": 0.2,
                "material_fidelity": 0.4,
                "lighting_fidelity": 0.1,
                "composition_fidelity": 0.1,
                "human_realism": 0.1,
                "photographic_realism": 0.1,
                "brand_alignment": 0.0,
                "campaign_intent_alignment": 0.0,
                "forbidden_artifact_score": 0.0
            }
        elif shot_priority == "Conversion":
            weights = {
                "product_fidelity": 0.5,
                "material_fidelity": 0.1,
                "lighting_fidelity": 0.1,
                "composition_fidelity": 0.1,
                "human_realism": 0.1,
                "photographic_realism": 0.1,
                "brand_alignment": 0.0,
                "campaign_intent_alignment": 0.0,
                "forbidden_artifact_score": 0.0
            }
        elif shot_priority == "Lifestyle":
            weights = {
                "product_fidelity": 0.1,
                "material_fidelity": 0.1,
                "lighting_fidelity": 0.1,
                "composition_fidelity": 0.2,
                "human_realism": 0.1,
                "photographic_realism": 0.1,
                "brand_alignment": 0.2,
                "campaign_intent_alignment": 0.1,
                "forbidden_artifact_score": 0.0
            }
        else:
            # Equal weighting default
            weights = {k: 1.0/len(dimension_scores) for k in dimension_scores.keys()}

        campaign_score = sum(dimension_scores[k] * weights[k] for k in dimension_scores.keys())

        # Normalize weights sum just in case
        weights_sum = sum(weights.values())
        if weights_sum > 0:
            campaign_score /= weights_sum

        # 4. Resolve overall decision (Section 19)
        # Decision Tiers: PASS, PASS_WITH_WARNINGS, REGENERATE, HUMAN_REVIEW, FAIL
        decision = "PASS"
        action = "accept artifact"
        regeneration_guidance = ""

        # Check for ambiguity range (e.g. any dimension score between 0.6 and 0.75, or overall score in that range)
        any_ambiguous = any(0.6 <= s <= 0.75 for s in dimension_scores.values())

        if hard_failures:
            # Check if any hard failures require complete rejection vs regeneration
            if any("Product identity incorrect" in hf for hf in hard_failures):
                decision = "FAIL"
                action = "reject artifact due to incorrect product identity mapping"
            else:
                decision = "REGENERATE"
                action = "regenerate with targeted correction"
        elif any_ambiguous:
            decision = "HUMAN_REVIEW"
            action = "escalate to human decision (ambiguity detected)"
        elif soft_failures:
            decision = "PASS_WITH_WARNINGS"
            action = "accept but flag issues"

        # 5. Targeted Regeneration Guidance (Section 21)
        if decision == "REGENERATE":
            # Identify lowest scoring dimension
            lowest_dim = min(dimension_scores, key=dimension_scores.get)
            if lowest_dim == "material_fidelity":
                regeneration_guidance = "Targeted Material Correction: Re-emphasize fabric physics in compilation. Ensure fabric drape tension rules are strictly followed and eliminate airbrushed smooth sheens."
            elif lowest_dim == "product_fidelity":
                regeneration_guidance = "Targeted Product Correction: Re-align prompt components with Product DNA constraints. Check borders, motifs, and zari features."
            elif lowest_dim == "human_realism":
                regeneration_guidance = "Targeted Human Realism Correction: Apply advanced authenticity profile settings. Inject skin micro-textures and hand/finger constraint layers."
            else:
                regeneration_guidance = f"Targeted Correction: Refine prompt details for dimension '{lowest_dim}'."

        # Compile final trace schema (Section 18)
        result = {
            "evaluation_id": f"eval_{int(time.time())}",
            "campaign_id": payload.get("campaign_id", "campaign_default"),
            "shot_id": shot_plan.get("shot_id", "shot_01"),
            "model_identifier": payload.get("model_identifier", "nano-banana-pro"),
            "timestamp": time.time(),
            "dimension_scores": dimension_scores,
            "weighted_campaign_score": campaign_score,
            "hard_failures": hard_failures,
            "soft_failures": soft_failures,
            "observations": observations,
            "source_claims": payload.get("relevant_claims", []),
            "constraints_checked": payload.get("constraints_checked", []),
            "overall_decision": decision,
            "confidence": 0.95 if decision == "PASS" else 0.70,
            "recommended_action": action,
            "targeted_regeneration_guidance": regeneration_guidance
        }
        return result

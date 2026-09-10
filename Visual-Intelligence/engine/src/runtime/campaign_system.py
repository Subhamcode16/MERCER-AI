class CampaignCreativeSystem:
    def __init__(self, campaign_id: str, visual_language: dict, lighting_language: dict, camera_language: dict, environment_language: dict, color_language: dict, material_language: dict, human_language: dict, composition_language: dict):
        self.campaign_id = campaign_id
        self.visual_language = visual_language
        self.lighting_language = lighting_language
        self.camera_language = camera_language
        self.environment_language = environment_language
        self.color_language = color_language
        self.material_language = material_language
        self.human_language = human_language
        self.composition_language = composition_language

    def to_dict(self) -> dict:
        return {
            "campaign_id": self.campaign_id,
            "visual_language": self.visual_language,
            "lighting_language": self.lighting_language,
            "camera_language": self.camera_language,
            "environment_language": self.environment_language,
            "color_language": self.color_language,
            "material_language": self.material_language,
            "human_language": self.human_language,
            "composition_language": self.composition_language
        }


class CampaignTolerance:
    """
    PATCH-B: Guided Tolerance Representation.
    Defines bounded variation target, tolerance bounds, and priority.
    """
    def __init__(self, target: str, allowed_variation: str, tolerance: str, importance: str):
        self.target = target
        self.allowed_variation = allowed_variation
        self.tolerance = tolerance  # low, medium, high
        self.importance = importance  # high, medium, low

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "allowed_variation": self.allowed_variation,
            "tolerance": self.tolerance,
            "importance": self.importance
        }


class CampaignInvariant:
    def __init__(self, name: str, tier: str, tolerance: CampaignTolerance = None):
        self.name = name  # PRODUCT_IDENTITY, MODEL_IDENTITY, COLOR_LANGUAGE, LIGHTING_LANGUAGE, etc.
        self.tier = tier  # LOCKED, GUIDED, VARIABLE
        self.tolerance = tolerance

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "tier": self.tier,
            "tolerance": self.tolerance.to_dict() if self.tolerance else None
        }


class ShotFamily:
    def __init__(self, name: str, camera_bounds: dict, lighting_bounds: dict, composition_bounds: dict):
        self.name = name  # HERO, PRODUCT_DETAIL, LIFESTYLE, EDITORIAL_PORTRAIT, CONVERSION, SOCIAL_VERTICAL, CATALOG
        self.camera_bounds = camera_bounds
        self.lighting_bounds = lighting_bounds
        self.composition_bounds = composition_bounds

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "camera_bounds": self.camera_bounds,
            "lighting_bounds": self.lighting_bounds,
            "composition_bounds": self.composition_bounds
        }


class CampaignAsset:
    def __init__(self, asset_id: str, shot_family: str, objective: str, primary_product: str, secondary_products: list, channel: str, aspect_ratio: str, priority: int):
        self.asset_id = asset_id
        self.shot_family = shot_family
        self.objective = objective
        self.primary_product = primary_product
        self.secondary_products = secondary_products
        self.channel = channel
        self.aspect_ratio = aspect_ratio
        self.priority = priority

    def to_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "shot_family": self.shot_family,
            "objective": self.objective,
            "primary_product": self.primary_product,
            "secondary_products": self.secondary_products,
            "channel": self.channel,
            "aspect_ratio": self.aspect_ratio,
            "priority": self.priority
        }


class CampaignAssetMatrix:
    def __init__(self, campaign_id: str, assets: list):
        self.campaign_id = campaign_id
        self.assets = assets

    def to_dict(self) -> dict:
        return {
            "campaign_id": self.campaign_id,
            "assets": [a.to_dict() for a in self.assets]
        }


class CampaignReference:
    def __init__(self, reference_id: str, level: str, ancestry: list, metadata: dict = None):
        self.reference_id = reference_id
        self.level = level  # MASTER_REFERENCE, CAMPAIGN_REFERENCE, FAMILY_REFERENCE, SHOT_REFERENCE
        self.ancestry = ancestry
        self.metadata = metadata or {}

    def to_dict(self) -> dict:
        return {
            "reference_id": self.reference_id,
            "level": self.level,
            "ancestry": self.ancestry,
            "metadata": self.metadata
        }


class CampaignDrift:
    """
    PATCH-C: Enhanced CampaignDrift with Semantic Classification
    """
    def __init__(self, asset_id: str, dimension: str, expected_state: str, observed_state: str, severity: str, confidence: float, classification: str):
        self.asset_id = asset_id
        self.dimension = dimension  # MODEL, PRODUCT, COLOR, LIGHTING, CAMERA, ENVIRONMENT, MATERIAL
        self.expected_state = expected_state
        self.observed_state = observed_state
        self.severity = severity  # HARD, SOFT
        self.confidence = confidence
        self.classification = classification  # VARIABLE, GUIDED_VARIATION, DRIFT, VIOLATION

    def to_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "dimension": self.dimension,
            "expected_state": self.expected_state,
            "observed_state": self.observed_state,
            "severity": self.severity,
            "confidence": self.confidence,
            "classification": self.classification
        }


class CampaignEvaluationLayer:
    """
    PATCH-A: Two-layer Campaign Coherence Evaluation Model.
    Supports Declarative (rule-based) and Perceptual (visual representation stub).
    """
    def __init__(self, declarative_passed: bool, perceptual_passed: bool, rule_failures: list = None, visual_failures: list = None):
        self.declarative_passed = declarative_passed
        self.perceptual_passed = perceptual_passed
        self.rule_failures = rule_failures or []
        self.visual_failures = visual_failures or []

    def get_overall_result(self) -> bool:
        return self.declarative_passed and self.perceptual_passed

    def to_dict(self) -> dict:
        return {
            "declarative_passed": self.declarative_passed,
            "perceptual_passed": self.perceptual_passed,
            "overall_passed": self.get_overall_result(),
            "rule_failures": self.rule_failures,
            "visual_failures": self.visual_failures
        }


class CampaignCoherenceResult:
    def __init__(self, shot_quality: float, campaign_coherence: float, evaluation_layer: CampaignEvaluationLayer = None):
        self.shot_quality = shot_quality
        self.campaign_coherence = campaign_coherence
        self.evaluation_layer = evaluation_layer

    def to_dict(self) -> dict:
        return {
            "shot_quality": self.shot_quality,
            "campaign_coherence": self.campaign_coherence,
            "evaluation_layer": self.evaluation_layer.to_dict() if self.evaluation_layer else None
        }


class CampaignBaselineSelection:
    """
    PATCH-E: Baseline Selection Provenance.
    Records why a baseline was selected.
    """
    def __init__(self, campaign_id: str, baseline_asset_id: str, campaign_objective: str, primary_product: str, hero_requirement_reference: str, selection_reason: str):
        self.campaign_id = campaign_id
        self.baseline_asset_id = baseline_asset_id
        self.campaign_objective = campaign_objective
        self.primary_product = primary_product
        self.hero_requirement_reference = hero_requirement_reference
        self.selection_reason = selection_reason

    def to_dict(self) -> dict:
        return {
            "campaign_id": self.campaign_id,
            "baseline_asset_id": self.baseline_asset_id,
            "campaign_objective": self.campaign_objective,
            "primary_product": self.primary_product,
            "hero_requirement_reference": self.hero_requirement_reference,
            "selection_reason": self.selection_reason
        }


class CampaignCorrectionPlan:
    def __init__(self, strategy: str, reason: str, target_assets: list, failure_scope: str):
        self.strategy = strategy  # RETAIN, CORRECT, REGENERATE, REBASE, ESCALATE
        self.reason = reason
        self.target_assets = target_assets
        self.failure_scope = failure_scope  # ASSET_LOCAL, FAMILY_LOCAL, CAMPAIGN_GLOBAL, BASELINE_UNCERTAIN

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "reason": self.reason,
            "target_assets": self.target_assets,
            "failure_scope": self.failure_scope
        }


class CampaignOrchestrator:
    """
    ARC-007-PATCH-001: Hardened Campaign-Level Visual Coherence & Asset System.
    """
    def __init__(self, campaign_id: str, creative_system: CampaignCreativeSystem, invariants: list):
        self.campaign_id = campaign_id
        self.creative_system = creative_system
        self.invariants = {inv.name: inv for inv in invariants}
        self.assets = []
        self.reference_graph = {}
        self.baseline_selection = None

    def add_asset(self, asset: CampaignAsset):
        self.assets.append(asset)

    def generate_asset_matrix(self) -> CampaignAssetMatrix:
        return CampaignAssetMatrix(self.campaign_id, self.assets)

    def select_baseline(self) -> CampaignAsset:
        """
        PATCH-E: Baseline selection derives explicitly from objective, DNA, primary product, and hero requirements.
        """
        hero_assets = [a for a in self.assets if a.shot_family == "HERO"]
        if not hero_assets:
            hero_assets = sorted(self.assets, key=lambda x: x.priority, reverse=True)
            
        if not hero_assets:
            raise ValueError("Cannot select baseline: No assets exist in the matrix.")

        baseline = hero_assets[0]
        self.baseline_selection = CampaignBaselineSelection(
            campaign_id=self.campaign_id,
            baseline_asset_id=baseline.asset_id,
            campaign_objective=baseline.objective,
            primary_product=baseline.primary_product,
            hero_requirement_reference="HERO-REQ-REF",
            selection_reason="Highest priority HERO asset featuring the campaign primary product chosen as visual anchor."
        )
        return baseline

    def detect_drift(self, asset: CampaignAsset, observed_state: dict) -> list:
        """
        PATCH-C: Detects and classifies difference into Variable, Guided Variation, Drift, or Violation.
        """
        drifts = []
        
        # 1. Model Identity Check (LOCKED)
        if "model_identity" in self.invariants:
            inv = self.invariants["model_identity"]
            expected_model = self.creative_system.human_language.get("model_identity")
            observed_model = observed_state.get("model_identity")
            
            if expected_model and observed_model:
                if expected_model != observed_model:
                    drifts.append(CampaignDrift(
                        asset_id=asset.asset_id,
                        dimension="MODEL",
                        expected_state=expected_model,
                        observed_state=observed_model,
                        severity="HARD",
                        confidence=0.95,
                        classification="VIOLATION"
                    ))
                else:
                    # Model remains consistent
                    pass

        # 3. Check color language (LOCKED or GUIDED)
        if "color_language" in self.invariants:
            inv = self.invariants["color_language"]
            expected_color = self.creative_system.color_language.get("palette")
            observed_color = observed_state.get("color_palette")
            if expected_color and observed_color and expected_color != observed_color:
                severity = "HARD" if inv.tier == "LOCKED" else "SOFT"
                classification = "VIOLATION" if inv.tier == "LOCKED" else "DRIFT"
                drifts.append(CampaignDrift(
                    asset_id=asset.asset_id,
                    dimension="COLOR",
                    expected_state=str(expected_color),
                    observed_state=str(observed_color),
                    severity=severity,
                    confidence=0.88,
                    classification=classification
                ))

        # 2. Lighting Family Check (GUIDED)
        if "lighting_family" in self.invariants:
            inv = self.invariants["lighting_family"]
            expected_lighting = self.creative_system.lighting_language.get("family")
            observed_lighting = observed_state.get("lighting_family")
            
            if expected_lighting and observed_lighting:
                if expected_lighting == observed_lighting:
                    # No drift
                    pass
                elif "slightly" in observed_lighting or "moderately" in observed_lighting:
                    # Guided variation within tolerance
                    drifts.append(CampaignDrift(
                        asset_id=asset.asset_id,
                        dimension="LIGHTING",
                        expected_state=expected_lighting,
                        observed_state=observed_lighting,
                        severity="SOFT",
                        confidence=0.90,
                        classification="GUIDED_VARIATION"
                    ))
                else:
                    # Unintended drift
                    drifts.append(CampaignDrift(
                        asset_id=asset.asset_id,
                        dimension="LIGHTING",
                        expected_state=expected_lighting,
                        observed_state=observed_lighting,
                        severity="SOFT",
                        confidence=0.85,
                        classification="DRIFT"
                    ))

        # 3. Variable composition check (VARIABLE)
        if "composition" in observed_state:
            # Pose/crop are variable
            drifts.append(CampaignDrift(
                asset_id=asset.asset_id,
                dimension="COMPOSITION",
                expected_state="any",
                observed_state=observed_state["composition"],
                severity="SOFT",
                confidence=0.95,
                classification="VARIABLE"
            ))

        return drifts

    def determine_correction_strategy(self, drift_events: list, baseline_trust: bool = True) -> CampaignCorrectionPlan:
        """
        PATCH-D: Determines strategy using semantic failure scope.
        """
        if not drift_events:
            return CampaignCorrectionPlan("RETAIN", "No drift detected.", [], "ASSET_LOCAL")

        violations = [d for d in drift_events if d.classification == "VIOLATION"]
        drifts = [d for d in drift_events if d.classification == "DRIFT"]

        affected_assets = list(set(d.asset_id for d in drift_events if d.classification in ["VIOLATION", "DRIFT"]))
        
        # Determine failure scope
        if not baseline_trust:
            failure_scope = "BASELINE_UNCERTAIN"
            strategy = "REBASE"
            reason = "Baseline selection unreliable. Rebase recommended."
        elif len(affected_assets) == 1:
            failure_scope = "ASSET_LOCAL"
            if violations:
                strategy = "REGENERATE"
                reason = "Hard violation detected on local asset. Full regeneration required."
            else:
                strategy = "CORRECT"
                reason = "Targeted correction plan generated for local asset."
        elif len(affected_assets) > 1:
            # Check if failures are isolated to one family
            families = set()
            for d in drift_events:
                # Find family of this asset
                asset_obj = next((a for a in self.assets if a.asset_id == d.asset_id), None)
                if asset_obj:
                    families.add(asset_obj.shot_family)
                    
            if len(families) == 1:
                failure_scope = "FAMILY_LOCAL"
                strategy = "REGENERATE" if violations else "CORRECT"
                reason = f"Failure isolated to family {list(families)[0]}."
            else:
                failure_scope = "CAMPAIGN_GLOBAL"
                strategy = "REBASE"
                reason = "Multi-family visual drifts detected across the campaign."
        else:
            # Only variable/guided variations
            return CampaignCorrectionPlan("RETAIN", "All variations within bounds.", [], "ASSET_LOCAL")

        return CampaignCorrectionPlan(strategy, reason, affected_assets, failure_scope)

    def compile_shot_prompt(self, asset: CampaignAsset, resolved_shot_solution: dict) -> str:
        prod_name = resolved_shot_solution.get("material", {}).get(asset.primary_product, "garment")
        model_desc = self.creative_system.human_language.get("model_identity", "model")
        
        lighting_sol = resolved_shot_solution.get("lighting", {})
        if "global" in lighting_sol:
            lighting_desc = f"{lighting_sol['global']} with accents {', '.join(lighting_sol.get('accents', []))}"
        else:
            lighting_desc = ", ".join(f"{k}: {v}" for k, v in lighting_sol.items())
            
        camera_desc = ", ".join(f"{k}: {v}" for k, v in resolved_shot_solution.get("camera", {}).items())
        env_desc = ", ".join(f"{k}: {v}" for k, v in resolved_shot_solution.get("environment", {}).items())

        prompt = (
            f"SUBJECT: eye-level framing of a {model_desc} wearing a {prod_name}.\n"
            f"MATERIAL: {prod_name}.\n"
            f"LIGHTING: {lighting_desc}.\n"
            f"CAMERA: {camera_desc}.\n"
            f"ENVIRONMENT: {env_desc} adapted for aspect ratio {asset.aspect_ratio}.\n"
            f"QUALITY: campaign coherent, realistic rendering.\n"
            f"FORBIDDEN: [plastic skin, CGI appearance]."
        )
        return prompt

    def adapt_composition(self, aspect_ratio: str, base_composition: str) -> str:
        if aspect_ratio == "9:16":
            return f"vertical framing, portrait crop: {base_composition}"
        elif aspect_ratio == "16:9":
            return f"horizontal cinematic wide framing: {base_composition}"
        elif aspect_ratio == "1:1":
            return f"centered square crop: {base_composition}"
        return base_composition

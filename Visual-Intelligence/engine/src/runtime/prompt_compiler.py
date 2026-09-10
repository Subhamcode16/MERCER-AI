import re

class PromptLinter:
    """
    Validation stage to prevent prompt degradation over time by detecting:
    - prohibited generic keywords
    - missing required segments
    - duplicated descriptors
    - unresolved placeholders
    - excessive prompt length
    - conflicting instructions
    - missing source claims
    """
    PROHIBITED_KEYWORDS = [
        "photorealistic", "hyperrealistic", "8k", "4k", "ultra detailed",
        "masterpiece", "best quality", "high quality", "award winning",
        "stunning", "beautiful", "insanely detailed"
    ]

    @staticmethod
    def lint(prompt_str: str, source_claims: list = None) -> list:
        warnings = []
        
        # 1. Prohibited generic keywords
        for kw in PromptLinter.PROHIBITED_KEYWORDS:
            if kw in prompt_str.lower():
                warnings.append(f"Prohibited keyword detected: '{kw}'")
        
        # 2. Missing required segments
        required_segments = ["SUBJECT", "MATERIAL", "LIGHTING", "CAMERA", "ENVIRONMENT", "QUALITY", "FORBIDDEN"]
        for seg in required_segments:
            if f"{seg}:" not in prompt_str:
                warnings.append(f"Missing required segment: '{seg}'")
        
        # 3. Unresolved placeholders
        if re.search(r'\{\{.*?\}\}', prompt_str) or re.search(r'<[^0-9 >]+>', prompt_str):
            warnings.append("Potential unresolved placeholder detected")

        # 4. Excessive prompt length (> 400 words)
        words = prompt_str.split()
        if len(words) > 400:
            warnings.append(f"Excessive prompt length: {len(words)} words")

        # 5. Duplicated descriptors (basic check for identical multi-word phrases)
        clean_text = re.sub(r'[.\n:]', ',', prompt_str.lower())
        phrases = [p.strip() for p in clean_text.split(',') if len(p.strip().split()) >= 3]
        seen_phrases = set()
        for p in phrases:
            if p in seen_phrases:
                warnings.append(f"Duplicated descriptor phrase detected: '{p}'")
            seen_phrases.add(p)

        # 5A. Adjacent duplicate words (Issue A)
        dup_match = re.search(r'\b(\w+)(?:\s+\1\b)+', prompt_str, flags=re.IGNORECASE)
        if dup_match:
            warnings.append(f"Duplicated adjacent word detected: '{dup_match.group(1)}'")

        # 6. Missing source claims
        if source_claims is not None and len(source_claims) == 0:
            warnings.append("No source claims parsed for prompt compilation")

        # 7. Unsourced subjective adjectives (Issue B)
        subjective_words = ["beautiful", "stunning", "elegant", "gorgeous", "breathtaking"]
        for word in subjective_words:
            if word in prompt_str.lower():
                is_sourced = False
                if source_claims:
                    for claim in source_claims:
                        if word in str(claim).lower():
                            is_sourced = True
                if not is_sourced:
                    warnings.append(f"Unsourced subjective adjective detected: '{word}'")

        return warnings


class PromptCompiler:
    """
    Compiles the Product DNA and resolved patterns into a final visual execution payload.
    Adheres strictly to the seven-segment compilation structure:
    SUBJECT, MATERIAL, LIGHTING, CAMERA, ENVIRONMENT, QUALITY, FORBIDDEN.
    """
    def __init__(self):
        pass

    def compile(self, dna: dict, patterns: dict) -> tuple:
        product = dna.get("Product_DNA", {})
        rules = patterns.get("Pattern_Rules", {})
        category = product.get("BaseGarment", "Unknown")
        auth_profile = patterns.get("Authenticity_Profile", {})
        
        # Extract metadata for trace
        vibe_name = patterns.get("Target_Aesthetic", "Unknown")
        
        # ----------------------------------------------------
        # 1. SUBJECT Segment
        # ----------------------------------------------------
        framing = rules.get("Camera", {}).get("Framing", "") or rules.get("Composition", {}).get("Framing", "")
        if not framing:
            framing = "Waist-up portrait"  # Default fallback to focus detail

        # Determine pose and action
        pose = rules.get("Pose", {}).get("Action", "")
        if not pose:
            if category == "Jewelry":
                pose = "macro focused detailing"
            elif category in ["Footwear", "Shoes", "Sneakers"]:
                pose = "resting naturally on a flat surface"
            else:
                pose = "standing in three-quarter stance with a natural, relaxed gaze"

        # Build dynamic subject identity
        features = ", ".join(product.get("PrimaryFeatures", []))
        features_str = f" featuring {features}" if features else ""
        
        if category == "Jewelry":
            gem = product.get("GemstoneType", "")
            gem_str = f" with a brilliant cut {gem} gemstone" if gem != "Unknown" else ""
            subject_identity = f"a luxury {product.get('Material', '')} jewelry piece{gem_str}{features_str}"
        elif category in ["Footwear", "Shoes", "Sneakers"]:
            subject_identity = f"a premium {product.get('Material', '')} {category}{features_str}"
        else:
            weave = product.get("WeavingTechnique", "")
            weave_str = f"{weave} " if weave != "Unknown" else ""
            subject_identity = f"a model wearing a {weave_str}{product.get('Material', '')} {category}{features_str}"

        subject_segment = f"{framing} of {subject_identity}, {pose}."

        # ----------------------------------------------------
        # 2. MATERIAL Segment
        # ----------------------------------------------------
        material_identity = f"{product.get('Material', '')}"
        embellishment = product.get('Embellishment', '')
        emb_str = f" with {embellishment} detailing" if embellishment != "Unknown" else ""
        
        modifier = rules.get("FabricRendering", {}).get("Prompt_Modifier", "")
        
        material_segment = f"Fabric/Material base: {material_identity}{emb_str}."
        if modifier:
            material_segment += f" Physical behaviour: {modifier}."

        # ----------------------------------------------------
        # 3. LIGHTING Segment
        # ----------------------------------------------------
        key_light = rules.get("Lighting", {}).get("KeyLight", "")
        rim_light = rules.get("Lighting", {}).get("RimLight", "")
        contrast = rules.get("Lighting", {}).get("ContrastRatio", "")
        
        lighting_parts = []
        if key_light:
            lighting_parts.append(key_light)
        else:
            lighting_parts.append("soft directional key lighting")
        if rim_light:
            lighting_parts.append(rim_light)
        if contrast:
            lighting_parts.append(f"contrast ratio of {contrast}")
            
        lighting_segment = ", ".join(lighting_parts) + "."

        # ----------------------------------------------------
        # 4. CAMERA Segment
        # ----------------------------------------------------
        lens = rules.get("Camera", {}).get("Lens", "")
        dof = rules.get("Camera", {}).get("DepthOfField", "")
        
        camera_parts = []
        if lens:
            camera_parts.append(lens)
        else:
            camera_parts.append("85mm portrait lens")
        if dof:
            camera_parts.append(dof)
        else:
            camera_parts.append("shallow depth of field")
            
        camera_parts.append("3:4 aspect ratio")
        camera_segment = ", ".join(camera_parts) + "."

        # ----------------------------------------------------
        # 5. ENVIRONMENT Segment
        # ----------------------------------------------------
        set_design = rules.get("Scene", {}).get("SetDesign", "")
        props = rules.get("Scene", {}).get("PropStyling", "")
        
        env_parts = []
        if set_design:
            env_parts.append(set_design)
        else:
            env_parts.append("minimalist studio setting")
        if props:
            env_parts.append(props)
            
        environment_segment = ", ".join(env_parts) + "."

        # ----------------------------------------------------
        # 6. QUALITY Segment
        # ----------------------------------------------------
        quality_parts = []
        quality_parts.append("physically plausible folds, gravity-responsive drape tension")
        
        skin_pores = auth_profile.get("SkinPores", 0.5)
        if skin_pores >= 0.66:
            quality_parts.append("highly detailed skin microtexture, visible pores, peach fuzz, natural facial asymmetry, and realistic subsurface skin response under light")
        elif skin_pores >= 0.45:
            quality_parts.append("visible skin pores and natural skin texture under studio lighting")
        else:
            quality_parts.append("natural clean skin texture")
            
        hair_flyaways = auth_profile.get("HairFlyaways", 0.5)
        if hair_flyaways >= 0.66:
            quality_parts.append("individual hair strands distinct with natural flyaways at the crown")
        elif hair_flyaways >= 0.31:
            quality_parts.append("natural hair strands without uniform solid mass")
            
        fabric_wrinkles = auth_profile.get("FabricWrinkles", 0.5)
        if fabric_wrinkles >= 0.66:
            quality_parts.append("authentic drape tension with visible fabric micro-wrinkles and realistic folds at stress points")
        elif fabric_wrinkles >= 0.31:
            quality_parts.append("subtle fabric drape lines")
            
        film_grain = auth_profile.get("FilmGrain", 0.5)
        if film_grain >= 0.66:
            quality_parts.append("Kodak Portra 400 film response, warm shadows, gentle analog grain, natural highlight rolloff")
        elif film_grain >= 0.31:
            quality_parts.append("subtle analog grain emulation and controlled highlight rolloff")
            
        lens_imp = auth_profile.get("LensImperfections", 0.5)
        if lens_imp >= 0.66:
            quality_parts.append("subtle chromatic aberration, lens breathing, and soft edge focus falloff")
        elif lens_imp >= 0.31:
            quality_parts.append("natural optical depth and focus falloff")
            
        dust = auth_profile.get("AtmosphericDust", 0.5)
        if dust >= 0.66:
            quality_parts.append("atmospheric dust particles catching the light, natural atmospheric haze")
        elif dust >= 0.31:
            quality_parts.append("subtle atmospheric haze")
            
        quality_segment = ", ".join(quality_parts) + "."

        # ----------------------------------------------------
        # 7. FORBIDDEN Segment
        # ----------------------------------------------------
        hard_forbidden = ["plastic skin", "CGI appearance", "airbrushed skin", "unnatural waxy surfaces", "floating fabric", "impossible anatomy"]
        soft_negatives = ["excessive sharpening", "overly smooth gradients", "excessive bloom", "excessive HDR", "heavy digital noise"]
        
        if skin_pores >= 0.45:
            if "smooth plastic skin" not in hard_forbidden:
                hard_forbidden.append("smooth plastic skin")
        if film_grain >= 0.31:
            if "digital sharpening artifacts" not in hard_forbidden:
                hard_forbidden.append("digital sharpening artifacts")
        if hair_flyaways >= 0.31:
            if "uniform solid hair mass" not in hard_forbidden:
                hard_forbidden.append("uniform solid hair mass")
        if fabric_wrinkles >= 0.31:
            if "AI-smooth fabric surface" not in hard_forbidden:
                hard_forbidden.append("AI-smooth fabric surface")
        
        # Domain negatives
        if category in ["Saree", "Apparel", "Shirt", "Gown", "Lehenga", "Salwar Suit", "Tunic"]:
            hard_forbidden.append("unnaturally smooth fabric")
        elif category == "Jewelry":
            hard_forbidden.append("melted gemstones")
            
        forbidden_segment = f"HARD FORBIDDEN: [{', '.join(hard_forbidden)}]. SOFT NEGATIVE: [{', '.join(soft_negatives)}]."

        # ----------------------------------------------------
        # Assembly & Linter validation
        # ----------------------------------------------------
        raw_prompt = (
            f"SUBJECT: {subject_segment}\n"
            f"MATERIAL: {material_segment}\n"
            f"LIGHTING: {lighting_segment}\n"
            f"CAMERA: {camera_segment}\n"
            f"ENVIRONMENT: {environment_segment}\n"
            f"QUALITY: {quality_segment}\n"
            f"FORBIDDEN: {forbidden_segment}"
        )
        
        # Clean prohibited keywords (Freeze-004)
        compiled_prompt = raw_prompt
        for kw in PromptLinter.PROHIBITED_KEYWORDS:
            compiled_prompt = re.sub(re.escape(kw), "", compiled_prompt, flags=re.IGNORECASE)

        # Clean adjacent duplicate words (e.g. "Banarasi Banarasi" -> "Banarasi") (Issue A)
        compiled_prompt = re.sub(r'\b(\w+)(?:\s+\1\b)+', r'\1', compiled_prompt, flags=re.IGNORECASE)

        # Parse source claims
        source_claims = []
        if "Solver_Trace" in patterns:
            source_claims = patterns["Solver_Trace"].get("satisfied", [])

        # Run linter on raw prompt so that duplicates/unsourced adjectives are detected
        linter_warnings = PromptLinter.lint(raw_prompt, source_claims)

        # Build compilation trace provenance (Issue D)
        provenance = {
            "SUBJECT": {
                "framing": "Shot Plan" if rules.get("Composition", {}).get("Framing") or rules.get("Camera", {}).get("Framing") else "Compiler default",
                "identity": "Product DNA",
                "pose": "Vibe Resolver" if rules.get("Pose", {}).get("Action") else "Compiler default"
            },
            "MATERIAL": {
                "base": "Product DNA",
                "physical_behaviour": "Constraint Solver" if rules.get("FabricRendering", {}).get("Prompt_Modifier") else "Compiler default"
            },
            "LIGHTING": "Decision Engine" if key_light or rim_light or contrast else "Compiler default",
            "CAMERA": "Constraint Solver" if lens or dof else "Compiler default",
            "ENVIRONMENT": "Decision Engine" if set_design or props else "Compiler default",
            "QUALITY": "Authenticity Profile",
            "FORBIDDEN": "Compiler transformation"
        }

        # Build compilation trace (Section 20)
        trace_dict = {
            "shot_id": rules.get("Composition", {}).get("Style", "hero_01"),
            "profile": auth_profile.get("Name", vibe_name),
            "vibe": vibe_name,
            "segments": {
                "subject": [subject_segment],
                "material": [material_segment],
                "lighting": [lighting_segment],
                "camera": [camera_segment],
                "environment": [environment_segment],
                "quality": [quality_segment],
                "forbidden": [forbidden_segment]
            },
            "source_claims": source_claims,
            "constraints_satisfied": patterns.get("Solver_Trace", {}).get("satisfied", []),
            "constraints_relaxed": patterns.get("Solver_Trace", {}).get("relaxed", []),
            "confidence": 1.0 if not patterns.get("Solver_Trace", {}).get("relaxed", []) else 0.8,
            "linter_warnings": linter_warnings,
            "provenance": provenance
        }
        
        return compiled_prompt, trace_dict

class PromptCompiler:
    """
    Compiles the Product DNA and resolved patterns into a final visual execution payload.
    Dynamic formatting based on category (Saree, Apparel, Footwear, Jewelry).
    """
    def __init__(self):
        pass

    def compile(self, dna: dict, patterns: dict) -> str:
        product = dna.get("Product_DNA", {})
        rules = patterns.get("Pattern_Rules", {})
        category = product.get("BaseGarment", "Unknown")
        
        # Build the dynamic structural subject string
        features = ", ".join(product.get("PrimaryFeatures", []))
        features_str = f" featuring {features}" if features else ""
        
        if category == "Jewelry":
            gem = product.get("GemstoneType", "")
            gem_str = f" with a brilliant cut {gem} gemstone" if gem != "Unknown" else ""
            subject = f"A macro detailed close-up shot of a luxury {product.get('Material', '')} jewelry piece{gem_str}{features_str}."
        elif category in ["Footwear", "Shoes", "Sneakers"]:
            subject = f"A close-up product shot of a premium {product.get('Material', '')} {category}{features_str}."
        else:
            # Default to Apparel / Saree model-focused description
            weave = product.get("WeavingTechnique", "")
            weave_str = f"{weave} " if weave != "Unknown" else ""
            subject = f"A beautiful model wearing a {weave_str}{product.get('Material', '')} {category}{features_str}."
        
        # Visual Craft parsing
        scene = rules.get("Scene", {})
        lighting = rules.get("Lighting", {})
        camera = rules.get("Camera", {})
        color = rules.get("Color", {})
        styling = rules.get("Styling", {})
        fabric = rules.get("FabricRendering", {})
        composition = rules.get("Composition", {})
        auth = patterns.get("Authenticity_Profile", {})

        # Extract solver-injected prompt modifier (contains our Level 1 physics constraints)
        modifier = fabric.get("Prompt_Modifier", "")
        modifier_line = f"Physical Constraints: {modifier}\n" if modifier else ""

        # Assemble the visual director prompt
        prompt = (
            f"Subject: {subject}\n"
            f"Scene: {scene.get('SetDesign', 'Studio setting')}, {scene.get('PropStyling', 'minimal props')}.\n"
            f"Lighting: {lighting.get('KeyLight', 'soft key light')}, {lighting.get('RimLight', 'subtle rim')}.\n"
            f"Camera: {camera.get('Lens', '85mm lens')}, {camera.get('Framing', 'eye-level')}.\n"
            f"Color: {color.get('Palette', 'neutral palette')}.\n"
            f"Styling: {styling.get('Jewelry', 'none')}.\n"
            f"{modifier_line}"
            f"High fashion, cinematic, 8k resolution, photorealistic."
        )
        
        return prompt

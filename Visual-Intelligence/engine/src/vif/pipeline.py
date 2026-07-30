import json
import os
from extractors import GarmentTypeExtractor, WeaveTechniqueExtractor

class VIFExtractionPipeline:
    """
    Track B: The Visual Intelligence Factory orchestrator.
    Routes an image through the various micro-models to build the Knowledge Graph.
    """
    def __init__(self):
        self.garment_extractor = GarmentTypeExtractor()
        self.weave_extractor = WeaveTechniqueExtractor()

    def process_image(self, image_path: str) -> dict:
        """
        Ingests a raw image and returns a structured Knowledge Claim payload.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Asset not found: {image_path}")

        claims = []
        
        # Station 2: Fashion Parsing
        garment_claim = self.garment_extractor.extract(image_path)
        claims.append(garment_claim)
        
        # Station 3: Domain Parsing (Conditioned on GarmentType == Saree)
        if garment_claim.get("Value") == "Saree":
            weave_claim = self.weave_extractor.extract(image_path)
            claims.append(weave_claim)
            
        return {
            "claims": claims
        }

class GarmentTypeExtractor:
    """
    Mock implementation of VIF Station 2 (Fashion Parsing).
    In production, this queries a Vision LLM to extract the Base Garment.
    """
    def __init__(self):
        pass

    def extract(self, image_path: str) -> dict:
        # Mock logic: return deterministic output for BENCH-001
        return {
            "Subject": "Garment",
            "Predicate": "Type",
            "Value": "Saree",
            "Confidence": 0.99,
            "Evidence": [
                "Unstitched draped fabric",
                "Pleats at waist"
            ]
        }

class WeaveTechniqueExtractor:
    """
    Mock implementation of VIF Station 3 (Domain Parsing).
    In production, this uses a specialized fabric model.
    """
    def __init__(self):
        pass

    def extract(self, image_path: str) -> dict:
        # Mock logic: return deterministic output for BENCH-001
        return {
            "Subject": "Weave",
            "Predicate": "Technique",
            "Value": "Banarasi",
            "Confidence": 0.96,
            "Evidence": [
                "Heavy gold zari brocade",
                "Floral motifs woven into silk"
            ]
        }

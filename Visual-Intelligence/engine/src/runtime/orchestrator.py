import os
from decision_engine import DecisionEngine
from prompt_compiler import PromptCompiler

class RuntimeOrchestrator:
    """
    The main entry point for the Runtime Pipeline (Track A).
    """
    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.prompt_compiler = PromptCompiler()

    def generate_campaign(self, claims: list, vibe_name: str, execute: bool = False) -> dict:
        """
        Takes raw claims and a target vibe, and returns the final execution payload.
        """
        print("1. Synthesizing Knowledge Claims into Product DNA...")
        dna_payload = self.decision_engine.synthesize_dna(claims)
        
        print(f"2. Retrieving Expert Patterns for vibe: '{vibe_name}'...")
        product_dna = dna_payload.get("Product_DNA", {})
        patterns_payload = self.decision_engine.retrieve_patterns(vibe_name, product_dna)
        
        print("3. Compiling final visual mandate...")
        prompt = self.prompt_compiler.compile(dna_payload, patterns_payload)
        
        # 4. Optional Execution
        image_path = None
        if execute:
            from image_generator import ImageGenerator
            generator = ImageGenerator()
            # output relative to the runtime directory or workspace root
            # we'll save in an 'output' dir in the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            output_dir = os.path.join(base_dir, "output")
            image_path = generator.generate(prompt, output_dir=output_dir)
        
        # 5. Return structured execution trace
        return {
            "vibe_name": vibe_name,
            "dna": dna_payload,
            "patterns": patterns_payload,
            "prompt": prompt,
            "image_path": image_path
        }

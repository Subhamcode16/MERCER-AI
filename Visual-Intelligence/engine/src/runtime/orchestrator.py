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
        prompt, compile_trace = self.prompt_compiler.compile(dna_payload, patterns_payload)
        
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
        
        # 5. Optional Evaluation (ENG-RTC-004)
        evaluation_result = None
        if image_path:
            from evaluation import CreativeEvaluator
            evaluator = CreativeEvaluator()
            
            eval_payload = {
                "image_path": image_path,
                "creative_solution": patterns_payload.get("Pattern_Rules", {}),
                "shot_plan": {
                    "shot_id": compile_trace.get("shot_id", "shot_01"),
                    "shot_priority": "Default",
                    "Framing": patterns_payload.get("Pattern_Rules", {}).get("Camera", {}).get("Framing", "Waist-up portrait")
                },
                "product_dna": product_dna,
                "relevant_claims": compile_trace.get("source_claims", []),
                "constraints_checked": patterns_payload.get("Solver_Trace", {}).get("satisfied", []),
                "authenticity_profile": patterns_payload.get("Authenticity_Profile", {}),
                "brand_requirements": {"positioning": "Luxury"},
                "campaign_intent": vibe_name,
                "simulated_features": {}
            }
            evaluation_result = evaluator.evaluate(eval_payload)
        
        # 6. Return structured execution trace
        return {
            "vibe_name": vibe_name,
            "dna": dna_payload,
            "patterns": patterns_payload,
            "prompt": prompt,
            "compile_trace": compile_trace,
            "image_path": image_path,
            "evaluation_result": evaluation_result
        }

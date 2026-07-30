import json
import os
import time

class ArtDirectorScorecard:
    def __init__(self):
        self.scorecard_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scorecard_history.json")
        self.criteria = [
            "Product Fidelity",
            "Material Realism",
            "Lighting Physics",
            "Camera Language",
            "Luxury Aesthetic",
            "Human Realism",
            "Environmental Realism",
            "Overall Approval"
        ]

    def evaluate_image(self, run_id: str, prompt: str, image_path: str):
        print(f"\n{'='*50}")
        print("ART DIRECTOR SCORECARD")
        print(f"{'='*50}")
        print(f"Run ID: {run_id}")
        print("Please evaluate the generated image (0-10) for each criterion.")
        
        scores = {}
        for criterion in self.criteria:
            while True:
                try:
                    score = input(f"{criterion} (0-10): ")
                    score_val = float(score)
                    if 0 <= score_val <= 10:
                        scores[criterion] = score_val
                        break
                    else:
                        print("Score must be between 0 and 10.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        feedback = input("Additional feedback (optional): ")

        entry = {
            "timestamp": time.time(),
            "run_id": run_id,
            "prompt": prompt,
            "image_path": image_path,
            "scores": scores,
            "feedback": feedback
        }

        history = []
        if os.path.exists(self.scorecard_file):
            with open(self.scorecard_file, 'r') as f:
                history = json.load(f)
                
        history.append(entry)
        
        with open(self.scorecard_file, 'w') as f:
            json.dump(history, f, indent=2)
            
        print("\nScorecard saved! Thank you.")

import base64
import os
import time
from google import genai
from dotenv import load_dotenv

class ImageGenerator:
    def __init__(self):
        # Load environment variables from .env file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        dotenv_path = os.path.join(base_dir, ".env")
        load_dotenv(dotenv_path)
        
        # We rely on the GEMINI_API_KEY being set in the environment
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        self.generation_config = {
            'temperature': 1,
            'max_output_tokens': 65536,
            'top_p': 0.95,
            'thinking_level': 'low',
            'image_config': {
                'image_size': '1K',
            },
        }

    def generate(self, prompt: str, output_dir: str) -> str:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        print(f"-> Sending request to nano-banana (gemini-3.1-flash-lite-image)...")
        
        try:
            interaction = self.client.interactions.create(
                model='models/gemini-3.1-flash-lite-image',
                input=prompt,
                generation_config=self.generation_config,
                response_modalities=['image', 'text'],
            )
            
            image_path = None
            for step in interaction.steps:
                if step.type == 'model_output' and step.content:
                    for part in step.content:
                        if part.type == 'text':
                            print(f"Model Response: {part.text}")
                        elif part.type == 'image':
                            image_path = os.path.join(output_dir, f"nano_banana_campaign_{int(time.time())}.png")
                            with open(image_path, "wb") as f:
                                f.write(base64.b64decode(part.data))
                            print(f"-> Image successfully saved to: {image_path}")
                            
            return image_path
            
        except Exception as e:
            print(f"ERROR: Generation failed. Make sure GEMINI_API_KEY is set. Exception: {e}")
            return None

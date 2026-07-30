import os
import requests
import time
from inferencesh import inference

class ImageGenerator:
    """
    Adapter for Nano Banana Pro (Gemini 3.1 Flash Image Preview) via inferencesh.
    Takes a string prompt and saves the output image.
    """
    def __init__(self):
        try:
            api_key = os.environ.get("INFERENCESH_API_KEY")
            if api_key:
                self.client = inference(api_key=api_key)
            else:
                print("Warning: INFERENCESH_API_KEY not found in environment.")
                self.client = None
        except Exception as e:
            print("Warning: inferencesh client could not be initialized.", e)
            self.client = None

    def generate(self, prompt: str, output_dir: str = "output"):
        """
        Calls the inference engine and downloads the resulting image to output_dir.
        """
        if not self.client:
            print("Error: Inferencesh client is missing. Skipping generation.")
            return None
            
        print(f"Generating image with Nano Banana Pro...\nPrompt: {prompt}")
        
        try:
            result = self.client.run({
                "app": "google/gemini-3-1-flash-image-preview@0c7ma1ex",
                "input": {
                    "prompt": prompt,
                    "resolution": "4K"
                }
            })
            
            output_data = result.get("output", {})
            images = output_data.get("images", [])
            
            if not images:
                print("Error: No images were returned from the model.")
                return None
                
            image_url = images[0]
            print(f"Image generated! Downloading from {image_url}")
            
            # Ensure output dir exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # Download the image
            filename = f"campaign_{int(time.time())}.jpg"
            file_path = os.path.join(output_dir, filename)
            
            response = requests.get(image_url)
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
            print(f"Success! Image saved to {file_path}")
            return file_path
            
        except Exception as e:
            print(f"Error during image generation: {e}")
            return None

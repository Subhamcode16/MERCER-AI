import asyncio
from app.adapters.providers.base import BaseImageProvider

class ByteDanceProvider(BaseImageProvider):
    async def generate_image(self, prompt: str, model_name: str) -> bytes:
        print(f"[ByteDanceProvider] Calling Bytedance API with {model_name}: {prompt[:30]}...")
        await asyncio.sleep(1)
        
        with open("C:/Users/User/OneDrive/Desktop/Fashion Knowldge Wiki/Visual-Intelligence/product/backend/tests/mock_image.png", "rb") as f:
            return f.read()
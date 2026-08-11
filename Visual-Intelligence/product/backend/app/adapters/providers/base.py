from abc import ABC, abstractmethod

class BaseImageProvider(ABC):
    """
    Base interface for all Image Generation providers.
    """
    
    @abstractmethod
    async def generate_image(self, prompt: str, model_name: str) -> str:
        """
        Generates an image from the prompt using the specified model.
        Returns the raw binary bytes of the generated image.
        Raises an exception if the generation fails (to trigger fallbacks).
        """
        pass

from abc import ABC, abstractmethod
from PIL.Image import Image

class BgRemover(ABC):
    @abstractmethod
    async def remove_bg(self, image: Image) -> Image:
        """Removes background from an image and returns PIL.Image.Image object

        :param image: Original image (PIL.Image.Image object).
        """
        pass
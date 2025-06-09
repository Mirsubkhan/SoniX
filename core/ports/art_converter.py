from abc import ABC, abstractmethod
from PIL.Image import Image


class ArtConverter(ABC):
    @abstractmethod
    async def image_to_ascii(self, image: Image, char_width: int=300) -> Image:
        """Performs the conversion into an ASCII art and returns a PIL.Image.Image object.

        :param image: Original image (PIL.Image.Image object).
        :param char_width: Sets the detailing of ASCII-art.
        """
        pass
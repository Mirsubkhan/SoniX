from core.entities.file_dto import FileOutputDTO
from abc import ABC, abstractmethod
from PIL.Image import Image


class ASCIIConverter(ABC):
    @abstractmethod
    async def map_pixels_to_ascii(self, image: Image) -> Image:
        """Converts pixels into ASCII-symbols.

        :param image: Original image (PIL.Image object).
        """
        pass

    @abstractmethod
    async def image_to_ascii(self, image: Image, char_width: int=300) -> Image:
        """Converts image into ASCII-art and returns result as a PIL.Image object.

        :param image: Original image (PIL.Image object).
        :param char_width: Sets the detailing of ASCII-art.
        """
        pass
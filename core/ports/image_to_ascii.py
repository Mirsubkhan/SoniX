from core.entities.file_dto import FileOutputDTO
from abc import ABC, abstractmethod
from pathlib import Path
from PIL.Image import Image

class ImageToASCII(ABC):
    @abstractmethod
    async def map_pixels_to_ascii(self, image: Image) -> Image:
        pass

    @abstractmethod
    async def image_to_ascii(self, image: Image, fpath: Path, char_width: int=300) -> Image:
        pass
from abc import ABC, abstractmethod
from pathlib import Path
from PIL import Image
from core.entities.file import File

class PhotoStyleConverter(ABC):
    @abstractmethod
    async def map_pixels_to_ascii(self, image: Image, add_color=False) -> Image:
        pass

    @abstractmethod
    async def convert_image_to_ascii(self, file: File, add_color: bool=False) -> Path:
        pass
from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

class FileRepository(ABC):
    @abstractmethod
    async def open_img(self, path: Path) -> Image:
        pass

    @abstractmethod
    async def save_img(self, im: Image.Image, path: Path) -> None:
        pass
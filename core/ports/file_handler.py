from core.entities.file_dto import FileOutputDTO
from abc import ABC, abstractmethod
from numpy import ndarray
from pathlib import Path
from PIL import Image

class FileHandler(ABC):
    @abstractmethod
    async def open_img(self, fpath: Path) -> Image:
        pass

    @abstractmethod
    async def save_img(self, image: Image.Image, fpath: Path) -> FileOutputDTO:
        pass

    @abstractmethod
    async def save_as_txt(self, fpath: Path, text: str) -> FileOutputDTO:
        pass

    @abstractmethod
    async def open_img_with_cv2(self, fpath: Path):
        pass

    @abstractmethod
    async def save_img_with_cv2(self, image: ndarray, fpath: Path) -> FileOutputDTO:
        pass
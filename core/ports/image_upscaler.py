from abc import ABC, abstractmethod
from pathlib import Path
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from numpy import ndarray

class ImageUpscaler(ABC):
    @abstractmethod
    async def upscale_image(self, image: ndarray, fpath: Path) -> FileOutputDTO:
        pass

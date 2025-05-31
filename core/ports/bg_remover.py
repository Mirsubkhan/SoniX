from abc import ABC, abstractmethod
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from PIL.Image import Image

class BgRemover(ABC):
    @abstractmethod
    async def remove_bg(self, image: Image) -> Image:
        pass
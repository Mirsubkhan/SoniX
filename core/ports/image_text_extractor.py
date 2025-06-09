from core.entities.file_dto import FileInputDTO
from abc import ABC, abstractmethod
from PIL.Image import Image
from pathlib import Path


class ImageTextExtractor(ABC):
    @abstractmethod
    async def image_to_text(
            self,
            fpath: Path
    ) -> str:
        """Extracts text from an image.

        :param fpath: Path to the image file.
        """
        pass
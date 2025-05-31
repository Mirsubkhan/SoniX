from core.entities.file_dto import FileInputDTO
from abc import ABC, abstractmethod
from PIL.Image import Image
from pathlib import Path


class ImageTextExtractor(ABC):
    @abstractmethod
    async def image_to_text_handwritten(
            self,
            image: Image,
            fpath: Path
    ) -> str:
        """Extracts text from a handwritten image.

        :param image: PIL Image object to process.
        :param fpath: Path to the image file.
        """
        pass

    @abstractmethod
    async def image_to_text_printed(
            self,
            image: Image,
            fpath: Path
    ) -> str:
        """Extracts text from a printed image.

        :param image: PIL Image object to process.
        :param fpath: Path to the image file.
        """
        pass
from abc import ABC, abstractmethod
from pathlib import Path
from PIL.Image import Image
from core.entities.file_dto import FileOutputDTO

class ImageOCR(ABC):
    @abstractmethod
    async def image_to_text_handwritten(
            self,
            image: Image,
            fpath: Path
    ) -> FileOutputDTO:
        """Extracts text from a handwritten image.

        :param image: PIL Image object to process
        :param fpath: Path to the image file
        """
        pass

    @abstractmethod
    async def image_to_text_printed(
            self,
            image: Image,
            fpath: Path
    ) -> FileOutputDTO:
        """Extracts text from a printed image.

        :param image: PIL Image object to process
        :param fpath: Path to the image file
        """
        pass
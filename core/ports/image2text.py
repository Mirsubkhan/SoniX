from abc import ABC, abstractmethod
from pathlib import Path


class Image2Text(ABC):
    @abstractmethod
    async def image_to_text(
            self,
            fpath: Path
    ) -> str:
        """Extracts text from an image.

        :param fpath: Path to the image file.
        """
        pass
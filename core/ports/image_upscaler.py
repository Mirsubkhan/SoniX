from abc import ABC, abstractmethod
from numpy import ndarray
from pathlib import Path


class ImageUpscaler(ABC):
    @abstractmethod
    async def upscale_image(self, image: ndarray, fpath: Path) -> ndarray:
        """Increases image quality and returns ndarray object

        :param image: ndarray object
        :param fpath: Path object
        """
        pass

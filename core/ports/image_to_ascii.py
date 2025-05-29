from abc import ABC, abstractmethod
from PIL import Image
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class ImageToASCII(ABC):
    @abstractmethod
    async def map_pixels_to_ascii(self, image: Image) -> Image:
        pass

    @abstractmethod
    async def convert_image_to_ascii(self, file_input: FileInputDTO, char_width: int=300) -> FileOutputDTO:
        pass
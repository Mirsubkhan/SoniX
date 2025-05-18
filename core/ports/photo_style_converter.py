from abc import ABC, abstractmethod
from PIL import Image
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class PhotoStyleConverter(ABC):
    @abstractmethod
    async def map_pixels_to_ascii(self, image: Image, add_color=False) -> Image:
        pass

    @abstractmethod
    async def convert_image_to_ascii(self, file_input: FileInputDTO, add_color: bool=False) -> FileOutputDTO:
        pass
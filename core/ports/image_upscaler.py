from abc import ABC, abstractmethod
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class ImageUpscaler(ABC):
    @abstractmethod
    async def upscale_image(self, file_input: FileInputDTO) -> FileOutputDTO:
        pass

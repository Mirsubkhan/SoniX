from abc import ABC, abstractmethod
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class ImageOCR(ABC):
    @abstractmethod
    async def image_to_text(self, file_input: FileInputDTO, as_file: bool, lang: str) -> FileOutputDTO:
        pass
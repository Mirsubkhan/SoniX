from abc import ABC, abstractmethod
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class BackgroundRemover(ABC):
    @abstractmethod
    async def remove_bg(self, file: FileInputDTO) -> FileOutputDTO:
        pass
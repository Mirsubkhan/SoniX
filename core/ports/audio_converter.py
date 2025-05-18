from abc import ABC, abstractmethod
from core.entities.file import File
from pathlib import Path
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AudioConverter(ABC):
    @abstractmethod
    async def convert_to_wav(self, file_input: FileInputDTO) -> FileOutputDTO:
        pass
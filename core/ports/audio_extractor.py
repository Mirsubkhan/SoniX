from core.entities.file_dto import FileInputDTO, FileOutputDTO
from abc import ABC, abstractmethod

class AudioExtractor(ABC):
    @abstractmethod
    async def extract_audio(self, file_input: FileInputDTO) -> FileOutputDTO:
        """Extracts audio from a video and returns FileOutputDTO (file_path: Path)

        :param file_input: FileInputDTO object (file_path: Path)
        """
        pass
from abc import ABC, abstractmethod
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class AudioExtractor(ABC):
    @abstractmethod
    async def extract_audio_from_video(self, file_input: FileInputDTO) -> FileOutputDTO:
        pass
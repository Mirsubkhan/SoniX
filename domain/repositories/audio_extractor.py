from abc import ABC, abstractmethod
from domain.entities.file import File
from pathlib import Path

class IAudioExtractor(ABC):
    @abstractmethod
    async def extract_audio_from_video(self, file: File) -> Path:
        pass
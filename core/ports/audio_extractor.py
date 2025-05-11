from abc import ABC, abstractmethod
from core.entities.file import File
from pathlib import Path

class AudioExtractor(ABC):
    @abstractmethod
    async def extract_audio_from_video(self, file: File) -> Path:
        pass
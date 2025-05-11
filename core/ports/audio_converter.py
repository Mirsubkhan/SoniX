from abc import ABC, abstractmethod
from core.entities.file import File
from pathlib import Path

class AudioConverter(ABC):
    @abstractmethod
    async def convert_to_wav(self, file: File) -> Path:
        pass
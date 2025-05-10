from abc import ABC, abstractmethod
from domain.entities.file import File
from pathlib import Path

class IAudioConverter(ABC):
    @abstractmethod
    async def convert_to_wav(self, file: File) -> Path:
        pass
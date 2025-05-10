from abc import ABC, abstractmethod

from aiogram.types import Message

from domain.entities.file import File
from domain.entities.transcription_result import TranscriptionResult

class ITranscriber(ABC):
    @abstractmethod
    async def transcribe(self, file: File, message: Message = None, mid: int = None, rafile: bool = False):
        pass
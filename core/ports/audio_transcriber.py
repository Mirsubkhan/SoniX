from abc import ABC, abstractmethod
from typing import Callable, Awaitable
from core.entities.file_dto import FileInputDTO, FileOutputDTO


TranscribeProgressCallback = Callable[[int], Awaitable[None]]
DynamicProgressCallback = Callable[[str, bool], Awaitable[None]]

class AudioTranscriber(ABC):
    @abstractmethod
    async def transcribe_dynamic(self, file_input: FileInputDTO, on_progress: DynamicProgressCallback) -> None:
        pass

    @abstractmethod
    async def transcribe(self, file_input: FileInputDTO, on_progress: TranscribeProgressCallback) -> FileOutputDTO:
        pass
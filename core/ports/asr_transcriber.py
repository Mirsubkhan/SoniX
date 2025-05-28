from abc import ABC, abstractmethod
from typing import Callable, Awaitable
from core.entities.file_dto import FileInputDTO, FileOutputDTO


STTCallback = Callable[[int], Awaitable[None]]
DynamicSSTCallback = Callable[[str, bool], Awaitable[None]]

class ASRTranscriber(ABC):
    @abstractmethod
    async def transcribe_dynamic(self, file_input: FileInputDTO, on_progress: DynamicSSTCallback) -> None:
        pass

    @abstractmethod
    async def transcribe(self, file_input: FileInputDTO, on_progress: STTCallback) -> FileOutputDTO:
        pass
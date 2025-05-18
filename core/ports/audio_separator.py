from abc import ABC, abstractmethod
from typing import Callable, Awaitable
from core.entities.file_dto import FileInputDTO, FileOutputDTO

ProgressCallback = Callable[[int], Awaitable[None]]

class AudioSeparator(ABC):
    @abstractmethod
    async def separate(self, file_input: FileInputDTO, on_progress: ProgressCallback) -> FileOutputDTO:
        pass
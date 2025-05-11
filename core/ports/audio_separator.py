from abc import ABC, abstractmethod
from core.entities.file import File
from pathlib import Path
from typing import Callable, Awaitable

ProgressCallback = Callable[[int], Awaitable[None]]

class AudioSeparator(ABC):
    @abstractmethod
    async def separate(self, file: File, on_progress: ProgressCallback) -> Path:
        pass
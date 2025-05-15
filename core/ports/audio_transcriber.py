from abc import ABC, abstractmethod
from core.entities.file import File
from pathlib import Path
from typing import Callable, Awaitable

TranscribeProgressCallback = Callable[[int], Awaitable[None]]
DynamicProgressCallback = Callable[[str, bool], Awaitable[None]]

class AudioTranscriber(ABC):
    @abstractmethod
    async def transcribe_dynamic(self, file: File, on_progress: DynamicProgressCallback):
        """Динамическая транскрибация аудио внутри чата телеграма"""
        pass

    @abstractmethod
    async def transcribe(self, file: File, on_progress: TranscribeProgressCallback) -> Path:
        """транскрибация с выводом progress bar и вывод результата в .txt"""
        pass
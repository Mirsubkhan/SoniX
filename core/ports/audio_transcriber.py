from core.entities.file_dto import FileInputDTO
from typing import Union
from abc import ABC, abstractmethod
from config import DynamicSSTCallback, STTCallback


class AudioTranscriber(ABC):
    @abstractmethod
    async def transcribe_dynamic(
            self,
            file_input: FileInputDTO,
            on_progress: DynamicSSTCallback
    ) -> None:
        """Performs real-time transcription of audio and
        pushes partial results immediately to the chat interface.

        :param file_input: File metadata container (fpath: Path, f_duration: timedelta()).
        :param on_progress: Callback function invoked repeatedly during transcription.
        """
        pass

    @abstractmethod
    async def transcribe(self, file_input: FileInputDTO, on_progress: Union[STTCallback, None]) -> str:
        """Performs batch transcription of audio and
        returns full text upon completion. Supports progress tracking
        through a dynamic visual indicator (e.g., progress bar).

        :param file_input: File metadata container (fpath: Path, f_duration: timedelta()).
        :param on_progress: Callback function for progress notifications.
        """
        pass
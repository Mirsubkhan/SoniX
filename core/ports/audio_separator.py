from core.entities.file_dto import FileInputDTO, FileOutputDTO
from typing import Callable, Awaitable, Union
from abc import ABC, abstractmethod

SeparatorProgressCallback = Callable[[int], Awaitable[None]]

class AudioSeparator(ABC):
    @abstractmethod
    async def separate(
            self,
            f_input: FileInputDTO,
            on_progress: Union[SeparatorProgressCallback, None]
    ) -> FileOutputDTO:
        """Performs separation of audio into two parts: vocal and instrumental.

        :param f_input: File metadata container (fpath: Path).
        :param on_progress: Callback function for progress notifications.
        """
        pass
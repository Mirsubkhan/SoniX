from application.use_cases.audio_extractor_use_case import AudioExtractorUseCase
from core.ports.audio_separator import AudioSeparator, SeparatorProgressCallback
from core.entities.file_dto import FileInputDTO, FileOutputDTO
from core.entities.file import FileType
from typing import Union
from pathlib import Path

class AudioSeparatorUseCase:
    def __init__(self, separator: AudioSeparator, extractor: AudioExtractorUseCase):
        self.separator = separator
        self.extractor = extractor

    async def separate(self, f_input: FileInputDTO, on_progress: Union[SeparatorProgressCallback, None]) -> FileOutputDTO:
        f_input.file_path = await self._extract_audio(f_input=f_input)
        return await self.separator.separate(f_input, on_progress=on_progress)

    async def _extract_audio(self, f_input: FileInputDTO) -> Path:
        if f_input.file_type == FileType.VIDEO:
            file_output = await self.extractor.extract(file_input=f_input)
            f_input.file_path = file_output.file_path

        return f_input.file_path
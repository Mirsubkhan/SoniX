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

    async def separate(self, file_input: FileInputDTO, on_progress: Union[SeparatorProgressCallback, None]) -> FileOutputDTO:
        file_input.file_path = await self._extract_audio(file_input=file_input)
        return await self.separator.separate(file_input, on_progress=on_progress)

    async def _extract_audio(self, file_input: FileInputDTO) -> Path:
        if file_input.file_type == FileType.VIDEO:
            file_output = await self.extractor.extract(file_input=file_input)
            file_input.file_path = file_output.file_path

        return file_input.file_path
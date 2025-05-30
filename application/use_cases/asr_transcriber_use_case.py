from pathlib import Path

from core.entities.file import FileType
from core.ports.asr_transcriber import ASRTranscriber, DynamicSSTCallback, STTCallback
from application.use_cases.audio_extractor_use_case import AudioExtractorUseCase
from core.entities.file_dto import FileInputDTO, FileOutputDTO

class ASRTranscriberUseCase:
    def __init__(self, asr: ASRTranscriber, extractor: AudioExtractorUseCase):
        self.asr = asr
        self.extractor = extractor

    async def transcribe_dynamic(self, file_input: FileInputDTO, on_progress: DynamicSSTCallback) -> None:
        file_input.file_path = await self._extract_audio(file_input=file_input)
        return await self.asr.transcribe_dynamic(file_input, on_progress=on_progress)

    async def transcribe(self, file_input: FileInputDTO, on_progress: STTCallback) -> FileOutputDTO:
        file_input.file_path = await self._extract_audio(file_input=file_input)
        return await self.asr.transcribe(file_input=file_input, on_progress=on_progress)

    async def _extract_audio(self, file_input: FileInputDTO) -> Path:
        if file_input.file_type == FileType.VIDEO:
            file_output = await self.extractor.extract(file_input=file_input)
            file_input.file_path = file_output.file_path
            print("new", file_input.file_path)

        return file_input.file_path